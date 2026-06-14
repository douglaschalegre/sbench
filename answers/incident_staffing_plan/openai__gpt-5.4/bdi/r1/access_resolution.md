# Access Resolution

Access recency rule from `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source.

`access_update_2026-05-04.md` is newer than `roster_schedule.csv` and overrides older roster values where it conflicts.

| Responder | Roster access status as of 2026-05-01 | Effective `db-prod` access status | Source used | Notes |
|---|---|---|---|---|
| Asha | active | active | `roster_schedule.csv` | No newer change listed. |
| Ben | pending | active | `access_update_2026-05-04.md` | Newer access update says activated on 2026-05-04 at 09:00, valid through 2026-06-30. |
| Carmen | active | suspended | `access_update_2026-05-04.md` | Newer access update says suspended on 2026-05-04 at 10:15 pending rotation audit. |
| Deepa | active | active | `roster_schedule.csv` | No newer change listed. |
| Eli | active | active | `roster_schedule.csv` | No newer change listed. |
| Farah | active | active | `roster_schedule.csv` | No newer change listed. |
| Gabe | none | none / not provisioned | `access_update_2026-05-04.md` | Newer access update says still not provisioned as of 2026-05-04 at 10:30. |
