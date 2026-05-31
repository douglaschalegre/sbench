# Coverage Rules

Incident ID: INC-4472

Incident window: 2026-05-06 18:00 to 2026-05-06 22:00

System: customer billing database

Choose one primary responder and one backup responder.

General rules:

- Use local files only.
- If access status appears in more than one dated source, use the newest dated source.
- A responder must be available for the full incident window.
- A responder must have active `db-prod` access as of the newest access source.
- A responder is ineligible if they already have 2 or more active incidents.
- Primary and backup must be different people.

Primary rules:

- Primary must have role `Database Engineer` or `SRE`.
- Primary must be scheduled for `database` on-call coverage during the full incident window.

Backup rules:

- Backup must have role `Database Engineer` or `SRE`.
- Backup does not need to be database on-call, but must be available for the full incident window and have active `db-prod` access.
- If more than one backup is eligible, choose the candidate with the fewest active incidents. If still tied, choose the alphabetically first name.
