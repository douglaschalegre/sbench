## Source Resolution

Source reliability rule from `01_selection_rules.md`:

- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster is baseline information, but newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

| Clinic ID | Clinic | Effective Storage Status | Controlling Source | Resolution Note |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update. |
| N-102 | Riverbend Health | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update overrides baseline and audit `conditional pass pending`. |
| N-103 | Pine Ridge Outreach | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update. |
| N-104 | Lakeside Family Care | suspended | `04_storage_update_2026-05-06.md` | Newer update overrides baseline and audit `certified`. |
| N-105 | Cedar Works Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update. |
| N-106 | Hillcrest Annex | certified | `04_storage_update_2026-05-06.md` | Newer update overrides baseline and audit `expired`. |
| N-107 | Old Mill Clinic | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms status remains not accepted for first wave. |
| S-201 | South Gate Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update. |

Archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules and were treated as context only.
