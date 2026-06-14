## Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

Northstar appears in two local dated sources:

| Vendor | Source | Date | Status | Notes |
| --- | --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` | 2026-04-24 | Stale | Baseline row superseded by newer vendor-specific update. |
| Northstar | `northstar_update_2026-04-30.md` | 2026-04-30 | Current | Newest dated source, so this is the effective quote for screening. |

Effective Northstar terms used for screening:

| Vendor | Effective source | Unit price | Available quantity | Delivery date | Screen size | Battery rating | Rugged case | Warranty |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- | ---: |
| Northstar | `northstar_update_2026-04-30.md` | $178 | 12 | 2026-05-16 | 10.1 inches | 11 hours | included | 12 months |
