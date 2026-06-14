# Staffing Assignment

- Incident ID: INC-4472
- Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00
- Primary responder: Ben
- Backup responder: Deepa

## Primary choice
Ben is the selected primary because he is a `Database Engineer`, is scheduled for `database` on-call coverage for the full incident window, is confirmed available for the full window, has active `db-prod` access per the newest access update, and has only 1 active incident.

## Backup choice
Deepa is the selected backup because she is an `SRE`, is confirmed available for the full incident window, has active `db-prod` access, can serve as backup per the availability notes, and has 0 active incidents. Among backup-eligible candidates before final assignment, Ben and Deepa were eligible; Deepa has fewer active incidents than Ben, so she is the preferred backup candidate. Since primary and backup must be different people, Ben remains primary and Deepa is assigned backup.

## Rejected-candidate summary
- Asha: not eligible because she already has 2 active incidents.
- Carmen: not eligible because the newest access update suspended her `db-prod` access.
- Eli: not eligible because the role is `Incident Manager`, not `Database Engineer` or `SRE`, and availability is coordination-only.
- Farah: not eligible because she is not available for the full incident window and her shift starts at 20:00.
- Gabe: not eligible because the newest access update says he is still not provisioned for `db-prod` access.
