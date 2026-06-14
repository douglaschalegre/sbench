# Source Resolution

- Source reliability rule: when two files disagree about the same clinic eligibility field, use the newest dated source for that field. Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- `04_storage_update_2026-05-06.md` is newer than `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.
- Archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules.

| Clinic ID | Clinic | Baseline roster storage | Audit storage | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | certified | 02_site_roster.csv and 03_storage_audit_2026-04-18.csv (consistent) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | certified after mitigation complete | 04_storage_update_2026-05-06.md |
| N-103 | Pine Ridge Outreach | certified | certified | certified | 02_site_roster.csv and 03_storage_audit_2026-04-18.csv (consistent) |
| N-104 | Lakeside Family Care | certified | certified | suspended | 04_storage_update_2026-05-06.md |
| N-105 | Cedar Works Clinic | certified | certified | certified | 02_site_roster.csv and 03_storage_audit_2026-04-18.csv (consistent) |
| N-106 | Hillcrest Annex | expired | expired | certified | 04_storage_update_2026-05-06.md |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | conditional pass pending | 04_storage_update_2026-05-06.md |
| S-201 | South Gate Clinic | certified | certified | certified | 02_site_roster.csv and 03_storage_audit_2026-04-18.csv (consistent) |
