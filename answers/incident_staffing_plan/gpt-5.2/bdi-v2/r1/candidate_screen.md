# Candidate Screen

## Incident window being screened
- **INC-4472 window:** 2026-05-06 18:00 to 2026-05-06 22:00 (from `coverage_rules.md`)

## Eligibility rules applied (summary)
From `coverage_rules.md`:
- Must be **available for the full incident window**.
- Must have **active `db-prod` access** as of the **newest access source**.
- **Ineligible if active incidents >= 2**.
- Role constraints:
  - Primary: role **Database Engineer** or **SRE** AND scheduled for **database on-call** during full window.
  - Backup: role **Database Engineer** or **SRE**; does **not** need database on-call.

Availability constraints sourced from:
- Scheduled shift coverage in `roster_schedule.csv` (must cover 18:00–22:00).
- Notes in `availability_notes.md` (can further restrict availability or role intent).

Access constraints sourced from:
- Effective access status resolved in `answer/access_resolution.md` (from roster + `access_update_2026-05-04.md`).

## Screening table (all responders)

| Responder | Primary eligible? | Backup eligible (pre-assignment)? | Blocking reason(s) if ineligible (primary/backup) |
|---|---:|---:|---|
| Asha | no | no | **Active incidents = 2** (rule: ineligible if >=2), despite being SRE, database on-call, available, and db-prod active. |
| Ben | **yes** | **yes** | — (Meets: role Database Engineer; database on-call 16:00–00:00 covers window; available per notes; db-prod active per 2026-05-04 update; active incidents = 1) |
| Carmen | no | no | **db-prod access suspended** per 2026-05-04 access update (fails access rule). |
| Deepa | no | **yes** | Primary: not scheduled for **database** on-call (on_call_area = secondary). Backup: meets role (SRE), shift 18:00–23:00 covers window, available per notes, db-prod active, active incidents = 0. |
| Eli | no | no | Role is **Incident Manager** (not Database Engineer/SRE). Also noted: only serves incident manager coordination shifts. |
| Farah | no | no | Shift starts **20:00** (not available for full 18:00–22:00 window). |
| Gabe | no | no | **db-prod access none/not provisioned** per 2026-05-04 access update (fails access rule). |
