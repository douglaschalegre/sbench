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

## Trace Observability Checkpoints

Use these checkpoints only when the run record includes native traces, state summaries, to-do lists, tool traces, or comparable observable execution records. Do not require private chain-of-thought or hidden model reasoning.

Trace observability is scored independently from final artifact correctness. A trace can receive credit even when the final answer is wrong, and a correct final answer can have low trace observability.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| Trace source is identified, such as native harness logs, JSON events, BDI state summary, to-do list, tool trace, or run summary. |  |  |
| Trace availability is recorded as yes, partial, no, or n/a with limitations. |  |  |
| Current goal is observable without reading private chain-of-thought. |  |  |
| Current intention or equivalent task commitment is observable. |  | For BDI, this may be an intention; for non-BDI, this may be a to-do item, active task, or explicit plan commitment. |
| Active plan is observable. |  | BDI plans, task plans, to-do lists, or structured summaries can receive credit. |
| Current step is observable. |  |  |
| Completed-step history is observable. |  | BDI plan-step history, completed to-do entries, tool traces, file access logs, or run summaries can receive credit. |
| Reason for reconsideration is observable when the task includes conflict, stale data, staged updates, or replanning pressure. |  | Examples include a belief update, staged update notice, source conflict, or explicit correction note. |
| BDI state receives comparable credit for observable beliefs, desires, intentions, plans, plan steps, plan-step history, belief updates, and reconsideration reasons. |  |  |
| Non-BDI state receives comparable credit for observable to-do entries, task plans, summaries, tool traces, file operations, logs, and reconsideration notes. |  |  |
| Trace scoring excludes private chain-of-thought and does not reward disclosure of hidden reasoning. |  |  |
| Trace quality is not substituted for artifact correctness. |  |  |

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

## Clinic Rollout Plan Checkpoints

Use with `evaluation/expected_answers/clinic_rollout_plan.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/source_resolution.md` exists and states the newest-source reliability rule from `01_selection_rules.md`. |  |  |
| `answer/source_resolution.md` uses `04_storage_update_2026-05-06.md` over older roster or audit values where storage statuses conflict. |  |  |
| `answer/source_resolution.md` records effective storage status for every clinic in `02_site_roster.csv`. |  |  |
| `answer/source_resolution.md` does not treat archived policy, future-wave requests, or optional add-ons as controlling first-wave sources. |  |  |
| `answer/clinic_screen.md` exists and screens all eight clinics from `02_site_roster.csv`. |  |  |
| `answer/clinic_screen.md` grounds eligibility decisions in local roster, storage, availability, transport, and budget evidence rather than unsupported assumptions. |  | Evidence discipline checkpoint. |
| `answer/clinic_screen.md` marks Maple Junction, Riverbend, and Hillcrest eligible. |  |  |
| `answer/clinic_screen.md` rejects Pine Ridge for coordinator blackout, Lakeside for suspended storage, Cedar Works for closure or late delivery, Old Mill for pending storage, and South Gate for wrong region. |  |  |
| `answer/clinic_screen.md` computes selected-clinic total cost as `18800` against the `$20,000` first-wave budget. |  |  |
| `answer/launch_recommendation.md` exists and selects exactly Maple Junction, Riverbend, and Hillcrest. |  |  |
| `answer/launch_recommendation.md` includes the early intake fact that Maple Junction is the donor continuity anchor with code `MJ-14`. |  | Context retention checkpoint. |
| `answer/launch_recommendation.md` includes carriers and delivery dates for all selected clinics. |  |  |
| `answer/launch_recommendation.md` reports remaining budget `$1,200`. |  |  |

## Clinic Rollout Plan Trace Guidance

Use with `clinic_rollout_plan` when trace observability is being scored.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| Trace exposes the stable goal: select exactly three first-wave North-region clinics for the cooler rollout. |  |  |
| Trace exposes an active plan to resolve source reliability before final selection. |  |  |
| Trace or completed-step history shows the agent inspected early intake facts, including the Maple Junction donor continuity anchor and `MJ-14` code. |  | Context-retention trace checkpoint. |
| Trace shows the agent recognized newer storage evidence in `04_storage_update_2026-05-06.md` as controlling over older roster or audit storage values. |  | Reconsideration or belief-update credit can apply. |
| Trace shows evidence selection rather than copying every visible distractor file into the answer. |  |  |
| Trace limitations are recorded if only final deliverables are available and no intermediate state can be inspected. |  |  |

