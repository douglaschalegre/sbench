---
title: Add Expanded Result Scorecards
labels:
  - needs-triage
status: draft
type: AFK
user_stories_covered: 29-37, 42-47, 49-51
---

## What to build

Add expanded result capture and manual rollup scorecards for the multi-track benchmark. A runner should be able to record elapsed time, completion, correctness, context retention, goal stability, plan repair, progress preservation, trace observability, operational friction, model calls, and token usage where available, while keeping smoke and context-pressure results clearly separated.

## Acceptance criteria

- [ ] The result capture template records benchmark track, task ID, framework, model, elapsed time, completion, and required deliverable status.
- [ ] The template records model call count and token usage when a harness exposes them, without requiring those fields for every harness.
- [ ] The template records checkpoint correctness, context retention, goal stability, plan repair, progress preservation, trace observability, and operational friction.
- [ ] The manual checklist or a companion scorecard explains how to score each expanded category as `pass`, `fail`, `partial`, or `n/a`.
- [ ] Smoke-track results and context-pressure results are labeled as different tracks.
- [ ] Final artifact correctness remains separate from trace observability.
- [ ] The scorecard can be applied manually to each expanded task without an LLM judge.
- [ ] The scorecard structure leaves room for later deterministic checks without requiring a deterministic evaluator now.

## Blocked by

- 002-add-long-context-fixture-slice.md
- 003-add-trace-observability-scoring.md
- 004-add-replanning-scenario-slice.md
- 005-add-recovery-audit-slice.md
- 006-add-distractor-goal-slice.md
