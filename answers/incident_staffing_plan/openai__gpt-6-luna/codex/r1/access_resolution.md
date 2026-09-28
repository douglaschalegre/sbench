# Access resolution — `db-prod`

**Recency rule:** When access status appears in multiple dated sources, use the newest dated source. `access_update_2026-05-04.md` overrides older roster values where they conflict. The update says no other listed responder access changed after the roster snapshot.

| Responder | Effective `db-prod` access | Source used |
|---|---|---|
| Asha | Active | `roster_schedule.csv` (2026-05-01 snapshot); no later change listed in `access_update_2026-05-04.md` |
| Ben | Active (activated 2026-05-04 09:00; valid through 2026-06-30) | `access_update_2026-05-04.md`, newer than roster's pending status |
| Carmen | Suspended (2026-05-04 10:15, pending rotation audit) | `access_update_2026-05-04.md`, newer than roster's active status |
| Deepa | Active | `roster_schedule.csv` (2026-05-01 snapshot); no later change listed in `access_update_2026-05-04.md` |
| Eli | Active | `roster_schedule.csv` (2026-05-01 snapshot); no later change listed in `access_update_2026-05-04.md` |
| Farah | Active | `roster_schedule.csv` (2026-05-01 snapshot); no later change listed in `access_update_2026-05-04.md` |
| Gabe | Not provisioned | `access_update_2026-05-04.md` confirms no access as of 2026-05-04 10:30; consistent with roster's `none` |
