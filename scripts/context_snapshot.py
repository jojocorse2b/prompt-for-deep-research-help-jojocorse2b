#!/usr/bin/env python3
"""Create a bounded, redacted snapshot of project context for a research prompt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MAX_FILE_BYTES = 40_000
MAX_FILES = 40
INTERESTING = {
    "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml",
    "go.mod", "Dockerfile", "README.md", "AGENTS.md", "CLAUDE.md",
}
SECRET = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[\"']?\s*[:=]\s*[\"']?[^\"'\s,}]+"
)


def snapshot(root: Path) -> dict:
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "node_modules", "dist", "build"} for part in path.parts):
            continue
        if path.name not in INTERESTING and path.suffix not in {".md", ".toml", ".yaml", ".yml", ".json", ".txt"}:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        text = SECRET.sub(r"\1=[REDACTED]", text)
        files.append({"path": str(path.relative_to(root)), "content": text})
        if len(files) >= MAX_FILES:
            break
    return {"root": str(root.resolve()), "files": files, "truncated": len(files) >= MAX_FILES}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    payload = snapshot(args.root)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) if args.json else "\n\n".join(
        f"### {item['path']}\n{item['content']}" for item in payload["files"]
    )
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
