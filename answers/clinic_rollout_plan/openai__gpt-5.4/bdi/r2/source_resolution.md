# Source Resolution

## Controlling rules for first-wave decisions

- Per `01_selection_rules.md`: when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster provides baseline information, but newer storage updates control storage status where they conflict.
- `04_storage_update_2026-05-06.md` is newer than `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` for storage-status conflicts, so it controls those clinics' effective storage status.

## Effective storage status by clinic

| clinic_id | clinic_name | roster status | audit status | newer storage update? | effective storage status | controlling source |
| --- | --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | certified | none | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflicting update; update file says no newer change for other clinics) |
| N-102 | Riverbend Health | conditional pass pending | conditional pass pending | yes | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | certified | none | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflicting update; update file says no newer change for other clinics) |
| N-104 | Lakeside Family Care | certified | certified | yes | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | certified | none | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflicting update; update file says no newer change for other clinics) |
| N-106 | Hillcrest Annex | expired | expired | yes | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | conditional pass pending | yes | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | certified | none | certified | `02_site_roster.csv` / `03_storage_audit_2026-04-18.csv` (no newer conflicting update; update file says no newer change for other clinics) |

## Non-controlling context sources

- `10_archived_policy_excerpt.md` is archived historical context only and does not override the current rules in `01_selection_rules.md`.
- `09_future_wave_requests.md` contains later-wave requests only and does not change first-wave eligibility.
- `11_optional_addons.md` lists optional costs that are not part of first-wave eligibility or budget calculations.
