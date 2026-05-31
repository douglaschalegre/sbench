# Expense decisions (item-level audit)

Source files used: `expenses.csv`, `receipts.md`, `current_policy.md`.

| Expense ID | Date | Category | Description | Claimed (USD) | Approved (USD) | Non-reimb. (USD) | Status | Decision basis (policy / receipt rationale) |
|---|---|---|---|---:|---:|---:|---|---|
| T-001 | 2026-05-08 | airfare | Round-trip economy airfare | 480.00 | 480.00 | 0.00 | approved | Receipt present; economy airfare reimbursable with receipt. |
| T-002 | 2026-05-08 | airfare | Exit-row seat upgrade | 45.00 | 0.00 | 45.00 | rejected | Optional seat upgrade not reimbursable without **written preapproval**; receipt evidence states no preapproval included. |
| T-003 | 2026-05-08 | lodging | Hotel stay for two covered nights | 510.00 | 440.00 | 70.00 | partial | Receipt present. Lodging capped at **2 nights × $220.00 = $440.00**; excess over cap is non-reimbursable. |
| T-004 | 2026-05-09 | meal | Team dinner with wine | 76.00 | 58.00 | 18.00 | partial | Receipt present; alcohol is not reimbursable. Food subtotal $58 approved; wine $18 removed. (Meal cap not exceeded after alcohol removal.) |
| T-005 | 2026-05-09 | rideshare | Airport ride-share with tip | 70.00 | 60.00 | 10.00 | partial | Receipt present. Base fare $50 reimbursable. Tip capped at **20% of $50 = $10**; claimed tip $20 so **$10** disallowed. |
| T-006 | 2026-05-10 | supplies | USB-C adapters purchased during trip | 82.00 | 0.00 | 82.00 | rejected | Claimed amount ≥ $75 requires receipt; **no receipt provided**, so not reimbursable (even though business purpose note exists). |
| T-007 | 2026-05-10 | meal | Breakfast | 18.00 | 18.00 | 0.00 | approved | Receipt present; meal amount $18 within $65/day cap. |
