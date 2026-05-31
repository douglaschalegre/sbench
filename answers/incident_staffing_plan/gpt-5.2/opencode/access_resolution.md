# Access Resolution (db-prod)

Access recency rule (from `coverage_rules.md`): If access status appears in more than one dated source, use the newest dated source.

Note: `access_update_2026-05-04.md` (source date 2026-05-04) overrides older roster values from `roster_schedule.csv` (snapshot as of 2026-05-01) where it conflicts.

| Responder | Roster `db-prod` (as of 2026-05-01) | Newest source applied | Effective `db-prod` access | Source used |
| --- | --- | --- | --- | --- |
| Asha | active | No newer change listed | active | `roster_schedule.csv` (no change in `access_update_2026-05-04.md`) |
| Ben | pending | Updated | active | `access_update_2026-05-04.md` (activated 2026-05-04 09:00; valid through 2026-06-30) |
| Carmen | active | Updated | suspended | `access_update_2026-05-04.md` (suspended 2026-05-04 10:15) |
| Deepa | active | No newer change listed | active | `roster_schedule.csv` (no change in `access_update_2026-05-04.md`) |
| Eli | active | No newer change listed | active | `roster_schedule.csv` (no change in `access_update_2026-05-04.md`) |
| Farah | active | No newer change listed | active | `roster_schedule.csv` (no change in `access_update_2026-05-04.md`) |
| Gabe | none | Updated | none (not provisioned) | `access_update_2026-05-04.md` (still not provisioned as of 2026-05-04 10:30) |
