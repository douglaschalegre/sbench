# Staffing Assignment

## Final assignment

- Incident ID: **INC-4472**
- Assignment window: **2026-05-06 18:00 to 2026-05-06 22:00**
- Primary responder: **Ben**
- Backup responder: **Deepa**

## Primary choice explanation

Ben is the only primary-eligible responder. He is a `Database Engineer`, is scheduled for `database` on-call coverage from 2026-05-06 16:00 to 2026-05-07 00:00, is confirmed available for the full 18:00 to 22:00 incident window, has active `db-prod` access under the newer 2026-05-04 access update, and has only 1 active incident.

## Backup choice explanation

Deepa is backup-eligible and is the best backup choice. She is an `SRE`, confirmed available for the full incident window, has active `db-prod` access, and has 0 active incidents. Ben is also backup-eligible before final assignment, but the primary and backup must be different people; Deepa also has fewer active incidents than Ben.

## Rejected-candidate summary

- Asha: rejected because she already has 2 active incidents.
- Carmen: rejected because newer access information shows her `db-prod` access is suspended.
- Eli: rejected because he is an `Incident Manager`, not a `Database Engineer` or `SRE`, and only serves incident manager coordination shifts.
- Farah: rejected because she is not available for the full 18:00 to 22:00 window.
- Gabe: rejected because he does not have active `db-prod` access; newer access update says he is still not provisioned.

Ben is assigned primary and Deepa is assigned backup, satisfying the rule that the two assignments must be different people.
