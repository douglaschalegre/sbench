# Source Resolution

## Recency rule (from `requirements.md`)

If a vendor appears in more than one dated source and values conflict, use the **newest dated source** for that vendor.

## Vendor-by-vendor source resolution

### Northstar

- Stale CSV row: `vendor_quotes.csv` has a Northstar quote dated **2026-04-24** (explicitly marked as a baseline and to check for newer updates).
- Newer update: `northstar_update_2026-04-30.md` is dated **2026-04-30** and states it revises the baseline CSV quote.
- Resolution: Use the **2026-04-30** Northstar update as the effective source for screening and selection.

#### Effective Northstar terms used for screening

- Unit price: **$178**
- Available quantity: **12**
- Delivery date: **2026-05-16**
- Screen size: **10.1 inches**
- Battery rating: **11 hours**
- Rugged case status: **included**
- Warranty: **12 months**

