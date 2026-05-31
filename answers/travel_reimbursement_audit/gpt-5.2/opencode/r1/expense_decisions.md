# Expense Decisions (Checkpoint 2: Item-Level Audit)

Policy source used for all decisions: `current_policy.md` (effective for trips starting on/after 2026-05-01).

| Expense ID | Date | Category | Claimed (USD) | Approved (USD) | Non-reimbursable (USD) | Status | Decision Basis (Policy / Receipt Evidence) |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| T-001 | 2026-05-08 | airfare | 480.00 | 480.00 | 0.00 | approved | Economy airfare reimbursable with receipt. Receipt present in `receipts.md`. |
| T-002 | 2026-05-08 | airfare | 45.00 | 0.00 | 45.00 | rejected | Seat upgrade not reimbursable without written preapproval; receipt evidence notes no preapproval in `receipts.md`. |
| T-003 | 2026-05-08 | lodging | 510.00 | 440.00 | 70.00 | partial | Lodging capped at $220.00/night including taxes/fees. Covered nights = 2, cap = 440.00; receipt present. |
| T-004 | 2026-05-09 | meal | 76.00 | 58.00 | 18.00 | partial | Alcohol is not reimbursable and must be removed; receipt breaks out food 58.00 and wine 18.00 in `receipts.md`. Food amount is within $65.00/day cap. |
| T-005 | 2026-05-09 | rideshare | 70.00 | 60.00 | 10.00 | partial | Tip cap is 20% of base fare. Receipt shows base 50.00, tip 20.00; allowed tip = 10.00 (20% of 50.00). |
| T-006 | 2026-05-10 | supplies | 82.00 | 0.00 | 82.00 | rejected | Claimed amount is >= 75.00 so a receipt is required; `receipts.md` indicates no receipt provided. Supplies require required receipt + clear business purpose. |
| T-007 | 2026-05-10 | meal | 18.00 | 18.00 | 0.00 | approved | Meal is within $65.00/day cap; receipt present in `receipts.md`. |
