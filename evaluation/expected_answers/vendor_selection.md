# Vendor Selection Expected Deliverables

Hidden local note. Do not place this file in any agent-facing task folder.

Expected deliverables:

## `answer/source_resolution.md`

Must identify the recency rule and resolve Northstar using `northstar_update_2026-04-30.md` instead of the stale 2026-04-24 Northstar row in `vendor_quotes.csv`.

Effective Northstar terms:

| Field | Expected value |
| --- | --- |
| Source used | `northstar_update_2026-04-30.md` |
| Unit price | `178` |
| Available quantity | `12` |
| Delivery date | `2026-05-16` |
| Screen size | `10.1` inches |
| Battery rating | `11` hours |
| Rugged case | included |
| Warranty | `12` months |

## `answer/vendor_screen.md`

Must include one row or entry per vendor with these decisions:

| Vendor | Eligible | Expected reason or calculation |
| --- | --- | --- |
| Northstar | yes | Meets all hard requirements using the 2026-04-30 update; total cost is `12 * 178 = 2136`, within the `$2,200` budget. |
| Atlas | no | Delivery on 2026-05-18 misses the 2026-05-17 need-by date. |
| BrightPath | no | Screen size is 9.7 inches, below the 10.0-inch minimum. |
| Cobalt | no | Battery rating is 9 hours, below the 10-hour minimum. |
| Dockside | no | Only 11 units are available, below the required quantity of 12. |

## `answer/purchase_recommendation.md`

Expected recommendation:

| Field | Expected value |
| --- | --- |
| Selected vendor | `Northstar` |
| Quantity | `12` |
| Unit price | `178` |
| Total cost | `2136` |
| Budget result | within `$2,200` |
| Delivery date | `2026-05-16` |

The recommendation should explain that cheaper invalid vendors were rejected because they miss hard requirements, not because of price preference.
