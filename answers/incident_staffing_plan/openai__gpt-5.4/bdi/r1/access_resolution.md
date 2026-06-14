# Access Resolution

Access recency rule: if access status appears in more than one dated source, use the newest dated source. `access_update_2026-05-04.md` is newer than the roster snapshot in `roster_schedule.csv` and overrides older roster values where they conflict.

Effective `db-prod` access status for every responder:

| Responder | Roster status as of 2026-05-01 | Effective status | Source used | Notes |
|---|---|---|---|---|
| Asha | active | active | `roster_schedule.csv` | No newer change listed in `access_update_2026-05-04.md`. |
| Ben | pending | active | `access_update_2026-05-04.md` | Newer update says activated on 2026-05-04 at 09:00. |
| Carmen | active | suspended | `access_update_2026-05-04.md` | Newer update says suspended on 2026-05-04 at 10:15. |
| Deepa | active | active | `roster_schedule.csv` | No newer change listed in `access_update_2026-05-04.md`. |
| Eli | active | active | `roster_schedule.csv` | No newer change listed in `access_update_2026-05-04.md`. |
| Farah | active | active | `roster_schedule.csv` | No newer change listed in `access_update_2026-05-04.md`. |
| Gabe | none | none | `access_update_2026-05-04.md` | Newer update says still not provisioned as of 2026-05-04 at 10:30. |
