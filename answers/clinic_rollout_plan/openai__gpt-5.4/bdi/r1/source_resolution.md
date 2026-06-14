# Source Resolution

## Controlling rule

Per `01_selection_rules.md` (effective 2026-05-08):
- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files titled or labeled as archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster gives baseline information, but newer storage updates control storage status where they conflict.

## Storage-status conflict resolution

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls any storage-status conflicts for first-wave selection.

## Effective storage status by clinic

| clinic_id | clinic_name | baseline / prior status | effective storage status | controlling source | rationale |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (aligned with `02_site_roster.csv`; no newer change) | No conflicting newer storage update. |
| N-102 | Riverbend Health | conditional pass pending in roster and 2026-04-18 audit | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update says temperature logger installation was verified on 2026-05-05. |
| N-103 | Pine Ridge Outreach | certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (aligned with `02_site_roster.csv`; no newer change) | No conflicting newer storage update. |
| N-104 | Lakeside Family Care | certified in roster and 2026-04-18 audit | suspended | `04_storage_update_2026-05-06.md` | Newer update says compressor fault suspended certification; earliest retest is after 2026-06-15. |
| N-105 | Cedar Works Clinic | certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (aligned with `02_site_roster.csv`; no newer change) | No conflicting newer storage update. |
| N-106 | Hillcrest Annex | expired in roster and 2026-04-18 audit | certified | `04_storage_update_2026-05-06.md` | Newer update says recertification completed on 2026-05-05. |
| N-107 | Old Mill Clinic | conditional pass pending in roster and 2026-04-18 audit | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms status remains not accepted for first-wave use. |
| S-201 | South Gate Clinic | certified in roster and 2026-04-18 audit | certified | `03_storage_audit_2026-04-18.csv` (aligned with `02_site_roster.csv`; no newer change) | No conflicting newer storage update. |

## Non-controlling context sources

The following files are context only and do not override the current first-wave selection rules:
- `10_archived_policy_excerpt.md` (archived policy excerpt)
- `09_future_wave_requests.md` (future-wave requests)
- `11_optional_addons.md` (optional add-ons)

These may inform later planning, but they do not change first-wave eligibility, clinic count, or budget treatment for the current rollout.
