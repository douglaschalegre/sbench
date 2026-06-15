# Access Resolution

Access recency rule from [coverage_rules.md](/Users/douglas/code/masters/sbench/tasks/incident_staffing_plan/coverage_rules.md): if access status appears in more than one dated source, use the newest dated source.

`access_update_2026-05-04.md` overrides older roster values where it conflicts with [roster_schedule.csv](/Users/douglas/code/masters/sbench/tasks/incident_staffing_plan/roster_schedule.csv).

| Responder | Effective `db-prod` access status | Source used |
| --- | --- | --- |
| Asha | Active | `roster_schedule.csv` as of 2026-05-01; no newer change listed |
| Ben | Active | `access_update_2026-05-04.md` activated on 2026-05-04 at 09:00; overrides roster `pending` |
| Carmen | Inactive | `access_update_2026-05-04.md` suspended on 2026-05-04 at 10:15; overrides roster `active` |
| Deepa | Active | `roster_schedule.csv` as of 2026-05-01; no newer change listed |
| Eli | Active | `roster_schedule.csv` as of 2026-05-01; no newer change listed |
| Farah | Active | `roster_schedule.csv` as of 2026-05-01; no newer change listed |
| Gabe | Inactive | `access_update_2026-05-04.md` says still not provisioned as of 2026-05-04 at 10:30; confirms roster `none` |
