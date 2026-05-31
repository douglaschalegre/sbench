# Candidate Screen

Incident window (from `coverage_rules.md`): **2026-05-06 18:00 to 2026-05-06 22:00**

Screening rules applied:
- Full-window availability required. (Availability sourced from `availability_notes.md` and shift coverage in `roster_schedule.csv`.)
- Active `db-prod` access required, using newest dated access source per `answer/access_resolution.md`.
- Ineligible if `active_incidents >= 2` (from `coverage_rules.md` / `roster_schedule.csv`).
- Primary additionally requires:
  - role is `Database Engineer` or `SRE`
  - scheduled for `database` on-call coverage for the full incident window (`on_call_area == database` and shift covers window)
- Backup requires:
  - role is `Database Engineer` or `SRE`
  - full-window availability + active access + incident-load rule (no database on-call requirement)

| Responder | Primary eligible | Backup eligible (pre-assignment) | Blocking reason(s) when ineligible |
|---|---|---|---|
| Asha | no | no | Already at 2 active incidents (`active_incidents = 2`). |
| Ben | yes | yes | None. |
| Carmen | no | no | `db-prod` access is suspended as of 2026-05-04. |
| Deepa | no | yes | Primary: not scheduled for `database` on-call (`on_call_area = secondary`). |
| Eli | no | no | Role is `Incident Manager` (not `Database Engineer`/`SRE`); availability note indicates incident manager coordination shifts only. |
| Farah | no | no | Not available for full window (availability starts 20:00; shift starts 20:00). |
| Gabe | no | no | `db-prod` access not provisioned as of 2026-05-04; also not `database` on-call (`on_call_area = secondary`) for primary. |

