# Candidate screening checkpoint

Incident window being screened (from `coverage_rules.md`): **2026-05-06 18:00 to 2026-05-06 22:00**

Eligibility rules applied (from `coverage_rules.md`):
- Must be available for the full incident window.
- Must have **active** `db-prod` access per newest access source.
- Ineligible if **active_incidents >= 2**.
- **Primary**: role is `Database Engineer` or `SRE` **and** scheduled for `database` on-call coverage for the full window.
- **Backup** (pre-final-assignment): role is `Database Engineer` or `SRE`; does **not** need database on-call, but must meet availability/access/incident-count rules.

## Screening table (all responders)

| Responder | Role | On-call area | Shift covers full window? | Availability notes confirm full window? | Effective db-prod access | Active incidents | Primary eligible? | Backup eligible (pre-final)? | Blocking reason(s) if ineligible |
|---|---|---|---:|---:|---|---:|---|---|---|
| Asha | SRE | database | Yes (16:00–00:00) | Yes | active | 2 | no | no | Ineligible: already has 2 active incidents (>=2). |
| Ben | Database Engineer | database | Yes (16:00–00:00) | Yes | active (per 2026-05-04 update) | 1 | **yes** | **yes** | — |
| Carmen | SRE | database | Yes (16:00–00:00) | Yes | **suspended** (per 2026-05-04 update) | 1 | no | no | No active db-prod access (suspended). |
| Deepa | SRE | secondary | Yes (18:00–23:00) | Yes | active | 0 | no | **yes** | Not primary: not scheduled for database on-call (secondary). |
| Eli | Incident Manager | database | Yes (16:00–00:00) | (Available, but IM only) | active | 0 | no | no | Role not eligible (not Database Engineer or SRE). |
| Farah | Database Engineer | database | **No** (starts 20:00) | No (available starting 20:00 only) | active | 0 | no | no | Not available for full window; shift starts after 18:00. |
| Gabe | SRE | secondary | Yes (18:00–22:00) | Yes | none (not provisioned) | 0 | no | no | No active db-prod access (not provisioned). |
