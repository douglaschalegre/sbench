# Source Resolution

## Recency Rule

From `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor With Conflicting Sources

### Northstar

- Older source: `vendor_quotes.csv`
- Older source date: `2026-04-24`
- Older row status: stale because a newer dated vendor-specific update exists
- Newer source: `northstar_update_2026-04-30.md`
- Newer source date: `2026-04-30`
- Resolution: use the newer `northstar_update_2026-04-30.md` terms instead of the stale `vendor_quotes.csv` row where they conflict

## Effective Northstar Terms Used For Screening

| Field | Effective value | Source used |
| --- | --- | --- |
| Unit price | `$178` | `northstar_update_2026-04-30.md` |
| Available quantity | `12` | `northstar_update_2026-04-30.md` |
| Delivery date | `2026-05-16` | `northstar_update_2026-04-30.md` |
| Screen size | `10.1 inches` | `northstar_update_2026-04-30.md` |
| Battery rating | `11 hours` | `northstar_update_2026-04-30.md` |
| Rugged case status | `included` | `northstar_update_2026-04-30.md` |
| Warranty months | `12` | `northstar_update_2026-04-30.md` |
