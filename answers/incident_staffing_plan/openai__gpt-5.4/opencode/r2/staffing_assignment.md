## Checkpoint 3: Final Assignment

- Incident ID: `INC-4472`
- Assignment window: `2026-05-06 18:00 to 2026-05-06 22:00`
- Primary responder: `Ben`
- Backup responder: `Deepa`

### Primary Choice

`Ben` is the only responder who satisfies all primary rules: role `Database Engineer`, scheduled for `database` on-call coverage for the full window, available for the full window, active `db-prod` access after applying the 2026-05-04 access update, and fewer than 2 active incidents.

### Backup Choice

`Deepa` is eligible for backup because she is an `SRE`, available for the full incident window, has active `db-prod` access, and has 0 active incidents. Among eligible backup candidates before final assignment, `Deepa` beats `Ben` on the fewest-active-incidents tie-breaker (0 vs 1), and using `Deepa` also preserves different people for primary and backup.

### Rejected Candidate Summary

- `Asha` was rejected because she already has 2 active incidents.
- `Carmen` was rejected because the newest access update suspended `db-prod` access.
- `Eli` was rejected because the role is `Incident Manager`, not an eligible technical responder role.
- `Farah` was rejected because she is not available for the full 18:00 to 22:00 window.
- `Gabe` was rejected because the newest access update says `db-prod` access is still not provisioned, and he is not on `database` on-call for primary coverage.
