# Staffing Assignment

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice explanation:
Ben is a `Database Engineer`, is scheduled for `database` on-call coverage for the full window (16:00-00:00), is confirmed available, has active `db-prod` access per the newest access source (`access_update_2026-05-04.md`), and has fewer than 2 active incidents (1).

Backup choice explanation:
Deepa is an `SRE`, is confirmed available for the full window, has active `db-prod` access (no newer change after the roster snapshot), and has 0 active incidents. Deepa is not `database` on-call, but that is allowed for backup.

Short rejected-candidate summary:
- Asha: Ineligible (already has 2 active incidents).
- Carmen: Ineligible (`db-prod` access suspended in newest access update).
- Gabe: Ineligible (`db-prod` access not provisioned in newest access update).
- Farah: Ineligible (not available for full window; starts at 20:00).
- Eli: Ineligible (role is `Incident Manager`, not `SRE`/`Database Engineer`; notes indicate coordination-only).
