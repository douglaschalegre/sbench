# Staffing Assignment

Incident ID: **INC-4472**

Assignment window: **2026-05-06 18:00 to 2026-05-06 22:00**

Primary responder: **Ben**

Backup responder: **Deepa**

Primary rationale (Ben):
- Meets primary role requirement (`Database Engineer`).
- Scheduled on `database` on-call for the full window (shift 16:00 to 00:00 covers 18:00 to 22:00).
- Confirmed available for the full window (`availability_notes.md`, updated 2026-05-03).
- Has active `db-prod` access per newest source (`access_update_2026-05-04.md`: activated 2026-05-04 09:00).
- Incident load is below the ineligibility threshold (`active_incidents = 1`).

Backup rationale (Deepa):
- Meets backup role requirement (`SRE`).
- Confirmed available for the full window and explicitly noted as able to serve as backup (`availability_notes.md`).
- Has active `db-prod` access (no newer override after roster snapshot).
- Fewest active incidents among eligible backup candidates (`active_incidents = 0`).

Rejected-candidate summary:
- Asha: ineligible due to already carrying 2 active incidents.
- Carmen: ineligible due to `db-prod` access suspended in newest access update.
- Eli: ineligible due to role (`Incident Manager`) and availability constraints (coordination shifts only).
- Farah: ineligible due to not being available for the full window (starts at 20:00).
- Gabe: ineligible due to `db-prod` access not provisioned as of 2026-05-04.

