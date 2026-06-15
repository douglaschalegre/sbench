# Source Resolution

## Recency rule
Per `requirements.md`: **If a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.**

## Vendor source status

| Vendor | Source(s) reviewed | Current source used | Resolution |
|---|---|---|---|
| Northstar | `vendor_quotes.csv` dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | The Northstar row in `vendor_quotes.csv` is stale. The newer dated Northstar update overrides conflicting Northstar values. |
| Atlas | `vendor_quotes.csv` dated 2026-04-27 | `vendor_quotes.csv` | No newer vendor-specific local source found. |
| BrightPath | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer vendor-specific local source found. |
| Cobalt | `vendor_quotes.csv` dated 2026-04-25 | `vendor_quotes.csv` | No newer vendor-specific local source found. |
| Dockside | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer vendor-specific local source found. |

## Effective Northstar terms used for screening
Using the newer `northstar_update_2026-04-30.md`, the effective Northstar terms are:

| Field | Effective value |
|---|---|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | Included |
| Warranty months | 12 |
