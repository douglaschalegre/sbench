# Staffing Assignment

- Incident ID: INC-4472
- Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00
- Primary responder: Ben
- Backup responder: Deepa

## Primary choice

Ben is the selected primary because he is a `Database Engineer`, is scheduled for `database` on-call coverage for the full incident window, is confirmed available for the full window, has active `db-prod` access per the newest access update dated 2026-05-04, and has only 1 active incident.

## Backup choice

Deepa is the selected backup because she is an `SRE`, is confirmed available for the full incident window, has active `db-prod` access, and has 0 active incidents. Among backup-eligible candidates before final assignment, Ben and Deepa were eligible; Deepa has fewer active incidents than Ben, so she is the required backup choice. This also keeps primary and backup as different people.

## Rejected-candidate summary

- Asha: Ineligible for both roles because she already has 2 active incidents.
- Carmen: Ineligible because newest access update shows `db-prod` access suspended.
- Eli: Ineligible because role is `Incident Manager`, not `Database Engineer` or `SRE`.
- Farah: Ineligible because not available for the full incident window.
- Gabe: Ineligible because `db-prod` access is not active in the newest access update.
- Ben was not used as backup because he was selected as primary, and primary/backup must be different people.
