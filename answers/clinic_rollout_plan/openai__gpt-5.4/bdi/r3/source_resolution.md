# Source Resolution

## Controlling rules

From `01_selection_rules.md`:
- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files titled or labeled as archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster gives baseline information, but newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls any storage-status conflict.

## Effective storage status by clinic

| Clinic ID | Clinic name | Baseline / prior status | Effective storage status | Controlling source | Notes |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | Certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (consistent with roster; no newer change) | No newer storage update listed. |
| N-102 | Riverbend Health | Conditional pass pending in roster and 2026-04-18 audit | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update says temperature logger installation was verified on 2026-05-05. |
| N-103 | Pine Ridge Outreach | Certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (consistent with roster; no newer change) | No newer storage update listed. |
| N-104 | Lakeside Family Care | Certified in roster and 2026-04-18 audit | suspended | `04_storage_update_2026-05-06.md` | Newer update says compressor fault suspended certification; retest is after 2026-06-15. |
| N-105 | Cedar Works Clinic | Certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (consistent with roster; no newer change) | Storage remains certified, though clinic status is closed maintenance. |
| N-106 | Hillcrest Annex | Expired in roster and 2026-04-18 audit | certified | `04_storage_update_2026-05-06.md` | Newer update says recertification completed on 2026-05-05. |
| N-107 | Old Mill Clinic | Conditional pass pending in roster and 2026-04-18 audit | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms status remains not accepted for first-wave use. |
| S-201 | South Gate Clinic | Certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (consistent with roster; no newer change) | No newer storage update listed. |

## Non-controlling context files

Archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules. Specifically:
- `10_archived_policy_excerpt.md` is historical only.
- `09_future_wave_requests.md` is planning context only.
- `11_optional_addons.md` is not part of first-wave eligibility or budget unless later approved, which is not present here.
