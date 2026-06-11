---
title: Archive Answers With Canonical rN Runs
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 7-13, 32, 40-45, 47, 49
---

## What to build

Centralize answer archiving in the SBench orchestrator. Each harness-task run should start with a clean task-local `answer/` folder, allow the harness to write deliverables there, then archive the produced deliverables into the canonical future structure `answers/<task_id>/<model_path>/<harness>/rN/`, where `rN` is selected incrementally for that exact task, model path, and harness.

## Acceptance criteria

- [x] The orchestrator cleans or recreates `tasks/<task_id>/answer/` before each harness-task run.
- [x] Produced files from `tasks/<task_id>/answer/` are archived after each harness-task run.
- [x] Archived deliverables use `answers/<task_id>/<model_path>/<harness>/rN/` as the canonical destination.
- [x] `rN` is computed by scanning existing `r1`, `r2`, and later run folders for the same task, model path, and harness.
- [x] Run numbering is scoped per task, model path, and harness.
- [x] Existing canonical run folders are never overwritten by default.
- [x] Missing or empty `answer/` output is recorded as incomplete rather than silently treated as success.
- [x] Model names that are unsafe as path segments are normalized for archive paths.
- [x] Display model names are preserved separately from path-safe model names where metadata is available.
- [x] Legacy direct answer files under a harness folder are not treated as the canonical future format and are not overwritten.
- [x] Tests cover archive planning, `r1` selection with no prior canonical runs, next-run selection with prior canonical runs, per-scope numbering, overwrite prevention, path-safe model names, answer cleanup, and produced-file archiving.

## Blocked by

- 009-add-orchestrator-cli-list-and-dry-run.md
