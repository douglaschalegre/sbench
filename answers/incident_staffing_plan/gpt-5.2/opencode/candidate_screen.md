# Candidate Screen

Incident window being screened (from `coverage_rules.md`): 2026-05-06 18:00 to 2026-05-06 22:00.

Screening rules applied (from `coverage_rules.md`):
Primary: role `Database Engineer` or `SRE`; scheduled for `database` on-call coverage during the full incident window; available for full window; active `db-prod` access per newest source; ineligible if `active_incidents >= 2`.
Backup: role `Database Engineer` or `SRE`; available for full window; active `db-prod` access per newest source; ineligible if `active_incidents >= 2`.

| Responder | Role | On-call area | Shift | Available full window? | Effective `db-prod` access | Active incidents | Primary eligible? | Backup eligible (pre-selection)? | Blocking reason(s) when ineligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Asha | SRE | database | 16:00-00:00 | yes (notes confirm) | active | 2 | no | no | Has 2 active incidents (rule: ineligible if already have 2+ active incidents). |
| Ben | Database Engineer | database | 16:00-00:00 | yes (notes confirm) | active | 1 | yes | yes |  |
| Carmen | SRE | database | 16:00-00:00 | yes (notes confirm) | suspended | 1 | no | no | `db-prod` access not active (suspended in newest access source). |
| Deepa | SRE | secondary | 18:00-23:00 | yes (notes confirm) | active | 0 | no | yes | Primary requires `database` on-call area during full window (currently `secondary`). |
| Eli | Incident Manager | database | 16:00-00:00 | no (notes: coordination only) | active | 0 | no | no | Role is not `Database Engineer` or `SRE` (and notes indicate non-technical responder). |
| Farah | Database Engineer | database | 20:00-04:00 | no (notes: starts 20:00; shift starts after 18:00) | active | 0 | no | no | Not available for full incident window (starts at 20:00). |
| Gabe | SRE | secondary | 18:00-22:00 | yes (notes say available; shift covers window) | none (not provisioned) | 0 | no | no | `db-prod` access not active (still not provisioned in newest access source). |
