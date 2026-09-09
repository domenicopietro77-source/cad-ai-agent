# Capability reference — `cad-analyze` JSON shapes

Each subcommand prints one JSON object on stdout under `--json`. Lead your
summary with the **headline** field, then surface the **list** entries. All
fields come straight from the drawing — never invent them.

## compliance — `cad-analyze compliance <file> [--profile ada|ibc-2021|residential]`

```jsonc
{
  "profile_name": "ADA",
  "violation_count": 2,        // headline — >0 also makes the CLI exit 1
  "warning_count": 1,
  "pass_count": 5,
  "checks_run": ["door_widths", "hallway_widths", "..."],
  "findings": [                // exact ComplianceFinding keys
    { "rule_id": "ADA-DOOR-01", "category": "door",
      "severity": "violation", "title": "...", "description": "...",
      "code_reference": "...", "zone_id": null,
      "entity_handles": ["2A"], "measured_value": 32.0,
      "required_value": 36.0, "unit": "in" }
  ],
  "zone_count": 4, "entity_count": 312
}
```
Report the selected profile and implemented-check result, then each finding with
its measurements and entity handles. The built-in thresholds assume one drawing
unit equals one inch. These checks are screening evidence, not certification.

## health — `cad-analyze health <file>`

```jsonc
{
  "score": 90.0,              // headline — 0..100
  "entity_count": 312, "layer_count": 6,
  "checks_run": ["_check_overlapping_entities", "..."],
  "issues": [                 // exact HealthIssue keys
    { "severity": "warning", "category": "overlap", "title": "...",
      "description": "...", "evidence": [
        { "entity_handle": "2A", "layer": "WALLS", "description": "...",
          "entity_type": "LINE", "location": [1.0, 2.0], "text_excerpt": null }
      ], "check_name": "_check_overlapping_entities" }
  ]
}
```
Report: the score, then the issues grouped by severity.

## takeoff — `cad-analyze takeoff <file>`

```jsonc
{ "items": [ { "name": "Door", "category": "...", "quantity": 12, "unit": "ea",
              "source_layer": "DOORS", "zone_id": null, "entity_handles": [...], "notes": "" } ] }
```
Report: the quantities table (name / quantity / unit), grouped by category.

## summary — `cad-analyze summary <file>`

```jsonc
{
  "headline": "...", "drawing_type": "...", "entity_count": 312,
  "layer_count": 6, "total_area": 1200.0, "room_count": 4,
  "rooms": [{ "name": "Office", "area": 240.0, "zone_id": "..." }],
  "key_features": ["..."], "layer_breakdown": ["..."],
  "plain_description": "..."
}
```
Report: `headline`, `plain_description`, key features, layer breakdown, and rooms.

## rfi — `cad-analyze rfi <file>`

```jsonc
{
  "items": [{ "rfi_id": "...", "category": "missing_dimension",
    "severity": "major", "question": "...", "location_description": "...",
    "entity_handles": ["2A"], "zone_id": null,
    "suggested_resolution": "..." }],
  "total_items": 1, "critical_count": 0, "major_count": 1,
  "minor_count": 0, "checks_run": ["..."], "entity_count": 312,
  "zone_count": 4
}
```
Report the RFIs with their severity, location, evidence handles, and suggested
resolution. Treat generated questions as review aids, not verified defects.

## zones — `cad-analyze zones <file> [--tolerance 0.5]`

```jsonc
{
  "zones": [{ "zone_id": "...", "boundary": [{ "x": 0.0, "y": 0.0 }],
    "area": 240.0, "perimeter": 64.0,
    "centroid": { "x": 8.0, "y": 8.0 }, "inferred_type": "office",
    "source_handles": ["2A"], "confidence": 0.8 }],
  "total_area": 240.0, "zone_count": 1, "confidence": 0.8,
  "method": "polyline_and_line_tracing", "warnings": []
}
```
Report detected areas, inference confidence, method, warnings, and source
handles. Increasing `--tolerance` changes topology and must be user-directed;
do not silently tune it until a desired answer appears.

## compare — `cad-revision diff <master> <revision> [--json]`

Separate CLI. Exit codes: `0` = no changes, `1` = changes found, `2` = error.
This skill uses `diff` only. `apply` and `bundle` write output files and are
outside its read-only scope.
