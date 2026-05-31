# Incident Staffing Plan Expected Deliverables

Hidden local note. Do not place this file in any agent-facing task folder.

Expected deliverables:

## `answer/access_resolution.md`

Must use `access_update_2026-05-04.md` over stale access values in `roster_schedule.csv` where they conflict.

Expected access statuses:

| Responder | Effective access | Source |
| --- | --- | --- |
| Asha | active | `roster_schedule.csv`, no newer change |
| Ben | active | `access_update_2026-05-04.md` activated access |
| Carmen | suspended | `access_update_2026-05-04.md` suspended access |
| Deepa | active | `roster_schedule.csv`, no newer change |
| Eli | active | `roster_schedule.csv`, no newer change |
| Farah | active | `roster_schedule.csv`, no newer change |
| Gabe | none or not provisioned | `access_update_2026-05-04.md` says still not provisioned |

## `answer/candidate_screen.md`

Must screen the incident window `2026-05-06 18:00 to 2026-05-06 22:00`.

Expected eligibility decisions before applying the final distinct-person assignment:

| Responder | Primary eligible | Backup eligible | Expected reason |
| --- | --- | --- | --- |
| Asha | no | no | Already has 2 active incidents, which reaches the assignment limit. |
| Ben | yes | yes | Database Engineer on database coverage for the full window, active `db-prod` access, available full window, and fewer than 2 active incidents. |
| Carmen | no | no | Newest access update suspends `db-prod` access. |
| Deepa | no | yes | SRE with active access and full availability, but on `secondary` coverage rather than `database` on-call coverage. |
| Eli | no | no | Incident Manager role is not eligible for technical responder assignment. |
| Farah | no | no | Available starting at 20:00 only, not for the full 18:00 to 22:00 window. |
| Gabe | no | no | No active `db-prod` access in the roster or newest access update. |

## `answer/staffing_assignment.md`

Expected assignment:

| Field | Expected value |
| --- | --- |
| Incident ID | `INC-4472` |
| Assignment window | `2026-05-06 18:00 to 2026-05-06 22:00` |
| Primary responder | `Ben` |
| Backup responder | `Deepa` |

The assignment should explain that Ben is the eligible database primary and Deepa is the eligible backup with the fewest active incidents. It should not assign the same person as primary and backup.
