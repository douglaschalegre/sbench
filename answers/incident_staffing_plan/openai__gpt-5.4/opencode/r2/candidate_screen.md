## Checkpoint 2: Candidate Screening

- Incident ID: `INC-4472`
- Incident window being screened: `2026-05-06 18:00 to 2026-05-06 22:00`

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
| --- | --- | --- | --- |
| Asha | no | no | Already has 2 active incidents, which makes the responder ineligible. |
| Ben | yes | yes | None |
| Carmen | no | no | No active `db-prod` access after newest access update; access is suspended. |
| Deepa | no | yes | Not scheduled for `database` on-call coverage, so cannot be primary. |
| Eli | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | no | no | Not available for the full incident window; shift and stated availability start at 20:00. |
| Gabe | no | no | No active `db-prod` access after newest access update; also not scheduled for `database` on-call coverage for primary. |
