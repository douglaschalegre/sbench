# Candidate screening

**Incident window:** 2026-05-06 18:00–22:00

Eligibility applies the coverage rules using the resolved access statuses in `access_resolution.md`. “Backup eligible before final assignment” means eligible under the backup rules as an individual; the distinct-person constraint is applied when making the final assignment.

| Responder | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---|---|
| Asha | No | No | Has 2 active incidents (threshold is ineligible at 2+); therefore ineligible for either role. |
| Ben | Yes | Yes | — |
| Carmen | No | No | `db-prod` access is suspended in the newest access source. |
| Deepa | No | Yes | Primary: not scheduled for `database` on-call coverage (listed as `secondary`). |
| Eli | No | No | Role is Incident Manager, not Database Engineer or SRE. |
| Farah | No | No | Not available for the full window; shift and availability begin at 20:00. |
| Gabe | No | No | No active `db-prod` access (not provisioned). |

Ben is the sole primary-eligible candidate. The eligible backup pool before final assignment is Ben and Deepa; the final backup must differ from the primary.
