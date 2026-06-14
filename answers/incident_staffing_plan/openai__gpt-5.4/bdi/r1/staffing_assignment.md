# Staffing Assignment

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice explanation: Ben is the only responder who satisfies all primary rules: role `Database Engineer`, scheduled for `database` on-call coverage for the full incident window, available for the full window, active `db-prod` access after applying the newest access update, and fewer than 2 active incidents.

Backup choice explanation: Deepa is eligible for backup because she is an `SRE`, available for the full incident window, has active `db-prod` access, and has 0 active incidents. Ben was also backup-eligible before final assignment, but primary and backup must be different people, so Deepa becomes the backup.

Short rejected-candidate summary: Asha was rejected for having 2 active incidents. Carmen was rejected because newer access data suspends `db-prod` access. Eli was rejected for non-qualifying role (`Incident Manager`). Farah was rejected because she is not available for the full window. Gabe was rejected because he does not have active `db-prod` access. Deepa was not eligible for primary because she is not on `database` on-call.
