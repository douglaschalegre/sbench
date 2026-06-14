# Staffing Assignment

Checkpoint: final assignment step for the incident coordinator.

- Incident ID: `INC-4472`
- Assignment window: `2026-05-06 18:00` to `2026-05-06 22:00`
- Primary responder: Ben
- Backup responder: Deepa

Primary choice: Ben is the only responder who satisfies every primary rule after the 2026-05-04 access update changed Ben to active `db-prod` access. Ben is a `Database Engineer`, is on `database` on-call for the full window, is available for the full window, and has only 1 active incident.

Backup choice: Deepa is eligible for backup because Deepa is an `SRE`, is available for the full window, has active `db-prod` access, and has 0 active incidents. Ben was also backup-eligible before final assignment, but primary and backup must be different people, so Deepa is the correct backup.

Rejected-candidate summary: Asha is blocked by 2 active incidents; Carmen is blocked by suspended access in the newest access source; Eli is blocked by role; Farah is blocked by partial-window availability; Gabe is blocked by missing `db-prod` access.
