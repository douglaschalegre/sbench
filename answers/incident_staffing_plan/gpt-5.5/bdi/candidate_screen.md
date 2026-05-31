# Candidate Screening Checkpoint

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00.

Primary eligibility requires: role `Database Engineer` or `SRE`; scheduled for `database` on-call coverage during the full incident window; available for the full incident window; active `db-prod` access using the newest access source; fewer than 2 active incidents.

Backup eligibility before final assignment requires: role `Database Engineer` or `SRE`; available for the full incident window; active `db-prod` access using the newest access source; fewer than 2 active incidents. Backup does not need database on-call coverage.

| Responder | Primary eligible? | Backup eligible before final assignment? | Blocking reason when ineligible |
|---|---:|---:|---|
| Asha | no | no | Has 2 active incidents, so ineligible under the 2-or-more active incidents rule. |
| Ben | yes | yes | None. Database Engineer; database on-call covers full window; available full window; effective access active; 1 active incident. |
| Carmen | no | no | Effective `db-prod` access is suspended by the 2026-05-04 access update. |
| Deepa | no | yes | Primary blocked because on-call area is `secondary`, not `database`; otherwise available full window with active access and 0 active incidents. |
| Eli | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`; availability note says only incident manager coordination shifts. |
| Farah | no | no | Not available for the full window: availability starts at 20:00 and roster shift starts at 20:00, after the 18:00 incident start. |
| Gabe | no | no | Effective `db-prod` access is not active: still not provisioned in the 2026-05-04 access update; also not database on-call for primary. |
