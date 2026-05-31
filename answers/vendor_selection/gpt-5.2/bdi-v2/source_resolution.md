# Source resolution (current vs stale)

## Recency rule (from `requirements.md`)
If a vendor appears in more than one dated source and values conflict, use the newest dated source for that vendor.

## Vendor-by-vendor source used

| Vendor | Source(s) present | Source dates | Current/effective source used | Why |
|---|---|---:|---|---|
| **Northstar** | `vendor_quotes.csv` row; `northstar_update_2026-04-30.md` | 2026-04-24; **2026-04-30** | **`northstar_update_2026-04-30.md`** | Newer dated vendor-specific update; explicitly supersedes CSV where conflicting. |
| Atlas | `vendor_quotes.csv` row only | 2026-04-27 | `vendor_quotes.csv` | Only source available. |
| BrightPath | `vendor_quotes.csv` row only | 2026-04-26 | `vendor_quotes.csv` | Only source available. |
| Cobalt | `vendor_quotes.csv` row only | 2026-04-25 | `vendor_quotes.csv` | Only source available. |
| Dockside | `vendor_quotes.csv` row only | 2026-04-26 | `vendor_quotes.csv` | Only source available. |

## Required dated facts (Northstar)

- **Stale Northstar CSV row**: `vendor_quotes.csv` Northstar quote dated **2026-04-24**.
- **Newer Northstar update**: `northstar_update_2026-04-30.md` with source date **2026-04-30**.

## Effective Northstar terms used for screening (from `northstar_update_2026-04-30.md`)

| Term | Effective value |
|---|---|
| Unit price (USD) | **$178** |
| Available quantity | **12** |
| Delivery date | **2026-05-16** |
| Screen size | **10.1 in** |
| Battery rating | **11 hours** |
| Rugged case included | **Yes** |
| Warranty | **12 months** |
