---
title: Add A Recovery Audit Slice
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 4, 6-9, 19-22, 32, 35, 41-42, 45, 48-50, 52
---

## What to build

Add one complete recovery task that starts with partially correct prior artifacts. The agent should audit the existing work, preserve correct progress, correct wrong content, and produce final deliverables that make both preservation and correction visible.

## Acceptance criteria

- [x] A new recovery task folder exists under `tasks/` with prior partial artifacts, visible evidence files, `task.md`, and `output_contract.md`.
- [x] The prior work includes both correct content that should be preserved and incorrect content that should be corrected.
- [x] The task can be solved from visible local files only and does not reveal hidden scoring criteria.
- [x] Required deliverables under `answer/` show the audit result, preserved correct work, corrected wrong work, and final recommendation or summary.
- [x] Hidden expected-answer notes exist outside the agent-facing task folder.
- [x] The manual checklist includes progress-preservation, correction accuracy, evidence-discipline, and unnecessary-rework checkpoints for this task.
- [x] Scoring can distinguish an agent that rewrites everything from one that preserves useful correct progress.
- [x] The fixture remains small enough to run manually.

## Blocked by

- 001-label-smoke-baseline-track.md
