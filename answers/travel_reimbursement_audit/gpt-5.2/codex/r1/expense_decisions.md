# Item-level audit checkpoint: expense decisions

All amounts are USD.

| expense_id | claimed | approved | non_reimbursable | status | reason (policy / receipt evidence) |
|---|---:|---:|---:|---|---|
| T-001 | 480.00 | 480.00 | 0.00 | approved | Economy airfare with receipt is reimbursable (`receipts.md`, current airfare rule). |
| T-002 | 45.00 | 0.00 | 45.00 | rejected | Seat upgrade has **no written preapproval**, so not reimbursable (`receipts.md`, current seat-upgrade rule). |
| T-003 | 510.00 | 440.00 | 70.00 | partial | Lodging capped at **2 nights × $220.00 = $440.00** (`current_policy.md` lodging cap; `receipts.md` hotel folio). |
| T-004 | 76.00 | 58.00 | 18.00 | partial | Alcohol (wine **$18.00**) removed; remaining food subtotal **$58.00** reimbursable and within **$65/day** cap (`receipts.md`, current meals rule). |
| T-005 | 70.00 | 60.00 | 10.00 | partial | Tip capped at **20% × $50.00 = $10.00**; approve base **$50.00** + tip **$10.00** (`receipts.md`, current ride-share tip rule). |
| T-006 | 82.00 | 0.00 | 82.00 | rejected | Claimed **$82.00** is >= **$75.00** receipt threshold, but **no receipt provided**, so not reimbursable (`receipts.md`, current receipt threshold + supplies receipt rule). |
| T-007 | 18.00 | 18.00 | 0.00 | approved | Meal with receipt; **$18.00** within **$65/day** cap (`receipts.md`, current meals rule). |

