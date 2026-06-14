# Access Resolution Checkpoint

Access recency rule: if access status appears in more than one dated source, use the newest dated source.

Note: `access_update_2026-05-04.md` overrides older `roster_schedule.csv` access values where they conflict.

| Responder | Effective `db-prod` access status | Source used |
| --- | --- | --- |
| Asha | active | `roster_schedule.csv` (no newer change listed) |
| Ben | active | `access_update_2026-05-04.md` override: activated on 2026-05-04 09:00 |
| Carmen | suspended | `access_update_2026-05-04.md` override: suspended on 2026-05-04 10:15 |
| Deepa | active | `roster_schedule.csv` (no newer change listed) |
| Eli | active | `roster_schedule.csv` (no newer change listed) |
| Farah | active | `roster_schedule.csv` (no newer change listed) |
| Gabe | not provisioned | `access_update_2026-05-04.md` override: still not provisioned as of 2026-05-04 10:30 |
