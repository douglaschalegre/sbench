# Checkpoint 1: Source Resolution

## Controlling rule

From `01_selection_rules.md`:

- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- The clinic roster is baseline information, but newer storage updates control storage status where they conflict.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.

## Storage conflict note

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

## Effective storage status by clinic

| Clinic ID | Clinic | Baseline roster status | 2026-04-18 audit status | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | certified | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-104 | Lakeside Family Care | certified | certified | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | certified | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-106 | Hillcrest Annex | expired | expired | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | certified | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |

## Non-controlling context

`10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` do not override the current first-wave selection rules. They are context only.
