# Source resolution

## Recency rule

When a vendor appears in more than one dated source and the values conflict, use that vendor's newest dated source. The Northstar-specific update dated **2026-04-30** supersedes the Northstar row in `vendor_quotes.csv` dated **2026-04-24** wherever terms differ.

## Effective Northstar terms

| Term | Effective value | Source |
|---|---:|---|
| Unit price | $178 | `northstar_update_2026-04-30.md` |
| Available quantity | 12 units | `northstar_update_2026-04-30.md` |
| Delivery date | 2026-05-16 | `northstar_update_2026-04-30.md` |
| Screen size | 10.1 inches | `northstar_update_2026-04-30.md` |
| Battery rating | 11 hours | `northstar_update_2026-04-30.md` |
| Rugged case | Included | `northstar_update_2026-04-30.md` |
| Warranty | 12 months | `northstar_update_2026-04-30.md` |

The older CSV row has a unit price of $185; all other listed terms match the update. Screening and cost calculations use the updated $178 unit price and the updated source as Northstar's effective quote.
