# Travel Reimbursement Audit Expected Deliverables

Hidden local note. Do not place this file in any agent-facing task folder.

Expected deliverables:

## `answer/policy_application.md`

Must apply `current_policy.md` dated 2026-04-20 instead of `stale_policy_excerpt.md` dated 2026-03-01.

Required policy facts:

- Trip dates are 2026-05-08 to 2026-05-10, so the current policy applies.
- Receipts are required for every expense of `$75.00` or more.
- Seat upgrades are not reimbursable without written preapproval.
- Lodging cap is `2 * 220.00 = 440.00`.
- Meals are reimbursable at actual cost up to `$65.00` per day, but alcohol is not reimbursable.
- Ride-share tips are capped at 20% of base fare.
- Supplies need a required receipt and a clear business purpose.

## `answer/expense_decisions.md`

Must include one row or entry per expense with these decisions:

| Expense | Status | Approved | Non-reimbursable | Expected reason |
| --- | --- | ---: | ---: | --- |
| T-001 | approved | `480.00` | `0.00` | Economy airfare is reimbursable with a receipt. |
| T-002 | rejected | `0.00` | `45.00` | Seat upgrade has no written preapproval. |
| T-003 | partial | `440.00` | `70.00` | Lodging is capped at 2 nights times `$220.00` per night. |
| T-004 | partial | `58.00` | `18.00` | Alcohol is not reimbursable, so only the food subtotal is approved. |
| T-005 | partial | `60.00` | `10.00` | Ride-share tip is capped at 20% of the `$50.00` base fare. |
| T-006 | rejected | `0.00` | `82.00` | No receipt is provided for an expense at or above `$75.00`. |
| T-007 | approved | `18.00` | `0.00` | Breakfast is within the meal policy and has receipt evidence. |

## `answer/reimbursement_summary.md`

Expected summary facts:

| Field | Expected value |
| --- | --- |
| Reimbursable total | `1056.00` |
| Non-reimbursable total | `225.00` |
| Fully approved IDs | `T-001`, `T-007` |
| Partially reimbursed IDs | `T-003`, `T-004`, `T-005` |
| Rejected IDs | `T-002`, `T-006` |

Required arithmetic:

```text
480.00 + 440.00 + 58.00 + 60.00 + 18.00 = 1056.00
```
