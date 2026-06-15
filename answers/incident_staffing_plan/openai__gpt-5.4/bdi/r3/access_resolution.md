# Access Resolution

Per `coverage_rules.md`, if access status appears in more than one dated source, the newest dated source is used. Therefore, `access_update_2026-05-04.md` overrides older roster values from `roster_schedule.csv` (snapshot as of 2026-05-01) wherever they conflict.

| Responder | Roster access as of 2026-05-01 | Newer access update? | Effective `db-prod` access status | Source used |
|---|---|---|---|---|
| Asha | active | No later change listed | active | `roster_schedule.csv` |
| Ben | pending | Activated on 2026-05-04 at 09:00 | active | `access_update_2026-05-04.md` |
| Carmen | active | Suspended on 2026-05-04 at 10:15 | suspended / not active | `access_update_2026-05-04.md` |
| Deepa | active | No later change listed | active | `roster_schedule.csv` |
| Eli | active | No later change listed | active | `roster_schedule.csv` |
| Farah | active | No later change listed | active | `roster_schedule.csv` |
| Gabe | none | Still not provisioned as of 2026-05-04 at 10:30 | none / not active | `access_update_2026-05-04.md` |

Note: `access_update_2026-05-04.md` is explicitly newer than `roster_schedule.csv` and overrides the older roster values where conflicts exist, notably for Ben, Carmen, and Gabe.
