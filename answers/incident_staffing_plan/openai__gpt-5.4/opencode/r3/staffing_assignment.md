# Staffing Assignment

Incident ID: `INC-4472`

Assignment window: `2026-05-06 18:00` to `2026-05-06 22:00`

Primary responder: `Ben`

Backup responder: `Deepa`

Primary choice: `Ben` is the only responder who meets every primary rule after applying the newest access update: correct role, full-window availability, `database` on-call coverage, active `db-prod` access, and fewer than 2 active incidents.

Backup choice: `Deepa` is backup-eligible with the correct role, full-window availability, active `db-prod` access, and 0 active incidents. Although `Ben` was also backup-eligible before final assignment, the primary and backup must be different people.

Rejected candidate summary: `Asha` is over the active-incident limit, `Carmen` lost `db-prod` access in the newer access update, `Eli` does not have an eligible responder role, `Farah` is unavailable for the full window, and `Gabe` lacks active `db-prod` access and is not on `database` on-call.
