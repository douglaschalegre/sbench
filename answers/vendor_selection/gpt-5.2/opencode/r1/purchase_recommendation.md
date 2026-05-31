# Purchase Recommendation

Select Northstar for the field inspection team tablet order.

| Fact | Recommendation detail |
| --- | --- |
| Selected vendor | Northstar |
| Quantity | 12 tablets |
| Unit price | $178 |
| Total cost calculation | 12 x $178 = $2,136 |
| Budget result | Within the $2,200 maximum by $64 |
| Delivery date | 2026-05-16, which is before the 2026-05-17 need-by date |

## Rationale

Northstar is the only vendor that meets all hard requirements after applying the recency rule. Its newer `northstar_update_2026-04-30.md` terms replace the stale `vendor_quotes.csv` row dated 2026-04-24, and the effective quote provides 12 units, 10.1-inch screens, 11-hour battery rating, rugged cases included, 12-month warranty, and delivery by 2026-05-16.

## Rejected-Vendor Summary

| Vendor | Reason rejected |
| --- | --- |
| Atlas | Delivery date is 2026-05-18, after the 2026-05-17 need-by date. |
| BrightPath | Screen size is 9.7 inches, below the 10.0-inch minimum. |
| Cobalt | Battery rating is 9 hours, below the 10-hour minimum. |
| Dockside | Only 11 units are available, below the required quantity of 12. |
