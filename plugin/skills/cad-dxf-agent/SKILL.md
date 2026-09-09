---
name: cad-dxf-agent
description: Analyzes DXF drawings deterministically — ADA/IBC screening, drawing health and QA, quantity takeoff, plain-English summaries, RFI generation, room/zone detection, and revision comparison — with no LLM or API key at runtime. Use when a user has one or two .dxf files and wants evidence-grounded drawing analysis. Trigger with "analyze this DXF", "check compliance", "drawing health", "quantity takeoff", "summarize this drawing", "generate RFIs", "detect zones", "compare revisions", or "/cad-dxf-agent".
allowed-tools: Read, Glob, Bash(cad-analyze:*), Bash(cad-revision:*), Bash(python3:*), AskUserQuestion
argument-hint: a path to a .dxf file (and optionally which check — compliance, health, takeoff, summary, rfi, zones)
version: 0.2.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: Apache-2.0
compatibility: Claude Code with Python 3.11+ and the cad-dxf-agent CLI; portable instructions can be adapted for hosts that support Agent Skills and equivalent shell/file tools.
tags:
  - dxf
  - cad
  - compliance
  - takeoff
  - drawing-analysis
---

# cad-dxf-agent — DXF Drawing Analysis

## Overview

CAD reviewers manually scan drawings for code compliance, QA defects, quantities,
and ambiguities — slow and error-prone. This skill automates that for DXF files by
driving the deterministic `cad-analyze` CLI (no LLM, no API key, no network) and
reporting the findings in prose.

| Capability | What it answers | Command |
|---|---|---|
| **compliance** | What does the selected built-in screening profile flag? | `cad-analyze compliance FILE [--profile ada\|ibc-2021\|residential]` |
| **health** | Is the drawing clean? (overlaps, text, orphan layers) | `cad-analyze health FILE` |
| **takeoff** | How much of everything? (counts, lengths, areas) | `cad-analyze takeoff FILE` |
| **summary** | What is this drawing, in plain English? | `cad-analyze summary FILE` |
| **rfi** | What's ambiguous / needs clarification? | `cad-analyze rfi FILE` |
| **zones** | What rooms/areas are enclosed, and how big? | `cad-analyze zones FILE` |
| **compare** | What changed between two revisions? | `cad-revision diff MASTER REVISION` |

## Prerequisites

The CLI ships with the `cad-dxf-agent` Python package. Check it first:

```bash
cad-analyze --version
```

If it is missing, explain that installation downloads and executes a Python
package, ask for approval with `AskUserQuestion`, and only after approval run
the repository revision audited with this skill:

```bash
python3 -m pip install \
  "git+https://github.com/jeremylongshore/cad-ai-agent.git@6393e61869187eec7416f7fe54bd2cec861ad39a"
```

Do not claim a PyPI release exists and do not silently install from a mutable
branch. A user may instead provide an already-installed compatible build.

## Instructions

1. **Locate the DXF.** If the user named a file, use it; otherwise `Glob` for
   `**/*.dxf` and, if several match, ask which one with `AskUserQuestion`.
2. **Pick the capability** from the trigger words. If unclear, ask.
3. **Run the CLI with `--json`** and capture stdout, e.g. `cad-analyze health DRAWING.dxf --json`.
4. **Parse the JSON and report in prose** (see Output). For **compliance**, pass
   only a supported built-in `--profile`; default `ada`. State the drawing-unit
   assumption and screening limitations before the findings.

See `references/capabilities.md` for each report's JSON shape.

## Output

Report in prose, not raw JSON. Lead with the headline, then the notable entries:

- **compliance** → `violation_count` + each `findings[]` (`rule_id`,
  `code_reference`, measurements, and `entity_handles`).
- **health** → `score` (0–100) + `issues[]` grouped by `severity`.
- **takeoff** → the `items[]` quantities (name / quantity / unit) by category.
- **summary** → `headline`, `plain_description`, key features, and room list.
- **rfi** → the generated questions with severity, location, and entity handles.
- **zones** → detected areas with `inferred_type`, area, confidence, and source
  handles; do not turn an inferred type into a confirmed room label.

Always quote the drawing's own evidence (entity handles, layers) so the user can act.

## Error Handling

- `cad-analyze` exit `0` = completed without compliance violations; exit `1`
  = compliance violations present (valid JSON remains on stdout); exit `2` =
  invalid arguments, missing file, or unreadable DXF.
- `cad-analyze: command not found` → run the Prerequisites install, then retry.
- Empty `findings`/`issues` means no finding was produced by the implemented
  checks. Report that exact boundary; it is not proof of code compliance or a
  defect-free drawing.

## Examples

**"Check this floor plan for ADA compliance."**
```bash
cad-analyze compliance ./plans/level-1.dxf --profile ada --json
```
Read `violation_count`; if `> 0`, summarize each violation with its rule and
evidence handles, then state the drawing fails ADA on N items.

**"How clean is drawing.dxf?"**
```bash
cad-analyze health drawing.dxf --json
```
Report the `score`, then group `issues[]` by `severity` — e.g. "9 overlapping-entity
locations and inconsistent text heights on layer NOTES."

## Safety

- **Read-only by default.** `cad-analyze` and `cad-revision diff` do not modify
  the source DXF. Do not run `cad-revision apply` or `bundle` from this skill.
- **Offline at runtime.** The analysis capabilities make no network calls and
  use no secrets. Package installation is a separate, approved network action.
- **Screening, not certification.** Built-in ADA/IBC/residential rules are
  deterministic checks over supported DXF evidence, not a complete plan review,
  permit approval, or professional/legal determination. Default thresholds
  assume one drawing unit equals one inch. Confirm units, jurisdiction,
  amendments, and drawing completeness with the responsible professional.

Natural-language *editing* and agent-mode tool use require a bring-your-own LLM
provider (`CAD_LLM_PROVIDER=module:Class`) and are not exposed here — this skill
is analysis plus revision comparison only.

## Resources

- `references/capabilities.md` — JSON shape of each report and how to read it.
- Source + issues: <https://github.com/jeremylongshore/cad-ai-agent>
- `cad-analyze --help` / `cad-revision --help` — full CLI surface.
