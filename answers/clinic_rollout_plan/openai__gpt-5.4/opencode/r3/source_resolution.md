## Source Reliability Rule

- Per `01_selection_rules.md`, when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- `02_site_roster.csv` provides baseline clinic information, but `04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` for storage-status conflicts, so the newer storage update controls those conflicts.
- Archived policy excerpts, future-wave requests, and optional add-ons are planning context only and do not override the current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic Name | Baseline / Older Status | Effective Storage Status | Controlling Source | Reason |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer storage change was provided. |
| N-102 | Riverbend Health | `conditional pass pending` | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` | Newer update says logger installation was verified on 2026-05-05. |
| N-103 | Pine Ridge Outreach | `certified` | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer storage change was provided. |
| N-104 | Lakeside Family Care | `certified` | `suspended` | `04_storage_update_2026-05-06.md` | Newer update says certification was suspended after compressor fault. |
| N-105 | Cedar Works Clinic | `certified` | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer storage change was provided. |
| N-106 | Hillcrest Annex | `expired` | `certified` | `04_storage_update_2026-05-06.md` | Newer update says recertification was completed on 2026-05-05. |
| N-107 | Old Mill Clinic | `conditional pass pending` | `conditional pass pending` | `04_storage_update_2026-05-06.md` | Newer update confirms status remains pending and is not accepted for first-wave use. |
| S-201 | South Gate Clinic | `certified` | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` | No newer storage change was provided. |

## Source-Resolution Checkpoint

- Storage conflicts were resolved using the newest dated source for that field.
- `04_storage_update_2026-05-06.md` controlled clinics `N-102`, `N-104`, `N-106`, and `N-107`.
- `10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` were reviewed as context only and did not change first-wave eligibility.
