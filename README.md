# SBench

SBench is a local-file smoke suite for comparing agent frameworks on small operations tasks. Each task is self-contained and asks the agent to produce multiple semi-structured workplace deliverables under an `answer/` folder from local evidence only, so partial progress can be scored independently.

## Layout

- `tasks/`: agent-facing task fixture folders. Expose only one task folder to an agent run.
- `evaluation/`: hidden expected answers, manual checklist, and future evaluator notes. Do not expose these files to agents.
- `protocol/`: fair-run instructions for comparing frameworks consistently.
- `templates/`: reusable result capture documents.
- `issues/`: local implementation issue specs.

## Initial Tasks

- `vendor_selection`
- `travel_reimbursement_audit`
- `incident_staffing_plan`

For strict comparison runs, follow `protocol/strict_fair_run_protocol.md` and record each run with `templates/result_capture_template.md`.
