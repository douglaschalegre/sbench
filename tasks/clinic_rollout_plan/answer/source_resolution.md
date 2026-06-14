# Source Resolution

## Controlling source rule

Per `01_selection_rules.md`: when two files disagree about the same clinic eligibility field, use the newest dated source for that field. Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules. The clinic roster is baseline information, but newer storage updates control storage status where they conflict.

## Storage conflict note

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

## Effective storage status by clinic

| clinic_id | clinic_name | roster baseline | audit 2026-04-18 | newer update? | effective storage status | controlling source |
| --- | --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | none | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no conflict; no newer update) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | 2026-05-06 update says certified after mitigation complete | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | certified | none | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no conflict; no newer update) |
| N-104 | Lakeside Family Care | certified | certified | 2026-05-06 update says suspended | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | certified | none | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no conflict; no newer update) |
| N-106 | Hillcrest Annex | expired | expired | 2026-05-06 update says certified | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | 2026-05-06 update says remains conditional pass pending | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | certified | none | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no conflict; no newer update) |

## Non-controlling contextual files

Archived policy excerpts, future-wave requests, and optional add-ons do not override the current first-wave selection rules. Specifically:

- `10_archived_policy_excerpt.md` is historical context only.
- `09_future_wave_requests.md` is planning context only for later waves.
- `11_optional_addons.md` does not affect first-wave eligibility or budget calculation.
