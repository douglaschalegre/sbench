---
title: Add A Distractor Goal Slice
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 6-9, 15, 17-18, 32, 34, 42, 45, 48-50, 52
---

## What to build

Add one complete local task with a stable core objective and plausible out-of-scope secondary requests. The task should verify whether an agent maintains goal stability, explicitly controls scope, and avoids completing distractor work as if it were part of the core deliverable.

## Acceptance criteria

- [ ] A new distractor-goal task folder exists under `tasks/` with `task.md`, `output_contract.md`, and local Markdown or CSV evidence files.
- [ ] The visible request includes a clear core objective plus plausible secondary requests that should remain out of scope.
- [ ] The task can be solved from visible local files only and does not mention benchmark scoring.
- [ ] Required deliverables under `answer/` complete the core objective and include explicit scope-control notes.
- [ ] Hidden expected-answer notes exist outside the agent-facing task folder.
- [ ] The manual checklist includes goal-stability, scope-control, evidence-discipline, and out-of-scope-work checkpoints for this task.
- [ ] Scoring does not reward extra unrelated work as core task completion.
- [ ] The task includes enough evidence to be solved deterministically by a careful human.

## Blocked by

- 001-label-smoke-baseline-track.md
