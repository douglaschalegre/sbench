# Candidate Screen

Incident window screened: **2026-05-06 18:00 to 2026-05-06 22:00**.

Primary requirements: role `Database Engineer` or `SRE`, scheduled for `database` on-call coverage for the full window, available for the full window, active `db-prod` access using newest access source, and fewer than 2 active incidents.

Backup requirements before final assignment: role `Database Engineer` or `SRE`, available for the full window, active `db-prod` access using newest access source, and fewer than 2 active incidents. Backup does not need database on-call coverage.

| Responder | Primary eligible? | Backup eligible before final assignment? | Blocking reason when ineligible |
|---|---:|---:|---|
| Asha | no | no | Already has 2 active incidents, which meets the ineligibility threshold. |
| Ben | yes | yes | None. Meets role, full-window availability, full database on-call coverage, active access, and active incident limit. |
| Carmen | no | no | `db-prod` access suspended by newer 2026-05-04 access update. |
| Deepa | no | yes | Primary: not scheduled for `database` on-call coverage; on-call area is `secondary`. Backup: no blocker. |
| Eli | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`; availability notes say he only serves incident manager coordination shifts. |
| Farah | no | no | Not available for the full incident window; available starting at 20:00 and shift starts after the 18:00 window start. |
| Gabe | no | no | Does not have active `db-prod` access; newer update says still not provisioned as of 2026-05-04 at 10:30. |
