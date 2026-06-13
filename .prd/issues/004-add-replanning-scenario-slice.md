---
title: Add A Replanning Scenario Slice
labels:
  - needs-triage
status: completed
type: AFK
user_stories_covered: 3, 6-9, 13-16, 32, 34-35, 39-40, 45, 48-50, 52
---

## What to build

Add one complete staged local task where the top-level objective stays stable but a visible update changes the best plan. A runner should be able to expose the initial task, introduce the staged update according to protocol, and score whether the agent repaired its plan without discarding correct completed work.

## Acceptance criteria

- [x] A new replanning task folder exists under `tasks/` with initial instructions, evidence files, staged update material, and an `output_contract.md`.
- [x] The task remains local-file only and can be solved from visible files without external services or web access.
- [x] The staged update changes the correct plan while preserving the original top-level objective.
- [x] The task instructions make the deliverable contract clear without revealing hidden scoring details.
- [x] Required deliverables under `answer/` expose the original plan, the update response, and the final repaired recommendation or work product.
- [x] Hidden expected-answer notes exist outside the agent-facing task folder.
- [x] The manual checklist includes plan-repair, goal-stability, context-retention, and progress-preservation checkpoints for this task.
- [x] The run protocol explains how and when to introduce the staged update consistently across harnesses.

## Blocked by

- 001-label-smoke-baseline-track.md
