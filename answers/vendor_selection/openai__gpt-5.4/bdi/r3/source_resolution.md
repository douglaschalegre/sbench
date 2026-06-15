# Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor source determination

| Vendor | Source(s) reviewed | Current source used | Reason |
|---|---|---|---|
| Northstar | `vendor_quotes.csv` dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | Northstar appears in more than one dated source, and the 2026-04-30 update is newer than the stale 2026-04-24 CSV row. |
| Atlas | `vendor_quotes.csv` dated 2026-04-27 | `vendor_quotes.csv` | Only local source for Atlas. |
| BrightPath | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | Only local source for BrightPath. |
| Cobalt | `vendor_quotes.csv` dated 2026-04-25 | `vendor_quotes.csv` | Only local source for Cobalt. |
| Dockside | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | Only local source for Dockside. |

## Northstar stale vs. current source

- Stale Northstar row: `vendor_quotes.csv` dated **2026-04-24**.
- Newer Northstar update: `northstar_update_2026-04-30.md` dated **2026-04-30**.
- Effective source used for screening Northstar: **`northstar_update_2026-04-30.md`**.

## Effective Northstar terms used for screening

| Field | Effective value |
|---|---|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | Included |
| Warranty | 12 months |
