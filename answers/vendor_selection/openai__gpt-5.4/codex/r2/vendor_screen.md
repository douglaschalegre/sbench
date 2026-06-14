# Vendor Screen

Hard requirements applied from `requirements.md`: 12 units, delivery no later than `2026-05-17`, screen at least `10.0` inches, battery at least `10` hours, rugged case included, warranty at least `12` months, and total cost within the `$2,200` budget.

| Vendor | Effective source used | Eligible | Total cost if otherwise eligible | Blocking requirement when ineligible | Budget status |
| --- | --- | --- | --- | --- | --- |
| Northstar | `northstar_update_2026-04-30.md` superseding stale `vendor_quotes.csv` row dated `2026-04-24` | yes | `$2,136` (`12 x $178`) | none | within budget |
| Atlas | `vendor_quotes.csv` dated `2026-04-27` | no | `$2,016` (`12 x $168`) | Delivery date `2026-05-18` is after need-by date `2026-05-17` | within budget, but ineligible |
| BrightPath | `vendor_quotes.csv` dated `2026-04-26` | no | `$2,052` (`12 x $171`) | Screen size `9.7` inches is below `10.0` minimum | within budget, but ineligible |
| Cobalt | `vendor_quotes.csv` dated `2026-04-25` | no | `$2,112` (`12 x $176`) | Battery rating `9` hours is below `10` minimum | within budget, but ineligible |
| Dockside | `vendor_quotes.csv` dated `2026-04-26` | no | N/A | Available quantity is `11`, below required `12` units | not evaluated because quantity fails |

## Screening Checkpoint Result

- Eligible vendors: `Northstar`
- Ineligible vendors: `Atlas`, `BrightPath`, `Cobalt`, `Dockside`
- Lowest-cost eligible vendor within budget: `Northstar`
