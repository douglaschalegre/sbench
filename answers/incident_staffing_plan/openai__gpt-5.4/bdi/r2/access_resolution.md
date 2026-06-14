# Access Resolution

Access recency rule: if access status appears in more than one dated source, use the newest dated source. `access_update_2026-05-04.md` is newer than the roster snapshot in `roster_schedule.csv` and overrides older roster values where they conflict.

| Responder | Roster access as of 2026-05-01 | Newer access info | Effective `db-prod` access status | Source used |
|---|---|---|---|---|
| Asha | active | No change in `access_update_2026-05-04.md` | active | `roster_schedule.csv` |
| Ben | pending | Activated on 2026-05-04 at 09:00, valid through 2026-06-30 | active | `access_update_2026-05-04.md` |
| Carmen | active | Suspended on 2026-05-04 at 10:15 pending rotation audit | suspended / not active | `access_update_2026-05-04.md` |
| Deepa | active | No change in `access_update_2026-05-04.md` | active | `roster_schedule.csv` |
| Eli | active | No change in `access_update_2026-05-04.md` | active | `roster_schedule.csv` |
| Farah | active | No change in `access_update_2026-05-04.md` | active | `roster_schedule.csv` |
| Gabe | none | Still not provisioned as of 2026-05-04 at 10:30 | none / not active | `access_update_2026-05-04.md` |
