# Candidate Screening Checkpoint

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00.

Rules applied: responders must be available for the full window, have active `db-prod` access after applying newest access information, and have fewer than 2 active incidents. Primary must also be role `Database Engineer` or `SRE` and scheduled for `database` on-call coverage during the full window. Backup must be role `Database Engineer` or `SRE`; database on-call is not required.

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---|---|
| Asha | no | no | Has 2 active incidents; responders with 2 or more active incidents are ineligible. |
| Ben | yes | yes | None before final assignment. |
| Carmen | no | no | Effective `db-prod` access is suspended by the 2026-05-04 access update. |
| Deepa | no | yes | Primary: on-call area is `secondary`, not `database`; backup has no blocking reason. |
| Eli | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`; notes say only serves incident manager coordination shifts. |
| Farah | no | no | Not available for the full window; shift/availability starts at 20:00 after the 18:00 incident start. |
| Gabe | no | no | Effective `db-prod` access is none / not provisioned. |

Final-assignment constraint noted separately: primary and backup must be different people, so the selected primary cannot also serve as backup.
