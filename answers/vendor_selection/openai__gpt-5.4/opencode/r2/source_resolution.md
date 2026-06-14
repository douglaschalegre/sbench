## Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

| Vendor | Sources reviewed | Current source used | Notes |
| --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` row dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | The CSV row is stale because the newer dated update explicitly replaces conflicting Northstar values. |
| Atlas | `vendor_quotes.csv` row dated 2026-04-27 | `vendor_quotes.csv` | No newer local source provided. |
| BrightPath | `vendor_quotes.csv` row dated 2026-04-26 | `vendor_quotes.csv` | No newer local source provided. |
| Cobalt | `vendor_quotes.csv` row dated 2026-04-25 | `vendor_quotes.csv` | No newer local source provided. |
| Dockside | `vendor_quotes.csv` row dated 2026-04-26 | `vendor_quotes.csv` | No newer local source provided. |

### Effective Northstar Terms Used For Screening

The stale Northstar row in `vendor_quotes.csv` is dated 2026-04-24.

The newer Northstar update in `northstar_update_2026-04-30.md` sets the effective screening terms below:

| Field | Effective Northstar value |
| --- | --- |
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | included |
| Warranty months | 12 |
