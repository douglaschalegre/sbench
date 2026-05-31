# Access resolution checkpoint (db-prod)

## Access recency rule
From `coverage_rules.md`: **If access status appears in more than one dated source, use the newest dated source.** Therefore `access_update_2026-05-04.md` (2026-05-04) overrides `roster_schedule.csv` (snapshot as of 2026-05-01) where they conflict.

## Effective db-prod access by responder

| Responder | Roster value (as of 2026-05-01) | Newest access source used | Effective db-prod access status | Notes |
|---|---|---|---|---|
| Asha | active | `roster_schedule.csv` | active | No newer change listed in `access_update_2026-05-04.md`. |
| Ben | pending | `access_update_2026-05-04.md` | **active** | Activated 2026-05-04 09:00 (valid through 2026-06-30). Overrides roster pending. |
| Carmen | active | `access_update_2026-05-04.md` | **suspended** | Suspended 2026-05-04 10:15 pending audit. Overrides roster active. |
| Deepa | active | `roster_schedule.csv` | active | No newer change listed in `access_update_2026-05-04.md`. |
| Eli | active | `roster_schedule.csv` | active | No newer change listed in `access_update_2026-05-04.md`. |
| Farah | active | `roster_schedule.csv` | active | No newer change listed in `access_update_2026-05-04.md`. |
| Gabe | none | `access_update_2026-05-04.md` | **none (not provisioned)** | Still not provisioned as of 2026-05-04 10:30. Confirms roster. |
