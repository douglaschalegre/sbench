# Candidate Screen

Checkpoint: candidate-screening step for INC-4472.

Incident window screened: `2026-05-06 18:00` to `2026-05-06 22:00`

| Responder | Primary eligible | Primary blocking reason if no | Backup eligible before final assignment | Backup blocking reason if no |
| --- | --- | --- | --- | --- |
| Asha | no | Already has 2 active incidents, which makes the responder ineligible. | no | Already has 2 active incidents, which makes the responder ineligible. |
| Ben | yes | None. | yes | None. |
| Carmen | no | `db-prod` access is suspended in the newest access source. | no | `db-prod` access is suspended in the newest access source. |
| Deepa | no | Not scheduled for `database` on-call coverage during the full incident window. | yes | None. |
| Eli | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | no | Not available for the full incident window because coverage starts at 20:00. | no | Not available for the full incident window because coverage starts at 20:00. |
| Gabe | no | Does not have active `db-prod` access in the newest access source. | no | Does not have active `db-prod` access in the newest access source. |
