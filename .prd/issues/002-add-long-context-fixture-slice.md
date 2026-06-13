---
title: Add A Long-Context Fixture Slice
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 2, 6-13, 29-33, 38, 42-45, 48-50, 52
---

## What to build

Add one complete local-file long-context task that pressures context retention while remaining manually runnable. The task should expose many plausible evidence files, place at least one important fact early in the evidence set, require that early fact in a final deliverable, include at least one stale-source conflict, and provide hidden expected answers and manual checkpoints outside the agent-facing task folder.

## Acceptance criteria

- [x] A new long-context task folder exists under `tasks/` with `task.md`, `output_contract.md`, and local Markdown or CSV evidence files.
- [x] The task can be solved from visible local files only and does not mention that it is a benchmark or evaluation task.
- [x] The fixture includes enough distractor material to require evidence selection rather than copying every visible fact.
- [x] At least one early-discovered fact is required in a late or final deliverable.
- [x] At least one stale or conflicting source must be resolved using visible source reliability rules.
- [x] Required deliverables are written under `answer/` and are independently scoreable.
- [x] Hidden expected-answer notes exist outside the agent-facing task folder.
- [x] The manual checklist includes task-specific correctness, context-retention, stale-source handling, and evidence-discipline checkpoints for this task.

## Blocked by

- 001-label-smoke-baseline-track.md
