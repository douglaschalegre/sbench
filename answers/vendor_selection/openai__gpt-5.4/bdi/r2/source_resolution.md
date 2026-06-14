# Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor with conflicting dated sources

| Vendor | Older source | Newer source | Source used | Why |
|---|---|---|---|---|
| Northstar | `vendor_quotes.csv` row dated 2026-04-24 | `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | The update is newer and explicitly says to use it instead of the older CSV row where they conflict. |

## Stale Northstar row noted

The stale Northstar row in `vendor_quotes.csv` is dated **2026-04-24**.

## Effective Northstar terms used for screening

Using the newer `northstar_update_2026-04-30.md`, the effective Northstar terms are:

| Field | Effective value |
|---|---|
| Unit price | $178 |
| Available quantity | 12 |
| Delivery date | 2026-05-16 |
| Screen size | 10.1 inches |
| Battery rating | 11 hours |
| Rugged case status | included |
| Warranty months | 12 |
