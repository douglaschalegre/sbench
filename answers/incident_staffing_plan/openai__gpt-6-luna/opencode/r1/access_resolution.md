# `db-prod` Access Resolution

Access recency rule: when access status appears in multiple dated sources, use the newest dated source. `access_update_2026-05-04.md` overrides older `roster_schedule.csv` values wherever they conflict. For responders not changed by the update, the roster snapshot dated 2026-05-01 remains the latest listed status.

| Responder | Effective `db-prod` access | Source used |
|---|---|---|
| Asha | Active | `roster_schedule.csv` (2026-05-01); no later change listed |
| Ben | Active; activated 2026-05-04 09:00, valid through 2026-06-30 | `access_update_2026-05-04.md` |
| Carmen | Suspended pending rotation audit (2026-05-04 10:15) | `access_update_2026-05-04.md` |
| Deepa | Active | `roster_schedule.csv` (2026-05-01); no later change listed |
| Eli | Active | `roster_schedule.csv` (2026-05-01); no later change listed |
| Farah | Active | `roster_schedule.csv` (2026-05-01); no later change listed |
| Gabe | Not provisioned as of 2026-05-04 10:30 | `access_update_2026-05-04.md` |
