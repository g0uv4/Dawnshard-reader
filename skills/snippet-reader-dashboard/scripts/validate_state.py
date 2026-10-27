#!/usr/bin/env python3
"""Check a Snippet Reader state.json.

Usage: python3 validate_state.py [path/to/state.json]
Uses the JSON Schema in ../../snippet-reader-getting-started/references/ when the
`jsonschema` package is installed; always runs the dependency-free checks below.
"""
import json, pathlib, sys

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".snippet-reader/state.json")
s = json.loads(path.read_text(encoding="utf-8"))
errors, notes = [], []
schema = pathlib.Path(__file__).resolve().parents[2] / "snippet-reader-getting-started/references/state.schema.json"
try:
    import jsonschema
    v = jsonschema.Draft202012Validator(json.loads(schema.read_text(encoding="utf-8")))
    errors += [f"schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in v.iter_errors(s)]
except ImportError:
    notes.append("jsonschema not installed: basic checks only")
except FileNotFoundError:
    notes.append(f"schema not found at {schema}: basic checks only")

STATUSES = {"unread", "in_progress", "done", "expired", "queued", "shelved"}
if s.get("version") != 1: errors.append("version must be 1")
if not isinstance(s.get("points"), int) or s["points"] < 0: errors.append("points must be a non-negative integer")
log_total = sum(e.get("delta", 0) for e in s.get("points_log", []))
if s.get("points_log") and log_total != s.get("points"): errors.append(f"points {s.get('points')} != points_log sum {log_total}")
ids = set()
for a in s.get("articles", []) + s.get("queue", []):
    for k in ("id", "title", "kind", "slices_total", "current_slice", "added_at", "status"):
        if k not in a: errors.append(f"article {a.get('id', '?')}: missing {k}")
    if a.get("id") in ids: errors.append(f"duplicate article id {a.get('id')}")
    ids.add(a.get("id"))
    if a.get("status") not in STATUSES: errors.append(f"article {a.get('id')}: unknown status {a.get('status')}")
    if a.get("current_slice", 0) > a.get("slices_total", 0): errors.append(f"article {a.get('id')}: current_slice > slices_total")
print("\n".join(errors + notes) or "", end="\n" if errors or notes else "")
if not errors: print(f"OK ({len(s.get('articles', []))} articles, points {s.get('points')})")
sys.exit(1 if errors else 0)
