## Staffing Assignment

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice: Ben is the only responder who satisfies all primary rules: role `Database Engineer`, scheduled for `database` on-call during the full window, available for the full window, active `db-prod` access in the newest source, and fewer than 2 active incidents.

Backup choice: Deepa is eligible for backup as an `SRE` with full-window availability, active `db-prod` access, and 0 active incidents. Among backup-eligible candidates, Deepa has fewer active incidents than Ben, so Deepa is the required backup selection.

Rejected-candidate summary: Asha is blocked by 2 active incidents. Carmen is blocked by suspended access in the newest access update. Eli is blocked by role mismatch. Farah is blocked by partial-window availability. Gabe is blocked by missing `db-prod` access. Ben was not used as backup because the primary and backup must be different people.
