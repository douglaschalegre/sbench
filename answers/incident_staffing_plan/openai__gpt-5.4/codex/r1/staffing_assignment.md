# Staffing Assignment

Incident ID: `INC-4472`

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice: Ben is the only responder who satisfies every primary rule after applying the 2026-05-04 access update. He is a `Database Engineer`, has active `db-prod` access, is available for the full window, is on `database` on-call for the full window, and has fewer than 2 active incidents.

Backup choice: Deepa is backup-eligible with full-window availability, active `db-prod` access, an allowed technical role (`SRE`), and 0 active incidents. Ben was also backup-eligible before final assignment, but primary and backup must be different people, so the remaining eligible backup with the fewest active incidents is Deepa.

Rejected candidate summary: Asha is blocked by already carrying 2 active incidents. Carmen is blocked by suspended access in the newest access file. Eli is blocked by role mismatch. Farah is blocked by partial-window availability. Gabe is blocked by missing `db-prod` access. Ben cannot also serve as backup because primary and backup must be different people.
