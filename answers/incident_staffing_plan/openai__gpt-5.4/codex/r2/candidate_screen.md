# Candidate Screen

Checkpoint: Candidate screening completed after access resolution and before final assignment.

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00

| Responder | Primary eligible | Primary blocking reason if no | Backup eligible before final assignment | Backup blocking reason if no |
| --- | --- | --- | --- | --- |
| Asha | no | Has 2 active incidents, which makes the responder ineligible under general rules. | no | Has 2 active incidents, which makes the responder ineligible under general rules. |
| Ben | yes |  | yes |  |
| Carmen | no | `db-prod` access is suspended in the newest access source. | no | `db-prod` access is suspended in the newest access source. |
| Deepa | no | Not scheduled for `database` on-call coverage during the full incident window. | yes |  |
| Eli | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | no | Not available for the full incident window; shift and availability both start at 20:00. | no | Not available for the full incident window; shift and availability both start at 20:00. |
| Gabe | no | Not scheduled for `database` on-call coverage and does not have active `db-prod` access. | no | Does not have active `db-prod` access. |

Primary-eligible pool: Ben.

Backup-eligible pool before final assignment: Ben, Deepa.
