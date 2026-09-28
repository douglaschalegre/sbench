# db-prod Access Resolution

Access recency rule: when access appears in multiple dated sources, use the newest dated source. The 2026-05-04 `access_update_2026-05-04.md` overrides older roster values where they conflict. Since that update says no other listed responder access changed after the 2026-05-01 roster snapshot, unchanged statuses use the roster.

| Responder | Effective db-prod access | Source used |
|---|---|---|
| Asha | Active | `roster_schedule.csv` (2026-05-01); no later change reported |
| Ben | Active, activated 2026-05-04; valid through 2026-06-30 | `access_update_2026-05-04.md` |
| Carmen | Suspended pending rotation audit | `access_update_2026-05-04.md` (overrides roster active) |
| Deepa | Active | `roster_schedule.csv` (2026-05-01); no later change reported |
| Eli | Active | `roster_schedule.csv` (2026-05-01); no later change reported |
| Farah | Active | `roster_schedule.csv` (2026-05-01); no later change reported |
| Gabe | Not provisioned | `access_update_2026-05-04.md` (confirms no provisioning) |
