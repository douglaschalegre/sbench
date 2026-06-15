## Source Resolution

Checkpoint: source-resolution

- Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.
- `vendor_quotes.csv` contains a stale Northstar row dated `2026-04-24`.
- `northstar_update_2026-04-30.md` is the newer Northstar source dated `2026-04-30`, so it overrides the CSV row where values conflict.

| Vendor | Source(s) reviewed | Current source used | Reason |
| --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` (`2026-04-24`), `northstar_update_2026-04-30.md` (`2026-04-30`) | `northstar_update_2026-04-30.md` | Newer dated source for the same vendor |
| Atlas | `vendor_quotes.csv` (`2026-04-27`) | `vendor_quotes.csv` | Only dated source present |
| BrightPath | `vendor_quotes.csv` (`2026-04-26`) | `vendor_quotes.csv` | Only dated source present |
| Cobalt | `vendor_quotes.csv` (`2026-04-25`) | `vendor_quotes.csv` | Only dated source present |
| Dockside | `vendor_quotes.csv` (`2026-04-26`) | `vendor_quotes.csv` | Only dated source present |

## Effective Northstar Terms

Checkpoint: effective-northstar-terms

| Field | Effective value used for screening |
| --- | --- |
| Unit price | `$178` |
| Available quantity | `12` |
| Delivery date | `2026-05-16` |
| Screen size | `10.1 inches` |
| Battery rating | `11 hours` |
| Rugged case status | `included` |
| Warranty months | `12` |
