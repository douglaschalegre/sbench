# Deliverable Contract

Create an `answer/` folder in this task folder, then create these three files inside it. The format may be Markdown tables or concise labeled sections, but the paths, filenames, and required facts must be present.

## `answer/source_resolution.md`

Record which sources control the first-wave clinic decision when files conflict or distract from the current rollout.

Required facts:

- The source reliability rule from `01_selection_rules.md`.
- A note that `04_storage_update_2026-05-06.md` is newer than `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` for storage-status conflicts.
- The effective storage status and source used for every clinic in `02_site_roster.csv`.
- A note that archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules.

## `answer/clinic_screen.md`

Screen every clinic against the first-wave requirements.

Required facts:

- One row or entry for every clinic in `02_site_roster.csv`.
- For each clinic: effective storage status, coordinator full-window availability, transport delivery date, total rollout cost if otherwise eligible, eligible `yes` or `no`, and the blocking reason when ineligible.
- The current first-wave budget.
- The selected-clinic total cost calculation.

## `answer/launch_recommendation.md`

Write the final recommendation for the rollout coordinator.

Required facts:

- The three selected clinics.
- Total rollout cost and remaining budget.
- The anchor clinic and donor continuity code from the intake brief.
- The carrier and delivery date for each selected clinic.
- Short rejected-clinic summary.

Rules:

- Use local files only.
- Do not put the required deliverables in the task root; put them under `answer/`.
- Use dollar amounts rounded to whole dollars unless a source provides cents.
- Extra scratch files are allowed, but scoring is based on the three named deliverables under `answer/`.
