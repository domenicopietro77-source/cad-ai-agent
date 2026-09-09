# cad-dxf-agent (Claude Code plugin)

Deterministic DXF drawing analysis from natural language — **no LLM or API key
required at runtime**. The plugin ships a single skill, `cad-dxf-agent`, that
drives the `cad-analyze` and read-only `cad-revision diff` CLIs and reports the
findings with their evidence boundaries.

## Capabilities

| Capability | What it answers |
|---|---|
| compliance | built-in ADA / IBC / residential screening |
| health | drawing quality / QA (overlaps, text, orphan layers) |
| takeoff | automated quantity takeoff (counts, lengths, areas) |
| summary | plain-English drawing summary |
| rfi | RFIs generated from detected ambiguities |
| zones | closed-loop room/area detection with area calc |
| compare | revision diff between two DXFs (via `cad-revision`) |

## Prerequisite

The skill drives the CLIs from the `cad-dxf-agent` Python package. It checks for
an existing compatible installation first and asks before any network install.
The audited package revision used by skill version 0.2.0 is:

```bash
python3 -m pip install \
  "git+https://github.com/jeremylongshore/cad-ai-agent.git@6393e61869187eec7416f7fe54bd2cec861ad39a"
# verifies:
cad-analyze --version
```

## Use

Install the plugin's marketplace, enable it, then ask Claude Code to analyze a
DXF — e.g. *"check this floor plan for ADA compliance"* or *"run a health report
on drawing.dxf"*. The skill (`skills/cad-dxf-agent/SKILL.md`) handles the rest.

Compliance output is deterministic screening over the implemented rules and
supported drawing evidence. It is not a complete code review, certification,
permit approval, or substitute for the responsible professional.

## License

Apache-2.0 — see [LICENSE](LICENSE). Source: <https://github.com/jeremylongshore/cad-ai-agent>.
