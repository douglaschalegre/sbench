# Incident Staffing Assignment

- Incident ID: INC-4472
- Assignment window: 2026-05-06 18:00 to 2026-05-06 22:00
- Primary responder: Ben
- Backup responder: Deepa

Ben is a Database Engineer scheduled for database on-call across the full window, available throughout, has one active incident, and has active db-prod access confirmed by the newest update.

Deepa is an SRE with active db-prod access, full-window availability, and zero active incidents. Backup does not require database on-call coverage; among eligible backups she has the fewest active incidents (zero), so she is selected.

Rejected candidates: Asha is already carrying two active incidents; Carmen's access is suspended; Eli lacks the required technical role; Farah is only available from 20:00; Gabe has no provisioned access. Deepa is not primary-eligible because she is secondary rather than database on-call. Ben is selected as primary rather than backup because he meets the primary coverage requirement.
