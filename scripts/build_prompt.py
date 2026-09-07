#!/usr/bin/env python3
"""Build, persist, and optionally copy a structured research prompt."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATES = {
    "general": "scope, alternatives, evidence quality, risks, and next actions",
    "technical": "compatibility, architecture, migration effort, performance, security, and operations",
    "product": "user problem, alternatives, adoption, UX, differentiation, metrics, and risks",
    "market": "market structure, competitors, pricing, demand signals, regulation, and scenarios",
    "scientific": "primary literature, methodology, replication, limitations, and open questions",
    "legal": "current authoritative rules, jurisdiction, obligations, exceptions, and uncertainty",
}


def load_context(path: Path | None) -> str:
    if not path:
        return "[No project context supplied; mark unknowns explicitly.]"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid context file: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("context file must contain a JSON object")
    return json.dumps(payload, indent=2, ensure_ascii=False)


def build_prompt(request: str, context: str, mode: str, template: str) -> str:
    angles = {"quick": 4, "standard": 6, "deep": 8}[mode]
    depth = {
        "quick": "Give a concise orientation and a short recommendation.",
        "standard": "Compare alternatives and finish with a decision matrix and recommendation.",
        "deep": "Perform multiple research rounds, include counter-evidence, and expose unresolved conflicts.",
    }[mode]
    return f"""## Objective
Research the following question and support a practical decision: {request}

## Context
Use only the verified project facts below. Treat missing information as [unknown] and do not invent details.

```json
{context}
```

## Investigate
Cover approximately {angles} focused angles relevant to {TEMPLATES[template]}. Include current alternatives, implementation or adoption effort, costs where relevant, security or regulatory risks, and the strongest counter-argument to the likely recommendation.

## Source Requirements
Use primary and authoritative sources first. Provide the URL, publisher, publication/update date, access date, source type, and a brief reliability assessment for each important source. Verify every material number, date, quotation, and causal claim. Show conflicting sources and explain the resolution; if unresolved, say so.

## Output Format
{depth}
Return: executive summary; methodology and scope; findings with inline source links; comparison matrix when applicable; recommendation with assumptions and trade-offs; contradictions; limitations; unknowns; and concrete next steps. Clearly label facts, inferences, and opinions.

## Constraints
Stay within the stated project context and decision. Do not use fabricated sources or unsupported claims. State the research date and flag information that may have changed. Avoid paid-only sources when a reliable public alternative exists.
"""


def copy_clipboard(text: str) -> bool:
    candidates = [("pbcopy", [])]
    if shutil.which("xclip"):
        candidates.append(("xclip", ["-selection", "clipboard"]))
    if shutil.which("wl-copy"):
        candidates.append(("wl-copy", []))
    if shutil.which("clip.exe"):
        candidates.append(("clip.exe", []))
    for command, args in candidates:
        if shutil.which(command):
            result = subprocess.run([command, *args], input=text, text=True, check=False)
            if result.returncode == 0:
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request")
    parser.add_argument("--context", type=Path)
    parser.add_argument("--mode", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--template", choices=sorted(TEMPLATES), default="general")
    parser.add_argument("--history-dir", type=Path, default=Path(".research-prompts"))
    parser.add_argument("--copy", action="store_true")
    args = parser.parse_args()
    try:
        prompt = build_prompt(args.request, load_context(args.context), args.mode, args.template)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    args.history_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = args.history_dir / f"{stamp}-{args.mode}-{args.template}.md"
    output.write_text(prompt, encoding="utf-8")
    copied = copy_clipboard(prompt) if args.copy else False
    print(prompt)
    print(f"\nSaved: {output}", file=sys.stderr)
    if args.copy:
        print("Copied to clipboard." if copied else "Clipboard unavailable; copy the prompt manually.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
