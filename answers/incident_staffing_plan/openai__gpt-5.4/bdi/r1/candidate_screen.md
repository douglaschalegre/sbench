# Candidate Screen

Incident window being screened: 2026-05-06 18:00 to 2026-05-06 22:00.

Eligibility rules applied:
- Primary: must be `Database Engineer` or `SRE`, scheduled for `database` on-call coverage during the full incident window, available for the full incident window, have active `db-prod` access, and have fewer than 2 active incidents.
- Backup: must be `Database Engineer` or `SRE`, available for the full incident window, have active `db-prod` access, and have fewer than 2 active incidents. Backup does not need database on-call coverage.

| Responder | Role | Full-window availability | Database on-call for full window | Effective `db-prod` access | Active incidents | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---|---|---|---:|---|---|---|
| Asha | SRE | Yes | Yes | active | 2 | no | no | Ineligible because already assigned to 2 active incidents. |
| Ben | Database Engineer | Yes | Yes | active | 1 | yes | yes | — |
| Carmen | SRE | Yes | Yes | suspended | 1 | no | no | Ineligible because newest access source shows `db-prod` access suspended. |
| Deepa | SRE | Yes | No (`secondary`) | active | 0 | no | yes | Not primary-eligible because not scheduled for `database` on-call coverage. |
| Eli | Incident Manager | Yes, but coordination-only | Yes | active | 0 | no | no | Ineligible because role is `Incident Manager`, not `Database Engineer` or `SRE`; availability note also says coordination shifts only. |
| Farah | Database Engineer | No | No (shift starts at 20:00) | active | 0 | no | no | Ineligible because not available for the full 18:00 to 22:00 window; shift also does not cover the full window. |
| Gabe | SRE | Yes | No (`secondary`) | none / not provisioned | 0 | no | no | Ineligible because newest access source says not provisioned for `db-prod`; also not on `database` on-call for primary. |
