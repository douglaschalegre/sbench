# Source Resolution

## Recency rule

From `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor source date resolution

| Vendor | Dated sources found | Current source used | Resolution |
|---|---:|---|---|
| Northstar | `vendor_quotes.csv` row dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | The CSV Northstar row dated 2026-04-24 is stale because the 2026-04-30 vendor-specific update is newer. |
| Atlas | `vendor_quotes.csv` dated 2026-04-27 | `vendor_quotes.csv` | No newer local source found. |
| BrightPath | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer local source found. |
| Cobalt | `vendor_quotes.csv` dated 2026-04-25 | `vendor_quotes.csv` | No newer local source found. |
| Dockside | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer local source found. |

## Effective Northstar terms used for screening

Using the newer `northstar_update_2026-04-30.md` source instead of the stale `vendor_quotes.csv` Northstar row dated 2026-04-24:

| Term | Effective value |
|---|---:|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | Included |
| Warranty | 12 months |
