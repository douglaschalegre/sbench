# Source Resolution

## Recency Rule

From `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Northstar Source Check

- Stale CSV row: `vendor_quotes.csv` has a Northstar quote dated `2026-04-24`.
- Newer source: `northstar_update_2026-04-30.md` is dated `2026-04-30` and explicitly says to use it instead of the older CSV row where values conflict.
- Effective source used for Northstar screening: `northstar_update_2026-04-30.md`.

## Effective Northstar Terms Used

| Field | Effective value | Source |
| --- | --- | --- |
| Unit price | `$178` | `northstar_update_2026-04-30.md` |
| Available quantity | `12` | `northstar_update_2026-04-30.md` |
| Delivery date | `2026-05-16` | `northstar_update_2026-04-30.md` |
| Screen size | `10.1 inches` | `northstar_update_2026-04-30.md` |
| Battery rating | `11 hours` | `northstar_update_2026-04-30.md` |
| Rugged case status | `included` | `northstar_update_2026-04-30.md` |
| Warranty | `12 months` | `northstar_update_2026-04-30.md` |
