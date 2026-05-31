# Access Resolution

## Access recency rule

Per `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source.

`access_update_2026-05-04.md` is newer than `roster_schedule.csv` and overrides older roster `db-prod` access values where it conflicts.

## Effective `db-prod` access status

| Responder | Roster access as of 2026-05-01 | Newer update | Effective access status | Source used |
|---|---|---|---|---|
| Asha | active | No change listed | active | `roster_schedule.csv` |
| Ben | pending | Activated on 2026-05-04 at 09:00, valid through 2026-06-30 | active | `access_update_2026-05-04.md` |
| Carmen | active | Suspended on 2026-05-04 at 10:15 pending rotation audit | suspended | `access_update_2026-05-04.md` |
| Deepa | active | No change listed | active | `roster_schedule.csv` |
| Eli | active | No change listed | active | `roster_schedule.csv` |
| Farah | active | No change listed | active | `roster_schedule.csv` |
| Gabe | none | Still not provisioned as of 2026-05-04 at 10:30 | none / not provisioned | `access_update_2026-05-04.md` |
