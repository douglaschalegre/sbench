# Deterministic Evaluator Spike Notes

Deterministic evaluation is not part of the SBench MVP. The MVP remains manual and uses `evaluation/manual_checklist.md` plus hidden expected-deliverable notes.

These notes describe a future upgrade path after the fixture ambiguity and scoring-readiness review is complete. They do not require changing the current run protocol.

## Future Evaluator Shape

A future evaluator could accept:

- Path to a task folder.
- Path to the produced `answer/` folder and deliverable files for that task.
- Path to the hidden expected-deliverable data for that task.
- Optional run metadata from `templates/result_capture_template.md`.

The evaluator should never require expected deliverables or scoring rules to be placed in an agent-facing task folder.

## Manual Category To Deterministic Check Mapping

| Manual category | Possible deterministic check | Readiness |
| --- | --- | --- |
| Completion | Check which required deliverable files exist under `answer/` before scoring. | Straightforward |
| Artifact validity | Verify required `answer/` paths, readable text, and required sections or labels. | Partly deterministic |
| Deliverable independence | Score each required deliverable separately, even when later files are missing. | Straightforward |
| Golden answer fields | Compare exact expected fields such as selected vendor, total cost, responder names, and reimbursement total within the relevant deliverables. | Straightforward for current tasks |
| Arithmetic | Recompute simple totals such as `12 * 178`, reimbursement sums, caps, and allowed tip amounts. | Straightforward for current tasks |
| Evidence filenames | Verify cited filenames exist inside the task folder when files are cited. | Straightforward |
| Evidence relevance | Check whether cited files include required sources, such as update files or current policy files. | Partly deterministic |
| Stale-source handling | Require references to newest or current source files and compare fields affected by stale sources. | Partly deterministic |
| Rejection reasons | Check presence of expected rejected vendors, expenses, or candidates. | Partly deterministic |
| Extra files | Ignore scratch files for score unless they contain the only attempted answer or introduce contradictions. | Manual |
| Operational friction | Preserve as manual run metadata. | Manual |

## Hidden Expected Deliverables

Expected deliverable notes should remain outside `tasks/`, such as under `evaluation/expected_answers/` or a future private golden-data directory. Future automated checks can load those files locally, but agents should still receive only the relevant task folder.

## Checks Likely To Stay Manual

- Whether an evidence note genuinely supports the reasoning rather than merely naming the right file.
- Whether a rejection reason is clear enough for a human reviewer when phrased differently from the expected note.
- Whether semi-structured prose is clear enough to score when the agent does not use the suggested table shape.
- Whether framework setup friction is acceptable or materially affects comparison fairness.

## Non-Goals For The MVP

- No deterministic Python evaluator is implemented now.
- No changes are required to `protocol/strict_fair_run_protocol.md`.
- No LLM judge is introduced.
- No hidden expected-deliverable data is moved into agent-facing folders.
