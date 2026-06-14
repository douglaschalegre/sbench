# Staffing Assignment

Incident ID: `INC-4472`

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice: Ben is the only responder who meets all primary rules: role `Database Engineer`, scheduled for full `database` on-call coverage during the window, available for the full window, under the incident-load cap, and `db-prod` access is active in the newest access source.

Backup choice: Deepa is eligible for backup because she is an `SRE`, is available for the full window, has active `db-prod` access, and has 0 active incidents. Ben was also backup-eligible before final assignment, but the backup must be different from the selected primary.

Rejected-candidate summary: Asha is over the 2-incident limit. Carmen lost eligibility because the newest access update suspended `db-prod` access. Eli is not in an allowed technical responder role. Farah is unavailable for the full window because her shift starts at 20:00. Gabe still does not have `db-prod` access and is not on `database` on-call for primary coverage.
