# Staffing Assignment Checkpoint

Incident ID: INC-4472

Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00

## Final assignment

| Assignment | Responder |
|---|---|
| Primary responder | Ben |
| Backup responder | Deepa |

## Explanation

Primary choice: Ben is the only eligible primary responder. He is a Database Engineer, is scheduled for database on-call coverage from 2026-05-06 16:00 to 2026-05-07 00:00, is confirmed available for the full 18:00 to 22:00 window, has fewer than 2 active incidents, and has active `db-prod` access after the 2026-05-04 access update activated him.

Backup choice: Deepa is eligible for backup and is different from the primary. She is an SRE, confirmed available for the full window, has active `db-prod` access, and has 0 active incidents. Among backup-eligible candidates, she has the fewest active incidents.

## Rejected-candidate summary

- Asha: rejected because she already has 2 active incidents.
- Carmen: rejected because the newest access source suspended her `db-prod` access.
- Eli: rejected because he is an Incident Manager rather than a Database Engineer or SRE, and availability is only for coordination shifts.
- Farah: rejected because she is not available for the full incident window; she starts at 20:00.
- Gabe: rejected because the newest access source says he is still not provisioned for `db-prod` access.
- Ben was backup-eligible before final assignment, but he is assigned as primary and primary and backup must be different people.
