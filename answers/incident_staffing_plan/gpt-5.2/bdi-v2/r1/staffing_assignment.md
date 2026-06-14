# Staffing Assignment

## Incident
- **Incident ID:** INC-4472
- **System:** customer billing database

## Assignment window
- **2026-05-06 18:00 to 2026-05-06 22:00**

## Final assignment
- **Primary responder:** Ben (Database Engineer)
- **Backup responder:** Deepa (SRE)

## Explanation (primary)
Ben is the only responder who satisfies **all primary rules**:
- Role is **Database Engineer** (allowed).
- Scheduled for **database on-call** during the full window (16:00–00:00 covers 18:00–22:00).
- Confirmed **available for the full 18:00–22:00 window** (`availability_notes.md`).
- Has **active db-prod access** per the newest access source (`access_update_2026-05-04.md`: activated 2026-05-04 09:00).
- Has **1 active incident** (< 2).

## Explanation (backup)
Deepa is eligible as backup:
- Role is **SRE** (allowed).
- Scheduled shift **18:00–23:00** covers the full incident window.
- Confirmed available and explicitly noted can serve as backup (`availability_notes.md`).
- db-prod access is **active** (no newer changes after roster snapshot).
- Has **0 active incidents**.

## Rejected-candidate summary
- **Asha:** disqualified (already at **2 active incidents**, rule: ineligible if >=2).
- **Carmen:** disqualified (**db-prod access suspended** as of 2026-05-04).
- **Eli:** disqualified (role **Incident Manager**; not a technical responder per notes).
- **Farah:** disqualified (not available for full window; shift begins at **20:00**).
- **Gabe:** disqualified (**db-prod access not provisioned** as of 2026-05-04).

Backup tie-breakers were not needed because Deepa was the only backup-eligible candidate besides Ben (and primary/backup must be different people).
