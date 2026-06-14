# Staffing Assignment

Incident ID: `INC-4472`

Assignment window: `2026-05-06 18:00` to `2026-05-06 22:00`

Primary responder: Ben

Backup responder: Deepa

Primary choice: Ben is the only responder who satisfies all primary rules: eligible role, full-window availability, `database` on-call coverage during the full window, fewer than 2 active incidents, and active `db-prod` access after applying the newest access update.

Backup choice: Deepa satisfies the backup rules with full-window availability, active `db-prod` access, eligible role, and 0 active incidents. Ben was also backup-eligible before assignment, but backup must be different from the selected primary.

Rejected candidate summary: Asha is blocked by 2 active incidents. Carmen is blocked by suspended access. Eli is blocked by role mismatch. Farah is blocked by partial-window availability. Gabe is blocked by missing access. Deepa is not primary-eligible because she is not on `database` on-call.
