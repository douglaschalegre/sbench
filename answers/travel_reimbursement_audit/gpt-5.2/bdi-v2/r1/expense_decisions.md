# Expense decisions (item-level audit)

Policy applied: `current_policy.md` (effective for trips starting 2026-05-01 or later). Receipt threshold $75.

| Expense ID | Date | Category | Description | Claimed (USD) | Approved (USD) | Non-reimb. (USD) | Status | Decision basis (policy / receipt reason) |
|---|---|---|---|---:|---:|---:|---|---|
| T-001 | 2026-05-08 | airfare | Round-trip economy airfare | 480.00 | 480.00 | 0.00 | approved | Receipt present; economy airfare reimbursable. |
| T-002 | 2026-05-08 | airfare | Exit-row seat upgrade | 45.00 | 0.00 | 45.00 | rejected | Optional seat upgrade; no written preapproval in receipt evidence => not reimbursable. |
| T-003 | 2026-05-08 | lodging | Hotel stay for two covered nights | 510.00 | 440.00 | 70.00 | partial | Lodging cap: 2 nights × $220.00 = $440.00 max; receipt present; amount above cap not reimbursable. |
| T-004 | 2026-05-09 | meal | Team dinner with wine | 76.00 | 58.00 | 18.00 | partial | Alcohol (wine $18.00) not reimbursable; food subtotal $58.00 reimbursable and within $65/day meal cap. |
| T-005 | 2026-05-09 | rideshare | Airport ride-share with tip | 70.00 | 60.00 | 10.00 | partial | Receipt shows base $50.00 + tip $20.00. Tip cap 20% of base = $10.00 reimbursable tip; approve $50.00 + $10.00 = $60.00. |
| T-006 | 2026-05-10 | supplies | USB-C adapters purchased during trip | 82.00 | 0.00 | 82.00 | rejected | Claimed >= $75 requires receipt; no receipt provided => not reimbursable (even though business purpose note exists). |
| T-007 | 2026-05-10 | meal | Breakfast | 18.00 | 18.00 | 0.00 | approved | Receipt present; meal is within $65/day cap. |
