from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_prompt import build_prompt, load_context
from context_snapshot import snapshot
from secret_scan import scan


def test_context_snapshot_redacts_credentials(tmp_path):
    (tmp_path / "package.json").write_text('{"name":"demo","api_key":"secret-value-12345"}', encoding="utf-8")
    result = snapshot(tmp_path)
    content = json.dumps(result)
    assert "secret-value-12345" not in content
    assert "REDACTED" in content


def test_prompt_modes_and_templates_are_specific():
    prompt = build_prompt("choose a database", "{\"files\": []}", "deep", "technical")
    assert "choose a database" in prompt
    assert "8 focused angles" in prompt
    assert "contradicting" in prompt.lower() or "conflicting" in prompt.lower()
    assert "technical" not in prompt.lower() or "architecture" in prompt.lower()


def test_history_input_and_secret_scan(tmp_path):
    context = tmp_path / "context.json"
    context.write_text('{"files":[]}', encoding="utf-8")
    assert json.loads(context.read_text()) == {"files": []}
    assert load_context(context) == '{\n  "files": []\n}'
    (tmp_path / "clean.md").write_text("public notes", encoding="utf-8")
    assert scan(tmp_path) == []

