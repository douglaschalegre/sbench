# Source Resolution

## Recency rule
Per `requirements.md`: **If a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.** Local files only were used.

## Vendor source determination

| Vendor | Source(s) reviewed | Current source used | Reason |
|---|---|---|---|
| Northstar | `vendor_quotes.csv` dated 2026-04-24; `northstar_update_2026-04-30.md` dated 2026-04-30 | `northstar_update_2026-04-30.md` | Newer dated source overrides the stale CSV row under the recency rule. |
| Atlas | `vendor_quotes.csv` dated 2026-04-27 | `vendor_quotes.csv` | Only local source for Atlas. |
| BrightPath | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | Only local source for BrightPath. |
| Cobalt | `vendor_quotes.csv` dated 2026-04-25 | `vendor_quotes.csv` | Only local source for Cobalt. |
| Dockside | `vendor_quotes.csv` dated 2026-04-26 | `vendor_quotes.csv` | Only local source for Dockside. |

## Northstar stale vs. current source

- Stale Northstar row in `vendor_quotes.csv` is dated **2026-04-24**.
- Newer Northstar update in `northstar_update_2026-04-30.md` is dated **2026-04-30**.
- Therefore the 2026-04-30 update is the effective source for screening Northstar.

## Effective Northstar terms used for screening

| Field | Effective value | Source |
|---|---:|---|
| Unit price | $178 | `northstar_update_2026-04-30.md` |
| Available quantity | 12 | `northstar_update_2026-04-30.md` |
| Delivery date | 2026-05-16 | `northstar_update_2026-04-30.md` |
| Screen size | 10.1 inches | `northstar_update_2026-04-30.md` |
| Battery rating | 11 hours | `northstar_update_2026-04-30.md` |
| Rugged case status | included | `northstar_update_2026-04-30.md` |
| Warranty | 12 months | `northstar_update_2026-04-30.md` |
