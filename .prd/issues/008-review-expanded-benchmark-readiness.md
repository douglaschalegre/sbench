---
title: Review Expanded Benchmark Readiness
labels:
  - needs-triage
status: draft
type: HITL
user_stories_covered: 8-9, 48-52
---

## What to build

Run a human readiness review for the expanded benchmark before using it for real framework comparisons. The review should confirm fixture solvability, hidden expected-answer correctness, scoring fairness, track separation, and whether the suite is ready to evaluate BDI context management and observability claims.

## Acceptance criteria

- [ ] Each expanded task is reviewed for accidental ambiguity and confirmed solvable from visible files alone.
- [ ] Hidden expected answers and required checkpoints are recalculated or manually confirmed.
- [ ] Stale-source conflicts, staged updates, recovery prior work, and distractor requests are confirmed intentional and fair.
- [ ] Task instructions are checked to ensure they do not reveal hidden evaluation criteria or benchmark framing.
- [ ] Manual scoring can distinguish correctness, context retention, goal stability, plan repair, progress preservation, and trace observability.
- [ ] BDI and non-BDI trace scoring are checked for comparable partial-credit opportunities.
- [ ] Smoke-track and context-pressure results remain clearly separated in protocol and scorecards.
- [ ] Any required fixture or scoring changes are recorded before real framework comparison runs begin.

## Blocked by

- 007-add-expanded-result-scorecards.md
