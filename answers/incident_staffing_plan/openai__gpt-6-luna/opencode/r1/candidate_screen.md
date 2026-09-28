# Candidate Screen

Incident window screened: **2026-05-06 18:00–22:00** (INC-4472).

“Backup eligible before final assignment” applies the backup role, full-window availability, active access, and incident-count rules before selecting the final primary/backup pair.

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---|---|
| Asha | No | No | Already has 2 active incidents, which disqualifies her. |
| Ben | Yes | Yes | — |
| Carmen | No | No | `db-prod` access is suspended per the 2026-05-04 update. |
| Deepa | No | Yes | Not scheduled for database on-call (secondary coverage); this blocks primary eligibility only. |
| Eli | No | No | Role is Incident Manager, not Database Engineer or SRE. |
| Farah | No | No | Not available for the full window: shift begins at 20:00. |
| Gabe | No | No | `db-prod` access is not provisioned per the 2026-05-04 update; also not database on-call for primary coverage. |
