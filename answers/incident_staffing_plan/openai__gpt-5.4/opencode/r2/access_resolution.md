## Checkpoint 1: Access Resolution

- Access recency rule from `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source.
- `access_update_2026-05-04.md` overrides older `roster_schedule.csv` access values where they conflict.

| Responder | Roster access as of 2026-05-01 | Effective `db-prod` access | Source used |
| --- | --- | --- | --- |
| Asha | active | active | `roster_schedule.csv` (no newer change listed) |
| Ben | pending | active | `access_update_2026-05-04.md` overrides roster |
| Carmen | active | suspended | `access_update_2026-05-04.md` overrides roster |
| Deepa | active | active | `roster_schedule.csv` (no newer change listed) |
| Eli | active | active | `roster_schedule.csv` (no newer change listed) |
| Farah | active | active | `roster_schedule.csv` (no newer change listed) |
| Gabe | none | not provisioned | `access_update_2026-05-04.md` overrides roster |
