# Deliverable Contract

Create an `answer/` folder in this task folder, then create these three files inside it. The format may be Markdown tables or concise labeled sections, but the paths, filenames, and required facts must be present.

## `answer/source_resolution.md`

Record which source is current for each vendor where source dates matter.

Required facts:

- The recency rule from `requirements.md`.
- The stale Northstar row in `vendor_quotes.csv` dated 2026-04-24.
- The newer Northstar update in `northstar_update_2026-04-30.md`.
- The effective Northstar terms used for screening: unit price, available quantity, delivery date, screen size, battery rating, rugged case status, and warranty months.

## `answer/vendor_screen.md`

Screen every vendor against the hard requirements.

Required facts:

- One row or entry for each vendor in `vendor_quotes.csv`.
- For each vendor: effective source used, eligible `yes` or `no`, total cost if the vendor is otherwise eligible, and the blocking requirement when ineligible.
- Budget status for any eligible vendor.

## `answer/purchase_recommendation.md`

Write the final recommendation for the purchasing teammate.

Required facts:

- Selected vendor.
- Quantity.
- Unit price.
- Total cost calculation.
- Budget result.
- Delivery date.
- Short rejected-vendor summary.

Rules:

- Use local files only.
- Do not put the required deliverables in the task root; put them under `answer/`.
- Extra scratch files are allowed, but scoring is based on the three named deliverables under `answer/`.
