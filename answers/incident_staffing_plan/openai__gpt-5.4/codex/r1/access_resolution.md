# Access Resolution

Access recency rule: if access status appears in more than one dated source, use the newest dated source. Here, [access_update_2026-05-04.md](/Users/douglas/code/masters/sbench/tasks/incident_staffing_plan/access_update_2026-05-04.md) overrides older roster values from [roster_schedule.csv](/Users/douglas/code/masters/sbench/tasks/incident_staffing_plan/roster_schedule.csv) where they conflict.

| Responder | Roster access as of 2026-05-01 | Effective `db-prod` access status | Source used |
| --- | --- | --- | --- |
| Asha | active | active | `roster_schedule.csv` (no newer change listed) |
| Ben | pending | active | `access_update_2026-05-04.md` override: activated on 2026-05-04 09:00 |
| Carmen | active | suspended | `access_update_2026-05-04.md` override: suspended on 2026-05-04 10:15 |
| Deepa | active | active | `roster_schedule.csv` (no newer change listed) |
| Eli | active | active | `roster_schedule.csv` (no newer change listed) |
| Farah | active | active | `roster_schedule.csv` (no newer change listed) |
| Gabe | none | none / not provisioned | `access_update_2026-05-04.md` confirms still not provisioned on 2026-05-04 10:30 |
