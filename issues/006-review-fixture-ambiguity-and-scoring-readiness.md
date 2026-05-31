# Review Fixture Ambiguity And Scoring Readiness

## Type

HITL

## User Stories Covered

47-50

## What to build

Run a human review pass over the completed SBench fixture suite before using it for real framework comparisons. The review should confirm that each task has one intended answer, that stale or conflicting sources are intentional, that hidden expected answers are correct, and that manual checkpoints are fair.

This is a human-in-the-loop slice because it requires judgment about ambiguity, benchmark integrity, and whether the suite is ready to use.

## Acceptance criteria

- [ ] Each task is reviewed for accidental ambiguity.
- [ ] Each expected answer is recalculated manually and confirmed.
- [ ] Each stale or conflicting source is confirmed to be intentional and solvable.
- [ ] Each task instruction is checked to ensure it does not reveal evaluation details.
- [ ] The manual checklist is checked against the fixture files and expected answers.
- [ ] Any required fixture changes are recorded before running framework comparisons.
- [ ] The suite is marked ready or not ready for first framework comparison.

## Blocked by

- 005-consolidate-manual-evaluation-checklist-across-the-suite.md
