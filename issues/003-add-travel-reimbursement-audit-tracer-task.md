# Add Travel Reimbursement Audit Tracer Task

## Type

AFK

## User Stories Covered

1-14, 19, 24-27, 32, 35, 37-39, 48-49

## What to build

Build the second complete SBench task slice: a local-file Travel Reimbursement Audit fixture that can be given to any agent framework as a standalone folder. The agent should read the task files, apply the current finance policy, ignore a stale policy excerpt, classify expenses, apply caps and exclusions, calculate the reimbursable total, and write `answer.json` using the shared SBench JSON shape.

This slice should be independently runnable and manually scoreable.

## Acceptance criteria

- [ ] A `travel_reimbursement_audit` task folder exists with all agent-facing fixture files.
- [ ] The task instruction asks the agent to calculate reimbursable total and write only `answer.json`.
- [ ] The fixture includes current policy, stale policy excerpt, expenses, and receipt evidence.
- [ ] The correct answer depends on using the current policy over the stale policy excerpt.
- [ ] The fixture includes alcohol, hotel cap, excessive ride-share tip, missing receipt, and seat upgrade cases.
- [ ] The correct reimbursable total is recoverable from the visible task files without external knowledge.
- [ ] The task has a hidden local expected-answer note outside the agent-facing task folder.
- [ ] The expected answer distinguishes approved, rejected, and capped items.
- [ ] The task can be completed by reading local files only.

## Blocked by

- 001-add-vendor-quote-selection-tracer-task.md
