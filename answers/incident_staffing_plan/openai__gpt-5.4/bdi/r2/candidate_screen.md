# Candidate Screening

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00

Screening rules applied:
- Must be available for the full incident window.
- Must have active `db-prod` access from the newest applicable access source.
- Ineligible if active incidents >= 2.
- Primary: role must be `Database Engineer` or `SRE`, and candidate must be scheduled for `database` on-call coverage during the full incident window.
- Backup: role must be `Database Engineer` or `SRE`; database on-call is not required.

| Responder | Role | Full-window available? | Effective access | Active incidents | Database on-call for full window? | Primary eligible | Primary blocking reason if no | Backup eligible before final assignment | Backup blocking reason if no |
|---|---|---:|---|---:|---:|---|---|---|---|
| Asha | SRE | yes | active | 2 | yes | no | Has 2 active incidents; threshold is ineligible at 2 or more. | no | Has 2 active incidents; threshold is ineligible at 2 or more. |
| Ben | Database Engineer | yes | active | 1 | yes | yes | — | yes | — |
| Carmen | SRE | yes | suspended | 1 | yes | no | `db-prod` access is suspended in newest access source. | no | `db-prod` access is suspended in newest access source. |
| Deepa | SRE | yes | active | 0 | no (`secondary` on-call) | no | Not scheduled for `database` on-call coverage during the full window. | yes | — |
| Eli | Incident Manager | yes | active | 0 | yes | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | Database Engineer | no | active | 0 | no for full window (shift starts at 20:00) | no | Not available for the full incident window and not on database coverage for the full window. | no | Not available for the full incident window. |
| Gabe | SRE | yes | none / not provisioned | 0 | no (`secondary` on-call) | no | No active `db-prod` access in newest access source; also not on `database` on-call. | no | No active `db-prod` access in newest access source. |