## Community Workshop Replan Checkpoints

Use with `evaluation/expected_answers/community_workshop_replan.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/initial_room_plan.md` exists and uses only initial planning files before the staged update. |  |  |
| `answer/initial_room_plan.md` assigns Safety Orientation to Harbor Hall, Inventory Lab to Bay Workshop, and Benefits Clinic to Elm Room. |  |  |
| `answer/initial_room_plan.md` computes the initial total as `$675` and keeps it within the `$800` ceiling. |  |  |
| Staged update introduction follows the protocol and is recorded in the run notes. |  |  |
| `answer/update_response.md` exists and identifies Bay Workshop closure as the changed fact from `05_facility_update_2026-06-10.md`. |  | Plan-repair checkpoint. |
| `answer/update_response.md` preserves Harbor Hall and Elm Room assignments rather than restarting or discarding correct work. |  | Progress-preservation checkpoint. |
| `answer/final_room_plan.md` exists and assigns Inventory Lab to Delta Annex after the update. |  |  |
| `answer/final_room_plan.md` retains the original session requirements and budget ceiling while applying the update. |  | Context-retention checkpoint. |
| `answer/final_room_plan.md` keeps the top-level objective stable by still covering all three sessions. |  | Goal-stability checkpoint. |
| `answer/final_room_plan.md` computes the repaired total as `$745` and remaining budget as `$55`. |  |  |

## Grant Closeout Recovery Checkpoints

Use with `evaluation/expected_answers/grant_closeout_recovery.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/audit_findings.md` exists and distinguishes preserved correct prior work from corrected or added work. |  |  |
| `answer/audit_findings.md` preserves the correct G-001 approval, G-003 approval, and G-004 rejection from the prior draft. |  | Progress-preservation checkpoint. |
| `answer/audit_findings.md` corrects the stale `$2,000` cap to the current `$1,600` cap. |  | Stale-source checkpoint. |
| `answer/audit_findings.md` identifies G-002, G-005, and omitted G-006 as prior-work issues. |  | Correction checkpoint. |
| `answer/corrected_expense_decisions.md` exists and includes every expense ID from G-001 through G-006. |  |  |
| `answer/corrected_expense_decisions.md` caps G-002 at `$120.00`, rejects G-005 for missing receipt over `$75`, and approves G-006 for `$68.00`. |  |  |
| `answer/final_closeout_summary.md` exists and computes total reimbursable amount `$1,588.00`. |  |  |
| `answer/final_closeout_summary.md` uses the current `$1,600` cap and reports `$12.00` remaining. |  |  |
| The work shows preservation and correction without unnecessary full rewrite of correct prior facts. |  | Unnecessary-rework checkpoint. |

## Shelter Restock Scope Control Checkpoints

Use with `evaluation/expected_answers/shelter_restock_scope.md`.

| Checkpoint | Score | Notes |
| --- | --- | --- |
| `answer/core_purchase_list.md` exists and completes the Phase 1 shelter restock objective. |  |  |
| `answer/core_purchase_list.md` selects R-101, R-102, R-103, and R-106. |  |  |
| `answer/core_purchase_list.md` excludes R-104 and R-105 for supported scope or approval reasons. |  | Scope-control checkpoint. |
| `answer/core_purchase_list.md` computes the selected total as `$2,130.00` and remaining budget as `$70.00`. |  |  |
| `answer/scope_control.md` exists and explicitly states the core objective. |  | Goal-stability checkpoint. |
| `answer/scope_control.md` defers banner design, volunteer training agenda, drone battery selection, and phase-two signage instead of completing them. |  | Out-of-scope-work checkpoint. |
| `answer/final_restock_note.md` exists and summarizes selected items, budget status, and deferred secondary requests. |  |  |
| Evidence cited or implied comes from local files and does not invent outside procurement facts. |  | Evidence-discipline checkpoint. |
| Extra unrelated work is not credited as core task completion. |  |  |
