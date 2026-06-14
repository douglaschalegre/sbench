# Staffing Assignment

Incident ID: `INC-4472`

Assignment window: `2026-05-06 18:00` to `2026-05-06 22:00`

Primary responder: `Ben`

Backup responder: `Deepa`

Primary choice: Ben is the only responder who meets every primary rule after applying the newest access update. Ben is a `Database Engineer`, is scheduled for `database` on-call coverage for the full window, is confirmed available, has active `db-prod` access as of 2026-05-04, and has fewer than 2 active incidents.

Backup choice: Deepa is eligible for backup because Deepa is an `SRE`, is available for the full window, has active `db-prod` access, and has 0 active incidents. Ben was also backup-eligible before final assignment, but primary and backup must be different people, so Deepa is the best remaining eligible backup.

Rejected-candidate summary: Asha is blocked by already carrying 2 active incidents. Carmen is blocked by suspended `db-prod` access in the newest access source. Eli is blocked by role and coordination-only availability. Farah is not available for the full window. Gabe lacks active `db-prod` access and is not on `database` on-call.
