# Access Resolution Checkpoint

Access recency rule: if access status appears in more than one dated source, use the newest dated source.

Override note: `access_update_2026-05-04.md` is newer than `roster_schedule.csv` and overrides older roster values where they conflict.

| Responder | Effective `db-prod` access status | Source used |
| --- | --- | --- |
| Asha | active | `roster_schedule.csv` (no newer change listed) |
| Ben | active | `access_update_2026-05-04.md` overrides roster `pending` |
| Carmen | suspended | `access_update_2026-05-04.md` overrides roster `active` |
| Deepa | active | `roster_schedule.csv` (no newer change listed) |
| Eli | active | `roster_schedule.csv` (no newer change listed) |
| Farah | active | `roster_schedule.csv` (no newer change listed) |
| Gabe | not provisioned | `access_update_2026-05-04.md` confirms newer status |
