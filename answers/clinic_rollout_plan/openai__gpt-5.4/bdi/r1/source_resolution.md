# Source Resolution

## Controlling source rule

Per `01_selection_rules.md`, when two files disagree about the same clinic eligibility field, the newest dated source for that field controls. Files labeled archived, future wave, or optional add-ons are planning context only and do not override the current first-wave selection rules. The clinic roster is baseline information, but newer storage updates control storage status where they conflict.

## Storage conflict handling

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

## Effective storage status by clinic

| Clinic ID | Clinic | Baseline / older status | Effective storage status | Controlling source | Notes |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-102 | Riverbend Health | conditional pass pending | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update says logger installation was verified on 2026-05-05. |
| N-103 | Pine Ridge Outreach | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-104 | Lakeside Family Care | certified | suspended | `04_storage_update_2026-05-06.md` | Newer update says certification was suspended after compressor fault. |
| N-105 | Cedar Works Clinic | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |
| N-106 | Hillcrest Annex | expired | certified | `04_storage_update_2026-05-06.md` | Newer update says recertification was completed on 2026-05-05. |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms repair delay and says status is not accepted for first-wave use. |
| S-201 | South Gate Clinic | certified | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` | No newer storage change listed in the 2026-05-06 update. |

## Non-controlling context files

`10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` do not override the current first-wave selection rules. They are context only and are excluded from first-wave eligibility control.