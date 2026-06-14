## Source Resolution Checkpoint

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

| Vendor | Dated source(s) reviewed | Current source used | Reason |
| --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` row dated `2026-04-24`; `northstar_update_2026-04-30.md` dated `2026-04-30` | `northstar_update_2026-04-30.md` | The CSV row is stale because a newer dated vendor-specific update exists. |
| Atlas | `vendor_quotes.csv` row dated `2026-04-27` | `vendor_quotes.csv` | No newer local source found. |
| BrightPath | `vendor_quotes.csv` row dated `2026-04-26` | `vendor_quotes.csv` | No newer local source found. |
| Cobalt | `vendor_quotes.csv` row dated `2026-04-25` | `vendor_quotes.csv` | No newer local source found. |
| Dockside | `vendor_quotes.csv` row dated `2026-04-26` | `vendor_quotes.csv` | No newer local source found. |

Stale Northstar baseline row: `vendor_quotes.csv` lists Northstar on `2026-04-24`.

Newer Northstar update: `northstar_update_2026-04-30.md` provides revised terms dated `2026-04-30` and explicitly says to use that source instead of the older CSV row where they conflict.

### Effective Northstar Terms Used For Screening

| Field | Effective value |
| --- | --- |
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | Included |
| Warranty | 12 months |
