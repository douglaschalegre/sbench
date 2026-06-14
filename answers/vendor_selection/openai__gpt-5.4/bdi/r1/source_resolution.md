# Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor source status

| Vendor | Source(s) reviewed | Source date(s) | Current source used | Reason |
|---|---|---:|---|---|
| Northstar | `vendor_quotes.csv`; `northstar_update_2026-04-30.md` | 2026-04-24; 2026-04-30 | `northstar_update_2026-04-30.md` | The CSV row is stale and the newer dated Northstar update supersedes it where values conflict. |
| Atlas | `vendor_quotes.csv` | 2026-04-27 | `vendor_quotes.csv` | Only local source provided for Atlas. |
| BrightPath | `vendor_quotes.csv` | 2026-04-26 | `vendor_quotes.csv` | Only local source provided for BrightPath. |
| Cobalt | `vendor_quotes.csv` | 2026-04-25 | `vendor_quotes.csv` | Only local source provided for Cobalt. |
| Dockside | `vendor_quotes.csv` | 2026-04-26 | `vendor_quotes.csv` | Only local source provided for Dockside. |

## Northstar stale vs current source

- Stale Northstar CSV row date: **2026-04-24** in `vendor_quotes.csv`.
- Newer Northstar update date: **2026-04-30** in `northstar_update_2026-04-30.md`.
- Effective Northstar terms used for screening come from the newer update.

## Effective Northstar terms used for screening

| Field | Effective value |
|---|---|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | included |
| Warranty | 12 months |
