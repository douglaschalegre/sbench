# Access Resolution

Access recency rule: if access status appears in more than one dated source, use the newest dated source.

Override note: `access_update_2026-05-04.md` overrides older `roster_schedule.csv` values where they conflict.

| Responder | Roster access as of 2026-05-01 | Newer update | Effective `db-prod` access status | Source used |
| --- | --- | --- | --- | --- |
| Asha | active | no change listed | active | `roster_schedule.csv` |
| Ben | pending | activated on 2026-05-04 at 09:00, valid through 2026-06-30 | active | `access_update_2026-05-04.md` |
| Carmen | active | suspended on 2026-05-04 at 10:15 pending rotation audit | suspended | `access_update_2026-05-04.md` |
| Deepa | active | no change listed | active | `roster_schedule.csv` |
| Eli | active | no change listed | active | `roster_schedule.csv` |
| Farah | active | no change listed | active | `roster_schedule.csv` |
| Gabe | none | still not provisioned as of 2026-05-04 at 10:30 | none | `access_update_2026-05-04.md` |
