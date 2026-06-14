# Staffing Assignment

- Incident ID: INC-4472
- Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00
- Primary responder: Ben
- Backup responder: Deepa

## Primary choice
Ben is the only responder who satisfies all primary rules: role `Database Engineer`, `database` on-call coverage for the full incident window, full availability, active `db-prod` access after applying the 2026-05-04 access update, and fewer than 2 active incidents.

## Backup choice
Deepa is eligible for backup because she is an `SRE`, is available for the full incident window, has active `db-prod` access, and has 0 active incidents. Among backup-eligible candidates before final assignment, Ben and Deepa qualify; Deepa is chosen as backup because she has fewer active incidents than Ben (0 vs 1), which is the required tie-break rule before considering alphabetical order. This also keeps primary and backup as different people.

## Rejected-candidate summary
Asha is ineligible due to already having 2 active incidents. Carmen is ineligible because the newest access update suspended `db-prod` access. Eli is ineligible because the role is `Incident Manager`, not a qualifying technical responder role. Farah is ineligible because availability starts at 20:00, so the full 18:00 to 22:00 window is not covered. Gabe is ineligible because the newest access update confirms no active `db-prod` access, and Gabe is also not on `database` on-call for primary.
