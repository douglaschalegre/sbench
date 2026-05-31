# Staffing Assignment Checkpoint

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

Primary responder: Ben

Backup responder: Deepa

Primary choice explanation: Ben is a Database Engineer scheduled for `database` on-call from 2026-05-06 16:00 to 2026-05-07 00:00, covering the full incident window. The newest access update activates Ben's `db-prod` access as of 2026-05-04 09:00, overriding the older roster pending status. Ben is available for the full window and has only 1 active incident.

Backup choice explanation: Deepa is an SRE, is confirmed available for the full 18:00 to 22:00 window, has active `db-prod` access from the roster with no newer conflicting update, and has 0 active incidents. Backup rules do not require database on-call coverage. Among eligible backup candidates after selecting Ben as primary, Deepa is the valid different-person backup and also has the fewest active incidents.

Rejected-candidate summary:

| Responder | Reason rejected |
|---|---|
| Asha | Ineligible because she already has 2 active incidents. |
| Ben | Selected as primary; cannot also be backup because primary and backup must be different people. |
| Carmen | Ineligible because newest access update suspends `db-prod` access. |
| Eli | Ineligible because role is Incident Manager, not Database Engineer or SRE. |
| Farah | Ineligible because availability starts at 20:00, after the 18:00 incident start. |
| Gabe | Ineligible because `db-prod` access is not provisioned. |
