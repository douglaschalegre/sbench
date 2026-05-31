# Add Vendor Quote Selection Tracer Task

## Type

AFK

## User Stories Covered

1-14, 19-23, 32, 35, 37-39, 48-49

## What to build

Build the first complete SBench task slice: a local-file Vendor Quote Selection fixture that can be given to any agent framework as a standalone folder. The agent should read the task files, choose the best vendor under budget and requirements, resolve one stale quote conflict, and write `answer.json` using the shared SBench JSON shape.

This slice should be independently runnable and manually scoreable without any other task existing.

## Acceptance criteria

- [ ] A `vendor_selection` task folder exists with all agent-facing fixture files.
- [ ] The task instruction asks the agent to choose the best vendor and write only `answer.json`.
- [ ] The fixture includes requirements, budget, baseline quotes, and one newer vendor update that changes the correct answer.
- [ ] The correct answer is recoverable from the visible task files without external knowledge.
- [ ] The task has a hidden local expected-answer note outside the agent-facing task folder.
- [ ] The expected answer selects `Northstar`, uses quantity `12`, and computes total cost `2136`.
- [ ] The expected answer requires using the newer vendor update instead of the stale CSV quote.
- [ ] At least two rejected vendors have clear, fixture-supported rejection reasons.
- [ ] The task can be completed by reading local files only.

## Blocked by

None - can start immediately.
