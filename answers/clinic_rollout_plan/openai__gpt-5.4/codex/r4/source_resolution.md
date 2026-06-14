# Source Resolution

## Checkpoint 1: Source Reliability Rule

From `01_selection_rules.md`:

- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster provides baseline information, but newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` for storage-status conflicts, so it controls storage for any clinic it updates.

Archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Effective storage status | Controlling source | Resolution note |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-102 | Riverbend Health | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit. |
| N-103 | Pine Ridge Outreach | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-104 | Lakeside Family Care | suspended | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit. |
| N-105 | Cedar Works Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-106 | Hillcrest Annex | certified | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit. |
| N-107 | Old Mill Clinic | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms status remains not accepted for first-wave use. |
| S-201 | South Gate Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
