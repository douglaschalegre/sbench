# Candidate Screen

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00.

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---|---|
| Asha | No | No | Already has 2 active incidents (ineligible under the 2-or-more rule); otherwise role, database coverage, availability, and access qualify. |
| Ben | Yes | Yes | — |
| Carmen | No | No | db-prod access suspended by 2026-05-04 update. |
| Deepa | No | Yes | Primary requires database on-call; Deepa is secondary coverage. Backup requirements are met. |
| Eli | No | No | Role is Incident Manager, not Database Engineer or SRE. |
| Farah | No | No | Not available for the full window; shift starts at 20:00. |
| Gabe | No | No | db-prod access is not provisioned. |

Primary eligibility requires technical role, full-window availability, active db-prod access, fewer than 2 active incidents, and database on-call coverage. Backup eligibility applies the same role, availability, access, and incident-load requirements, without the database on-call requirement.
