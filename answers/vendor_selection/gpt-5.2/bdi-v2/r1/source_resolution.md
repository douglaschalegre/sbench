# Source resolution (recency rule)

## Recency rule (from `requirements.md`)
If a vendor appears in more than one **dated** source and values conflict, use the **newest dated source** for that vendor.

## Sources reviewed
- `vendor_quotes.csv` (contains vendor rows with `quote_date`)
- `northstar_update_2026-04-30.md` (explicitly supersedes older Northstar row)

## Vendor-by-vendor source currency
| Vendor | Dated sources present | Conflicts? | Effective source used | Why |
|---|---|---:|---|---|
| Northstar | `vendor_quotes.csv` (2026-04-24) and `northstar_update_2026-04-30.md` (2026-04-30) | yes | `northstar_update_2026-04-30.md` | Newer dated source per recency rule; update explicitly says to use it instead of the older CSV row |
| Atlas | `vendor_quotes.csv` (2026-04-27) only | no | `vendor_quotes.csv` | Only source |
| BrightPath | `vendor_quotes.csv` (2026-04-26) only | no | `vendor_quotes.csv` | Only source |
| Cobalt | `vendor_quotes.csv` (2026-04-25) only | no | `vendor_quotes.csv` | Only source |
| Dockside | `vendor_quotes.csv` (2026-04-26) only | no | `vendor_quotes.csv` | Only source |

## Required note: stale vs newer Northstar information
- **Stale Northstar row** in `vendor_quotes.csv` is dated **2026-04-24** (unit price $185).
- **Newer Northstar update** is `northstar_update_2026-04-30.md` dated **2026-04-30** (unit price $178).

## Effective Northstar terms used for screening (from `northstar_update_2026-04-30.md`)
| Field | Effective value |
|---|---|
| Unit price | **$178** |
| Available quantity | **12** |
| Delivery date | **2026-05-16** |
| Screen size | **10.1 in** |
| Battery rating | **11 hours** |
| Rugged case included? | **yes** |
| Warranty | **12 months** |
