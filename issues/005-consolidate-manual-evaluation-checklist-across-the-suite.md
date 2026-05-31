# Consolidate Manual Evaluation Checklist Across The Suite

## Type

AFK

## User Stories Covered

13-14, 35, 37-39, 41-46, 47

## What to build

Create the suite-level manual evaluation checklist for post-run scoring. The checklist should let a human evaluator score each task after the agent completes without exposing hidden criteria to the agent during execution.

The checklist should cover completion, JSON validity, task identity, answer correctness, evidence discipline, contradiction handling, unnecessary assumptions, and operational friction.

## Acceptance criteria

- [ ] A local manual checklist document exists outside all agent-facing task folders.
- [ ] The checklist includes common checkpoints that apply to every task.
- [ ] The checklist includes task-specific checkpoints for Vendor Quote Selection.
- [ ] The checklist includes task-specific checkpoints for Travel Reimbursement Audit.
- [ ] The checklist includes task-specific checkpoints for Incident Staffing Plan.
- [ ] The checklist can be applied using only the final `answer.json`, task files, and hidden expected-answer notes.
- [ ] The checklist records pass/fail and notes for each checkpoint.
- [ ] The checklist does not require an LLM judge.

## Blocked by

- 003-add-travel-reimbursement-audit-tracer-task.md
- 004-add-incident-staffing-plan-tracer-task.md
