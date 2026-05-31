# Access Resolution (db-prod)

Access recency rule (from `coverage_rules.md`): **If access status appears in more than one dated source, use the newest dated source.**

Note: `access_update_2026-05-04.md` (source date **2026-05-04**) overrides older roster values from `roster_schedule.csv` (access snapshot **as of 2026-05-01**) where it conflicts.

| Responder | Roster `db_prod_access_as_of_2026-05-01` | Newest access source used | Effective `db-prod` access status | Evidence / resolution |
|---|---:|---|---|---|
| Asha | active | `roster_schedule.csv` | active | No change listed in `access_update_2026-05-04.md`; keep roster status. |
| Ben | pending | `access_update_2026-05-04.md` | active | Activated on **2026-05-04 09:00**, valid through **2026-06-30**. |
| Carmen | active | `access_update_2026-05-04.md` | inactive | Suspended on **2026-05-04 10:15** pending rotation audit. |
| Deepa | active | `roster_schedule.csv` | active | No change listed in `access_update_2026-05-04.md`; keep roster status. |
| Eli | active | `roster_schedule.csv` | active | No change listed in `access_update_2026-05-04.md`; keep roster status. |
| Farah | active | `roster_schedule.csv` | active | No change listed in `access_update_2026-05-04.md`; keep roster status. |
| Gabe | none | `access_update_2026-05-04.md` | inactive | Still not provisioned as of **2026-05-04 10:30**. |

