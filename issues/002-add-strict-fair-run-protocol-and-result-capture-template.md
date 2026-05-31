# Add Strict Fair-Run Protocol And Result Capture Template

## Type

AFK

## User Stories Covered

15-18, 32-36, 40-46

## What to build

Add the local run protocol and result capture template needed to compare `pydantic-ai-bdi`, OpenClaw, and Hermes Agent fairly. The protocol should explain how to run one framework on one task with the same model, a fresh session, no retained memory where possible, and a 10-minute timeout.

The result template should make it easy to record the produced `answer.json`, task completion status, JSON validity, checkpoint outcomes, elapsed time, and framework setup friction.

## Acceptance criteria

- [ ] A local run protocol document exists for strict fair-run mode.
- [ ] The protocol tells the runner not to tell agents they are being evaluated.
- [ ] The protocol tells the runner to expose only the relevant task folder to the agent.
- [ ] The protocol specifies same model, fresh session, no memory or learned skills where possible, and a 10-minute timeout per task.
- [ ] A reusable result capture template exists for recording one framework-task run.
- [ ] The template captures completion, validity, accuracy notes, evidence discipline, contradiction handling, concision, and operational friction.
- [ ] The template supports all three target frameworks without framework-specific fields being required.

## Blocked by

- 001-add-vendor-quote-selection-tracer-task.md
