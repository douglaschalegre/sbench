# Deliverable Contract

Create an `answer/` folder in this task folder, then create these three files inside it. The format may be Markdown tables or concise labeled sections, but the paths, filenames, and required facts must be present.

## `answer/policy_application.md`

Record which policy source controls this audit and the rules applied.

Required facts:

- The trip dates being audited.
- The current policy date and why it supersedes the stale policy excerpt.
- The receipt threshold.
- The seat-upgrade rule.
- The lodging cap calculation basis.
- The meal and alcohol rule.
- The ride-share tip cap.
- The supplies receipt rule.

## `answer/expense_decisions.md`

Record the item-level audit decision for every expense.

Required facts:

- One row or entry for every expense ID in `expenses.csv`.
- For each expense: claimed amount, approved amount, non-reimbursable amount, status (`approved`, `partial`, or `rejected`), and the policy or receipt reason.

## `answer/reimbursement_summary.md`

Write the final reimbursement summary for the finance teammate.

Required facts:

- Reimbursable total.
- Non-reimbursable total.
- Arithmetic showing how the reimbursable total was calculated.
- Fully approved expense IDs.
- Partially reimbursed or capped expense IDs.
- Rejected expense IDs.

Rules:

- Use local files only.
- Do not put the required deliverables in the task root; put them under `answer/`.
- Use dollar amounts rounded to two decimal places when needed.
- Extra scratch files are allowed, but scoring is based on the three named deliverables under `answer/`.
