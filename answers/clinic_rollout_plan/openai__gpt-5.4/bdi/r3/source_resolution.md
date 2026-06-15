# Source Resolution

## Controlling rules

- Per `01_selection_rules.md` (effective 2026-05-08), when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override the current first-wave selection rules.
- For storage-status conflicts specifically, the roster is baseline only and newer storage updates control storage status.

## Storage conflict resolution

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts for first-wave decisions.

## Effective storage status by clinic

| Clinic ID | Clinic | Baseline roster status | Audit status (2026-04-18) | Newer storage update? | Effective storage status for first wave | Controlling source |
| --- | --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | No | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no conflict; no newer change noted) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | Yes | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | certified | No | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no conflict; no newer change noted) |
| N-104 | Lakeside Family Care | certified | certified | Yes | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | certified | No | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no conflict; no newer change noted) |
| N-106 | Hillcrest Annex | expired | expired | Yes | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | Yes | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | certified | No | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no conflict; no newer change noted) |

## Non-controlling context files

The following files are context only and do not override current first-wave selection rules:

- `10_archived_policy_excerpt.md`
- `09_future_wave_requests.md`
- `11_optional_addons.md`

They may explain background or later-wave planning, but they do not change first-wave eligibility, required clinic count logic, storage acceptance rules, or budget calculations.
