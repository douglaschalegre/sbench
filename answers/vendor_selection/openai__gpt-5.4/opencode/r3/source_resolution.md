## Source Resolution Checkpoint

Recency rule from `requirements.md`: if a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

| Vendor | Source(s) reviewed | Current source used | Resolution |
| --- | --- | --- | --- |
| Northstar | `vendor_quotes.csv` dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | The CSV row is stale because the 2026-04-30 vendor-specific update is newer and explicitly says to use it instead of the older CSV row where they conflict. |
| Atlas | `vendor_quotes.csv` dated 2026-04-27 | `vendor_quotes.csv` | No newer conflicting source found. |
| BrightPath | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer conflicting source found. |
| Cobalt | `vendor_quotes.csv` dated 2026-04-25 | `vendor_quotes.csv` | No newer conflicting source found. |
| Dockside | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | No newer conflicting source found. |

### Northstar Effective Terms Used For Screening

- Stale baseline row in `vendor_quotes.csv`: dated 2026-04-24.
- Newer override source: `northstar_update_2026-04-30.md` dated 2026-04-30.
- Unit price: $178
- Available quantity: 12
- Delivery date: 2026-05-16
- Screen size: 10.1 inches
- Battery rating: 11 hours
- Rugged case: included
- Warranty: 12 months
