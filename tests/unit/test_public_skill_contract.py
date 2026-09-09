"""Regression tests for the public Agent Skill package."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "plugin" / "skills" / "cad-dxf-agent"


def _frontmatter() -> dict:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    _, raw, _ = text.split("---", 2)
    return yaml.safe_load(raw)


def test_skill_and_plugin_versions_match() -> None:
    manifest = json.loads((ROOT / "plugin" / ".claude-plugin" / "plugin.json").read_text())
    assert _frontmatter()["version"] == manifest["version"] == "0.2.0"


def test_skill_install_is_consent_bound_and_commit_pinned() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "ask for approval with `AskUserQuestion`" in text
    assert "cad-ai-agent.git@6393e61869187eec7416f7fe54bd2cec861ad39a" in text
    assert 'cad-ai-agent.git"' not in text
    assert "pip install cad-dxf-agent" not in text


def test_reference_uses_runtime_model_fields() -> None:
    text = (SKILL_DIR / "references" / "capabilities.md").read_text(encoding="utf-8")
    for field in (
        "rule_id",
        "entity_handles",
        "plain_description",
        "location_description",
        "inferred_type",
        "source_handles",
    ):
        assert f'"{field}"' in text
    assert '"context"' not in text
    assert '"label"' not in text


def test_skill_limits_compliance_claims() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "Screening, not certification" in text
    assert "one drawing unit equals one inch" in text
    assert "Empty `findings`/`issues` means no finding was produced" in text
