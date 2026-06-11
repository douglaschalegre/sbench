# Source Resolution Checkpoint

## Governing rule

From `01_selection_rules.md`: when two files disagree about the same clinic eligibility field, use the newest dated source for that field. The clinic roster is the baseline, but newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls any storage-status conflict.

Archived policy excerpts, future-wave requests, and optional add-ons are planning context only and do not override the current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Roster status | Audit status | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-104 | Lakeside Family Care | certified | certified | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-106 | Hillcrest Annex | expired | expired | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
