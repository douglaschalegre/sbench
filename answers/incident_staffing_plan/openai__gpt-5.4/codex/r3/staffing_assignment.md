# Staffing Assignment

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice: Ben is the only responder who meets every primary rule: role `Database Engineer`, `database` on-call coverage for the full window, confirmed availability, active `db-prod` access in the newest access source, and fewer than 2 active incidents.

Backup choice: Deepa is eligible for backup because she is an `SRE`, is available for the full window, has active `db-prod` access, and has 0 active incidents. She is the best backup candidate and remains distinct from the selected primary.

Rejected-candidate summary: Asha is blocked by 2 active incidents; Carmen is blocked by suspended access; Eli is blocked by role mismatch; Farah is blocked by partial availability; Gabe is blocked by missing access. Ben was backup-eligible before final assignment but could not also serve as backup once selected as primary.
