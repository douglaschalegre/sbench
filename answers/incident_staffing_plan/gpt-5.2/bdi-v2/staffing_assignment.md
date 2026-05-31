# Final staffing assignment checkpoint

## Incident
- **Incident ID:** INC-4472
- **System:** customer billing database
- **Assignment window:** 2026-05-06 18:00 to 2026-05-06 22:00

## Assignments
- **Primary responder:** **Ben** (Database Engineer)
- **Backup responder:** **Deepa** (SRE)

## Why these choices
### Primary (Ben)
- Meets primary requirements: role is **Database Engineer** and scheduled for **database** on-call covering the full window (16:00–00:00).
- Availability confirmed for full 18:00–22:00 window (`availability_notes.md`).
- Effective `db-prod` access is **active** per newest source (`access_update_2026-05-04.md`).
- Has **1** active incident (<2), so eligible.

### Backup (Deepa)
- Meets backup requirements: role is **SRE** and available for the full window (shift 18:00–23:00; availability confirmed).
- Effective `db-prod` access is **active** (no newer change after roster snapshot).
- Tie-break not needed, but she is also the eligible candidate with the **fewest active incidents (0)**.

## Rejected-candidate summary (key disqualifiers)
- **Asha:** ineligible due to **2 active incidents** (>=2).
- **Carmen:** `db-prod` access **suspended** per 2026-05-04 update.
- **Eli:** role is **Incident Manager** (not Database Engineer/SRE).
- **Farah:** not available for full window (starts at 20:00).
- **Gabe:** no `db-prod` access (still not provisioned per 2026-05-04 update).

(Primary/backup are different people, per rules.)
