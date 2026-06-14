# Vendor Screen

Hard requirements applied from [requirements.md](/Users/douglas/code/masters/sbench/tasks/vendor_selection/requirements.md): 12 units, delivery no later than 2026-05-17, screen at least 10.0 inches, battery at least 10 hours, rugged case included, warranty at least 12 months, and total cost at or below the $2,200 budget.

| Vendor | Effective source used | Eligible | Total cost if otherwise eligible | Blocking requirement when ineligible | Budget status |
| --- | --- | --- | --- | --- | --- |
| Northstar | `northstar_update_2026-04-30.md` | yes | 12 x $178 = $2,136 | None | Within budget by $64 |
| Atlas | `vendor_quotes.csv` (2026-04-27) | no | 12 x $168 = $2,016 | Delivery date 2026-05-18 is later than the 2026-05-17 need-by date | Within budget, but fails delivery requirement |
| BrightPath | `vendor_quotes.csv` (2026-04-26) | no | 12 x $171 = $2,052 | Screen size 9.7 inches is below the 10.0-inch minimum | Within budget, but fails screen-size requirement |
| Cobalt | `vendor_quotes.csv` (2026-04-25) | no | 12 x $176 = $2,112 | Battery rating 9 hours is below the 10-hour minimum | Within budget, but fails battery requirement |
| Dockside | `vendor_quotes.csv` (2026-04-26) | no | N/A | Available quantity is 11, below the required 12 units | N/A because quantity requirement fails first |

## Result

Northstar is the only eligible vendor, and its total cost of $2,136 is within the $2,200 budget.
