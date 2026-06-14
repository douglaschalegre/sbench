# Source Resolution

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Northstar source check

- Stale source: `vendor_quotes.csv` row for Northstar dated `2026-04-24`.
- Newer source: `northstar_update_2026-04-30.md` dated `2026-04-30`.
- Resolution: use `northstar_update_2026-04-30.md` instead of the older CSV row where values conflict.

## Effective Northstar terms used for screening

| Field | Effective value | Source used |
| --- | --- | --- |
| Unit price | `$178` | `northstar_update_2026-04-30.md` |
| Available quantity | `12` | `northstar_update_2026-04-30.md` |
| Delivery date | `2026-05-16` | `northstar_update_2026-04-30.md` |
| Screen size | `10.1 inches` | `northstar_update_2026-04-30.md` |
| Battery rating | `11 hours` | `northstar_update_2026-04-30.md` |
| Rugged case status | `included` | `northstar_update_2026-04-30.md` |
| Warranty months | `12` | `northstar_update_2026-04-30.md` |
