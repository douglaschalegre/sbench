# Source Resolution

## Checkpoint 1: Recency Rule

From `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor With Dated Source Conflict

| Vendor | Older source | Newer source | Effective source | Why |
| --- | --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` row dated 2026-04-24 | `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | Same vendor appears in two dated local sources, and the newer source must control where terms conflict. |

## Stale Northstar CSV Row

The `vendor_quotes.csv` Northstar row dated 2026-04-24 is stale because `northstar_update_2026-04-30.md` explicitly says to use the updated quote instead of the older CSV row where they conflict.

## Effective Northstar Terms Used For Screening

| Field | Effective value | Source used |
| --- | --- | --- |
| Unit price | $178 | `northstar_update_2026-04-30.md` |
| Available quantity | 12 | `northstar_update_2026-04-30.md` |
| Delivery date | 2026-05-16 | `northstar_update_2026-04-30.md` |
| Screen size | 10.1 inches | `northstar_update_2026-04-30.md` |
| Battery rating | 11 hours | `northstar_update_2026-04-30.md` |
| Rugged case status | included | `northstar_update_2026-04-30.md` |
| Warranty months | 12 | `northstar_update_2026-04-30.md` |
