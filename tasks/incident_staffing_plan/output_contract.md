# Deliverable Contract

Create an `answer/` folder in this task folder, then create these three files inside it. The format may be Markdown tables or concise labeled sections, but the paths, filenames, and required facts must be present.

## `answer/access_resolution.md`

Record the effective `db-prod` access status for every responder after applying the newest access information.

Required facts:

- The access recency rule from `coverage_rules.md`.
- One row or entry for every responder in `roster_schedule.csv`.
- For each responder: effective `db-prod` access status and source used.
- A note that `access_update_2026-05-04.md` overrides older roster values where it conflicts.

## `answer/candidate_screen.md`

Screen every responder against the primary and backup rules.

Required facts:

- One row or entry for every responder in `roster_schedule.csv`.
- For each responder: primary eligible `yes` or `no`, backup eligible before final assignment `yes` or `no`, and the blocking reason when ineligible.
- The incident window being screened.

## `answer/staffing_assignment.md`

Write the final assignment for the incident coordinator.

Required facts:

- Incident ID.
- Assignment window.
- Primary responder.
- Backup responder.
- Short explanation for the primary choice.
- Short explanation for the backup choice.
- Short rejected-candidate summary.

Rules:

- Use local files only.
- Do not put the required deliverables in the task root; put them under `answer/`.
- Primary and backup must be different people.
- Extra scratch files are allowed, but scoring is based on the three named deliverables under `answer/`.
