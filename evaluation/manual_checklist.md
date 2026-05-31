# Manual Evaluation Checklist

Hidden local document. Do not expose this checklist to agents during task execution.

Use this checklist after a run finishes. It can be applied with the produced deliverables, the relevant agent-facing task files, and the hidden expected-deliverable note for that task. No LLM judge is required.

Scoring values: `pass`, `fail`, `partial`, or `n/a`.

## Common Checkpoints

| Checkpoint | Score | Notes |
| --- | --- | --- |
| Completion: each required named deliverable exists under `answer/` by the 10-minute timeout. |  | Score each deliverable independently. |
| Partial progress: incomplete runs receive credit for any correct deliverable or correct section within a deliverable. |  |  |
| Artifact validity: files are readable Markdown, CSV, or text and use the requested `answer/` paths. |  |  |
| Deliverable contract: required sections, labels, rows, or facts from `output_contract.md` are present. |  |  |
| Work correctness: task-specific facts match the hidden expected-deliverable note. |  |  |
| Evidence discipline: cited or implied source files exist in the task folder and support the work. |  |  |
| Contradiction handling: the work uses the intended current or newest source over stale data. |  |  |
| Unsupported assumptions: any assumptions are explicit and limited to gaps in the local files. |  |  |
| Extra files: scratch files do not replace the required deliverables under `answer/` or contradict them. |  | Extra scratch files are allowed. |
| Operational friction: setup, file access, prompting, timeout, or output issues are recorded. |  |  |

## Vendor Quote Selection Checkpoints

Use with `evaluation/expected_answers/vendor_selection.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/source_resolution.md` exists and identifies the Northstar source conflict. |  |  |
| `answer/source_resolution.md` uses `northstar_update_2026-04-30.md` over the stale Northstar CSV row. |  |  |
| `answer/source_resolution.md` records updated Northstar terms, including unit price `178`. |  |  |
| `answer/vendor_screen.md` exists and screens all five vendors. |  |  |
| `answer/vendor_screen.md` marks Northstar eligible and computes total cost `2136`. |  |  |
| `answer/vendor_screen.md` rejects Atlas, BrightPath, Cobalt, and Dockside with file-supported reasons. |  |  |
| `answer/purchase_recommendation.md` exists and selects `Northstar`. |  |  |
| `answer/purchase_recommendation.md` uses quantity `12`, unit price `178`, and total cost `2136`. |  |  |
| `answer/purchase_recommendation.md` confirms the result is within the `$2,200` budget. |  |  |

## Travel Reimbursement Audit Checkpoints

Use with `evaluation/expected_answers/travel_reimbursement_audit.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/policy_application.md` exists and applies `current_policy.md` over `stale_policy_excerpt.md`. |  |  |
| `answer/policy_application.md` captures receipt threshold, seat-upgrade rule, lodging cap, meal/alcohol rule, ride-share tip cap, and supplies receipt rule. |  |  |
| `answer/expense_decisions.md` exists and includes every expense ID from T-001 through T-007. |  |  |
| `answer/expense_decisions.md` approves T-001 economy airfare at `480.00`. |  |  |
| `answer/expense_decisions.md` rejects T-002 seat upgrade because there is no preapproval. |  |  |
| `answer/expense_decisions.md` caps T-003 lodging at `440.00`. |  |  |
| `answer/expense_decisions.md` excludes T-004 alcohol and approves only `58.00` food. |  |  |
| `answer/expense_decisions.md` caps T-005 ride-share tip and approves `60.00`. |  |  |
| `answer/expense_decisions.md` rejects T-006 because a required receipt is missing. |  |  |
| `answer/expense_decisions.md` approves T-007 breakfast at `18.00`. |  |  |
| `answer/reimbursement_summary.md` exists and computes reimbursable total `1056.00`. |  |  |
| `answer/reimbursement_summary.md` distinguishes fully approved, partially reimbursed, and rejected items. |  |  |

## Incident Staffing Plan Checkpoints

Use with `evaluation/expected_answers/incident_staffing_plan.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/access_resolution.md` exists and covers every responder in the roster. |  |  |
| `answer/access_resolution.md` uses `access_update_2026-05-04.md` over stale roster access values. |  |  |
| `answer/access_resolution.md` marks Ben active, Carmen suspended, and Gabe not provisioned. |  |  |
| `answer/candidate_screen.md` exists and screens every responder for primary and backup eligibility. |  |  |
| `answer/candidate_screen.md` marks Ben eligible for primary. |  |  |
| `answer/candidate_screen.md` marks Deepa eligible for backup but not primary. |  |  |
| `answer/candidate_screen.md` rejects Asha because she is at the active-incident limit. |  |  |
| `answer/candidate_screen.md` rejects Carmen because newest access data suspends `db-prod` access. |  |  |
| `answer/candidate_screen.md` rejects Eli because of role-rule mismatch. |  |  |
| `answer/candidate_screen.md` rejects Farah because she is unavailable for the full window. |  |  |
| `answer/candidate_screen.md` rejects Gabe because he lacks active `db-prod` access. |  |  |
| `answer/staffing_assignment.md` exists and selects `Ben` as primary responder. |  |  |
| `answer/staffing_assignment.md` selects `Deepa` as backup responder and does not assign the same person twice. |  |  |
