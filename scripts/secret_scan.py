#!/usr/bin/env python3
"""Scan text files for likely credentials before prompt generation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    "secret assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}"
    ),
}
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "__pycache__"}
SKIP_FILES = {".env", ".env.local", ".env.production"}


def scan(path: Path) -> list[tuple[str, int, str]]:
    files = [path] if path.is_file() else (
        p for p in path.rglob("*") if p.is_file() and not any(x in SKIP_DIRS for x in p.parts)
    )
    findings: list[tuple[str, int, str]] = []
    for file in files:
        if file.name in SKIP_FILES:
            findings.append((str(file), 0, "secret-bearing environment file"))
            continue
        try:
            content = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(content.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append((str(file), line_no, label))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    findings = scan(args.path)
    if findings:
        for file, line, label in findings:
            print(f"SECRET-LIKE {label}: {file}:{line}", file=sys.stderr)
        return 1
    print(f"secret scan passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

