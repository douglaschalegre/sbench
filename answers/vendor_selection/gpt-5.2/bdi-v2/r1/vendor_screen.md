# Vendor screening vs hard requirements

Hard requirements (from `requirements.md`):
- Quantity: **12 units** available
- Screen size: **>= 10.0 in**
- Battery: **>= 10 hours**
- Rugged case: **included** in price
- Warranty: **>= 12 months**
- Need-by: delivery **no later than 2026-05-17**
- Budget maximum: **$2,200 total**

## Screening table
Total cost is computed as `unit_price * 12` for vendors that otherwise meet hard requirements.

| Vendor | Effective source used | Eligible (meets all hard reqs)? | Unit price | Available qty | Delivery date | Screen (in) | Battery (h) | Case included | Warranty (mo) | Total cost (12 units) | Budget status | Blocking issue if ineligible |
|---|---|---|---:|---:|---|---:|---:|---|---:|---:|---|---|
| Northstar | `northstar_update_2026-04-30.md` (supersedes 2026-04-24 CSV row) | **yes** | 178 | 12 | 2026-05-16 | 10.1 | 11 | yes | 12 | 178*12 = **$2,136** | **Within** $2,200 | — |
| Atlas | `vendor_quotes.csv` (2026-04-27) | no | 168 | 12 | **2026-05-18** | 10.1 | 12 | yes | 12 | 168*12 = $2,016 | Within $2,200 (but irrelevant) | Delivery after need-by (must be <= 2026-05-17) |
| BrightPath | `vendor_quotes.csv` (2026-04-26) | no | 171 | 12 | 2026-05-15 | **9.7** | 10 | yes | 12 | 171*12 = $2,052 | Within $2,200 (but irrelevant) | Screen size below 10.0 in minimum |
| Cobalt | `vendor_quotes.csv` (2026-04-25) | no | 176 | 12 | 2026-05-16 | 10.1 | **9** | yes | 12 | 176*12 = $2,112 | Within $2,200 (but irrelevant) | Battery rating below 10 hours minimum |
| Dockside | `vendor_quotes.csv` (2026-04-26) | no | 182 | **11** | 2026-05-14 | 10.1 | 13 | yes | 12 | (cannot quote 12 units) | n/a | Available quantity is 11; must be 12 |

## Eligible vendors within budget
Only **Northstar** is eligible and within budget based on the effective (newest) Northstar terms.
