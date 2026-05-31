# Access Resolution (db-prod)

**Goal:** Determine the effective `db-prod` access status for every responder by applying the newest dated access source.

## Recency rule (from `coverage_rules.md`)
- **If access status appears in more than one dated source, use the newest dated source.**

## Override note
- `access_update_2026-05-04.md` (dated **2026-05-04**) is newer than the roster snapshot column `db_prod_access_as_of_2026-05-01` in `roster_schedule.csv` (as-of **2026-05-01**) and **overrides it wherever they conflict**.

## Effective access status by responder

| Responder | Roster access (as-of 2026-05-01) | Newest access update (2026-05-04) | Effective db-prod access | Source used for effective status |
|---|---|---|---|---|
| Asha | active | no change listed | **active** | `roster_schedule.csv` (no change after 2026-05-01 per access update) |
| Ben | pending | activated 2026-05-04 09:00 (valid through 2026-06-30) | **active** | `access_update_2026-05-04.md` overrides roster |
| Carmen | active | suspended 2026-05-04 10:15 | **suspended (inactive)** | `access_update_2026-05-04.md` overrides roster |
| Deepa | active | no change listed | **active** | `roster_schedule.csv` (no change after 2026-05-01 per access update) |
| Eli | active | no change listed | **active** | `roster_schedule.csv` (no change after 2026-05-01 per access update) |
| Farah | active | no change listed | **active** | `roster_schedule.csv` (no change after 2026-05-01 per access update) |
| Gabe | none | still not provisioned as of 2026-05-04 10:30 | **none (inactive)** | `access_update_2026-05-04.md` overrides/confirms roster |
