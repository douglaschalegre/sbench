# Add Deterministic Evaluator Spike Notes

## Type

AFK

## User Stories Covered

47, 50

## What to build

Document a future deterministic evaluator path without implementing it in the MVP. The notes should explain how the manual checklist could be translated into JSON schema validation, golden-answer checks, evidence filename checks, arithmetic checks, and stale-source handling checks.

This keeps the MVP focused on manual evaluation while preserving a clear upgrade path if SBench proves useful.

## Acceptance criteria

- [ ] A local spike note exists for a future deterministic evaluator.
- [ ] The note explicitly says deterministic evaluation is not part of the MVP.
- [ ] The note maps current manual checkpoint categories to possible deterministic checks.
- [ ] The note identifies which checks are straightforward and which may remain manual.
- [ ] The note describes how expected answers should remain hidden from agent-facing task folders.
- [ ] The note does not require changing the current run protocol.

## Blocked by

- 006-review-fixture-ambiguity-and-scoring-readiness.md
