# Staffing Assignment

Checkpoint: Final assignment completed after access resolution and candidate screening.

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice explanation: Ben is the only responder who satisfies every primary rule: role `Database Engineer`, scheduled for `database` on-call coverage for the full window, available for the full window, fewer than 2 active incidents, and active `db-prod` access based on the newest access update from 2026-05-04.

Backup choice explanation: Deepa is eligible for backup because she is an `SRE`, is available for the full window, has active `db-prod` access, and has 0 active incidents. Ben was also backup-eligible before final assignment, but the primary and backup must be different people, so Deepa is the remaining eligible backup.

Rejected-candidate summary: Asha is blocked by having 2 active incidents. Carmen is blocked by suspended `db-prod` access in the newest access source. Eli is blocked by role mismatch. Farah is blocked by partial-window availability. Gabe is blocked by missing `db-prod` access and is not on `database` on-call coverage for primary eligibility.
