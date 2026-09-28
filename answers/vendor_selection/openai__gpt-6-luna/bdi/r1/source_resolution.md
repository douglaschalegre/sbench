# Source Resolution

The requirements' recency rule is: when a vendor appears in multiple dated sources with conflicting values, use the newest dated source for that vendor.

| Vendor | Source resolution |
|---|---|
| Northstar | The `vendor_quotes.csv` row dated 2026-04-24 is stale because a newer vendor-specific update is dated 2026-04-30. Use `northstar_update_2026-04-30.md` for screening wherever values conflict (and as the effective quote). Effective terms: unit price $178; available quantity 12; delivery 2026-05-16; screen 10.1 inches; battery 11 hours; rugged case included; warranty 12 months. |
| Atlas | `vendor_quotes.csv`, dated 2026-04-27 (no newer source found). |
| BrightPath | `vendor_quotes.csv`, dated 2026-04-26 (no newer source found). |
| Cobalt | `vendor_quotes.csv`, dated 2026-04-25 (no newer source found). |
| Dockside | `vendor_quotes.csv`, dated 2026-04-26 (no newer source found). |
