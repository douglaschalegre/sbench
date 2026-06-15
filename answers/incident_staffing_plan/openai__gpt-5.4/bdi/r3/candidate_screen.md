# Candidate Screen

Incident window screened: 2026-05-06 18:00 to 2026-05-06 22:00

Eligibility was checked against the primary and backup rules in `coverage_rules.md`, using effective access from `answer/access_resolution.md`.

| Responder | Role | Full-window available? | Effective `db-prod` access active? | Active incidents < 2? | Database on-call for full window? | Primary eligible | Backup eligible before final assignment | Blocking reason when ineligible |
|---|---|---:|---:|---:|---:|---|---|---|
| Asha | SRE | yes | yes | no | yes | no | no | Already has 2 active incidents, making responder ineligible. |
| Ben | Database Engineer | yes | yes | yes | yes | yes | yes | — |
| Carmen | SRE | yes | no | yes | yes | no | no | `db-prod` access suspended in newest access update. |
| Deepa | SRE | yes | yes | yes | no | no | yes | Not scheduled for `database` on-call coverage, so cannot be primary. |
| Eli | Incident Manager | yes | yes | yes | yes | no | no | Role is `Incident Manager`, not `Database Engineer` or `SRE`. |
| Farah | Database Engineer | no | yes | yes | no | no | no | Not available for full incident window; shift starts at 20:00 and availability note says available starting at 20:00 only. |
| Gabe | SRE | yes | no | yes | no | no | no | `db-prod` access is not active in newest access update. |
