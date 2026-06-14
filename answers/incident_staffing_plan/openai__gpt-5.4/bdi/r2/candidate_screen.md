# Candidate Screen

Incident window being screened: 2026-05-06 18:00 to 2026-05-06 22:00

Eligibility rules applied:
- Primary must have role `Database Engineer` or `SRE`.
- Primary must be scheduled for `database` on-call coverage during the full incident window.
- Both primary and backup must be available for the full incident window.
- Both primary and backup must have active `db-prod` access using the newest dated access source.
- Any responder with 2 or more active incidents is ineligible.
- Backup must have role `Database Engineer` or `SRE`.
- Backup does not need `database` on-call coverage before final assignment.

| Responder | Primary eligible | Primary blocking reason if no | Backup eligible before final assignment | Backup blocking reason if no |
|---|---|---|---|---|
| Asha | no | Has 2 active incidents, making responder ineligible despite matching role, on-call, availability, and active access. | no | Has 2 active incidents. |
| Ben | yes | — | yes | — |
| Carmen | no | Newest access source shows `db-prod` access suspended, so not active. | no | Newest access source shows `db-prod` access suspended. |
| Deepa | no | Not scheduled for `database` on-call coverage; on-call area is `secondary`. | yes | — |
| Eli | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | no | Not available for full incident window and not scheduled for full window because shift starts at 20:00. | no | Not available for full incident window because shift starts at 20:00. |
| Gabe | no | Not scheduled for `database` on-call coverage and does not have active `db-prod` access. | no | Does not have active `db-prod` access. |
