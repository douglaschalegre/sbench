# Access Resolution

Incident: INC-4472  
Effective access being resolved: `db-prod`

Rule applied from `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source. Therefore, `access_update_2026-05-04.md` overrides the older roster snapshot in `roster_schedule.csv` (as of 2026-05-01) wherever they conflict.

| Responder | Roster access as of 2026-05-01 | Newer update on 2026-05-04 | Effective `db-prod` access status | Source used |
|---|---|---|---|---|
| Asha | active | no change listed | active | `roster_schedule.csv` |
| Ben | pending | activated on 2026-05-04 at 09:00 | active | `access_update_2026-05-04.md` |
| Carmen | active | suspended on 2026-05-04 at 10:15 | suspended | `access_update_2026-05-04.md` |
| Deepa | active | no change listed | active | `roster_schedule.csv` |
| Eli | active | no change listed | active | `roster_schedule.csv` |
| Farah | active | no change listed | active | `roster_schedule.csv` |
| Gabe | none | still not provisioned as of 2026-05-04 at 10:30 | none / not provisioned | `access_update_2026-05-04.md` |

Override note: `access_update_2026-05-04.md` supersedes older roster access values for Ben, Carmen, and Gabe; all other responders keep the roster access status because no newer change is listed for them.
