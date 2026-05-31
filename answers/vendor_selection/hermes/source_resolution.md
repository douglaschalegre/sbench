# Source Resolution

Recency rule from requirements.md: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor source resolution

| Vendor | Current source used | Notes |
|---|---|---|
| Northstar | northstar_update_2026-04-30.md dated 2026-04-30 | vendor_quotes.csv has a stale Northstar row dated 2026-04-24. The newer Northstar update supersedes it where values conflict. |
| Atlas | vendor_quotes.csv row dated 2026-04-27 | No newer vendor-specific source found. |
| BrightPath | vendor_quotes.csv row dated 2026-04-26 | No newer vendor-specific source found. |
| Cobalt | vendor_quotes.csv row dated 2026-04-25 | No newer vendor-specific source found. |
| Dockside | vendor_quotes.csv row dated 2026-04-26 | No newer vendor-specific source found. |

## Effective Northstar terms used for screening

The stale Northstar row in vendor_quotes.csv is dated 2026-04-24. The newer Northstar update in northstar_update_2026-04-30.md is dated 2026-04-30, so the update is current under the recency rule.

Effective Northstar terms:

| Field | Effective value |
|---|---:|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | included |
| Warranty | 12 months |
