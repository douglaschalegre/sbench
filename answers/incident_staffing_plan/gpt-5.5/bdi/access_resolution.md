# Access Resolution Checkpoint

Access recency rule from `coverage_rules.md`: if access status appears in more than one dated source, use the newest dated source.

Newest access source considered: `access_update_2026-05-04.md`, which is newer than `roster_schedule.csv` (`db_prod_access_as_of_2026-05-01`). It overrides older roster values where it conflicts.

| Responder | Effective `db-prod` access status | Source used |
|---|---|---|
| Asha | active | `roster_schedule.csv` as of 2026-05-01; no later change listed |
| Ben | active | `access_update_2026-05-04.md`: activated on 2026-05-04 at 09:00, valid through 2026-06-30 |
| Carmen | suspended / not active | `access_update_2026-05-04.md`: suspended on 2026-05-04 at 10:15 pending rotation audit |
| Deepa | active | `roster_schedule.csv` as of 2026-05-01; no later change listed |
| Eli | active | `roster_schedule.csv` as of 2026-05-01; no later change listed |
| Farah | active | `roster_schedule.csv` as of 2026-05-01; no later change listed |
| Gabe | not provisioned / not active | `access_update_2026-05-04.md`: still not provisioned as of 2026-05-04 at 10:30 |
