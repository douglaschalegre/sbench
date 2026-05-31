# Vendor screen (hard requirements + budget)

Hard requirements (from `requirements.md`):
- Quantity: **12 units** available
- Screen: **≥ 10.0 in**
- Battery: **≥ 10 hours**
- Rugged case: **included**
- Warranty: **≥ 12 months**
- Delivery: **no later than 2026-05-17**

Budget: **$2,200 max total** for 12 units (total = unit_price_usd × 12).

## Screening table (all vendors in `vendor_quotes.csv`)

| Vendor | Effective source used | Unit price (USD) | Qty avail | Delivery | Screen (in) | Battery (hrs) | Rugged case | Warranty (mo) | Eligible (yes/no) | Blocking requirement (if no) | Total cost (if otherwise eligible) | Budget status (if eligible) |
|---|---|---:|---:|---:|---:|---:|---|---:|---|---|---:|---|
| **Northstar** | **`northstar_update_2026-04-30.md`** (supersedes CSV Northstar row dated 2026-04-24) | 178 | 12 | 2026-05-16 | 10.1 | 11 | yes | 12 | **yes** | — | **2136** | **Within budget** (2136 ≤ 2200) |
| Atlas | `vendor_quotes.csv` (2026-04-27) | 168 | 12 | 2026-05-18 | 10.1 | 12 | yes | 12 | no | Delivery later than 2026-05-17 | 2016 | — |
| BrightPath | `vendor_quotes.csv` (2026-04-26) | 171 | 12 | 2026-05-15 | 9.7 | 10 | yes | 12 | no | Screen size < 10.0 in | 2052 | — |
| Cobalt | `vendor_quotes.csv` (2026-04-25) | 176 | 12 | 2026-05-16 | 10.1 | 9 | yes | 12 | no | Battery hours < 10 | 2112 | — |
| Dockside | `vendor_quotes.csv` (2026-04-26) | 182 | 11 | 2026-05-14 | 10.1 | 13 | yes | 12 | no | Available quantity < 12 | 2184 | — |

## Eligible vendors and budget check

- Eligible vendors that pass all hard requirements: **Northstar only**.
- Budget result for eligible vendor(s): **Northstar total $2,136 is within the $2,200 cap**.

