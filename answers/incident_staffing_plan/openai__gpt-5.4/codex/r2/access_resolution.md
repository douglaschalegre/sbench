# Access Resolution

Checkpoint: access-resolution step for INC-4472 staffing.

Access recency rule from `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source.

Override note: `access_update_2026-05-04.md` overrides older roster values from `roster_schedule.csv` where they conflict.

| Responder | Roster access as of 2026-05-01 | Effective `db-prod` access status | Source used |
| --- | --- | --- | --- |
| Asha | active | active | `roster_schedule.csv` |
| Ben | pending | active | `access_update_2026-05-04.md` |
| Carmen | active | suspended | `access_update_2026-05-04.md` |
| Deepa | active | active | `roster_schedule.csv` |
| Eli | active | active | `roster_schedule.csv` |
| Farah | active | active | `roster_schedule.csv` |
| Gabe | none | none | `access_update_2026-05-04.md` |
