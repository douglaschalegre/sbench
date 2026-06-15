# Staffing Assignment

Incident ID: INC-4472  
Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

- Primary responder: **Ben**
- Backup responder: **Deepa**

## Why Ben is primary
Ben is eligible for the primary role because he is a `Database Engineer`, is scheduled for `database` on-call coverage for the full incident window, is confirmed available for the full window, has only 1 active incident, and his `db-prod` access is active based on the newest source `access_update_2026-05-04.md`.

## Why Deepa is backup
Deepa is eligible for backup because she is an `SRE`, is available for the full incident window, has active `db-prod` access, and has 0 active incidents. Backup does not require database on-call coverage. Among backup-eligible candidates, Deepa has fewer active incidents than Ben (0 vs 1), so she wins the backup tiebreaker. She is also different from the primary responder.

## Rejected candidate summary
- Asha: technically on database coverage and available, but ineligible because she already has 2 active incidents.
- Carmen: suspended `db-prod` access in the newest access update.
- Eli: wrong role (`Incident Manager`).
- Farah: not available for the full incident window because her shift starts at 20:00.
- Gabe: no active `db-prod` access in the newest access update.
- Ben was not assigned as backup because he is selected as primary, and primary and backup must be different people.
