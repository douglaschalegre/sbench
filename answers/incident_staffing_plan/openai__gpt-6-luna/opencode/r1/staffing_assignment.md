# Incident Staffing Assignment

- **Incident ID:** INC-4472
- **Assignment window:** 2026-05-06 18:00–22:00
- **Primary responder:** Ben
- **Backup responder:** Deepa

**Primary choice — Ben:** He is a Database Engineer scheduled for database on-call coverage throughout the window, is available for the full window, has active `db-prod` access under the 2026-05-04 update, and has only 1 active incident.

**Backup choice — Deepa:** She is an SRE with active `db-prod` access, full-window availability, and 0 active incidents. Database on-call is not required for backup. She is the eligible backup distinct from the selected primary.

**Rejected-candidate summary:** Asha is disqualified by her 2 active incidents. Carmen's access is suspended. Eli's role is Incident Manager rather than a technical responder. Farah is not available until 20:00. Gabe lacks provisioned `db-prod` access. Deepa is not eligible as primary because she is on secondary, not database, on-call coverage. Ben qualifies for both roles, but is assigned primary; the backup must be a different person.
