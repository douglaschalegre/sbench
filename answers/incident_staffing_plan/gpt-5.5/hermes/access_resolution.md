# Access Resolution Checkpoint

Access recency rule: if access status appears in more than one dated source, use the newest dated source.

Newest access source note: `access_update_2026-05-04.md` overrides older roster values where it conflicts. For responders not listed as changed in the update, the roster value from `roster_schedule.csv` (`db_prod_access_as_of_2026-05-01`) remains effective.

| Responder | Effective `db-prod` access | Source used |
|---|---|---|
| Asha | active | `roster_schedule.csv` as of 2026-05-01; no later change in `access_update_2026-05-04.md` |
| Ben | active | `access_update_2026-05-04.md`: activated on 2026-05-04 at 09:00, overriding roster pending status |
| Carmen | suspended | `access_update_2026-05-04.md`: suspended on 2026-05-04 at 10:15, overriding roster active status |
| Deepa | active | `roster_schedule.csv` as of 2026-05-01; no later change in `access_update_2026-05-04.md` |
| Eli | active | `roster_schedule.csv` as of 2026-05-01; no later change in `access_update_2026-05-04.md` |
| Farah | active | `roster_schedule.csv` as of 2026-05-01; no later change in `access_update_2026-05-04.md` |
| Gabe | none / not provisioned | `access_update_2026-05-04.md`: still not provisioned as of 2026-05-04 at 10:30, confirming roster none status |
