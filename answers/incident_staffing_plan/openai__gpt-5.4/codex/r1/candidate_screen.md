# Candidate Screen

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00 for Incident `INC-4472`.

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
| --- | --- | --- | --- |
| Asha | no | no | Has 2 active incidents, which meets the ineligible threshold. |
| Ben | yes | yes | None. Full-window availability, active `db-prod` access after newest update, role is `Database Engineer`, and shift covers database on-call. |
| Carmen | no | no | `db-prod` access is suspended in the newest access source. |
| Deepa | no | yes | Not primary-eligible because scheduled on `secondary`, not `database`, on-call coverage. |
| Eli | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | no | no | Not available for the full incident window; availability and shift both start at 20:00. |
| Gabe | no | no | No active `db-prod` access; newest source says still not provisioned. |
