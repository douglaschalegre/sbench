# Source Resolution

## Controlling reliability rules

- Per `01_selection_rules.md`, when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- The clinic roster provides baseline information, but newer storage updates control storage status where they conflict.
- Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.

## Storage conflict resolution

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage status wherever those files conflict.

## Effective storage status by clinic

| Clinic ID | Clinic | Baseline / prior status | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | Roster: certified; Audit: certified | certified | `03_storage_audit_2026-04-18.csv` and consistent with `02_site_roster.csv`; no newer change listed in `04_storage_update_2026-05-06.md` |
| N-102 | Riverbend Health | Roster: conditional pass pending; Audit: conditional pass pending | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | Roster: certified; Audit: certified | certified | `03_storage_audit_2026-04-18.csv` and consistent with `02_site_roster.csv`; no newer change listed in `04_storage_update_2026-05-06.md` |
| N-104 | Lakeside Family Care | Roster: certified; Audit: certified | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | Roster: certified; Audit: certified | certified | `03_storage_audit_2026-04-18.csv` and consistent with `02_site_roster.csv`; no newer change listed in `04_storage_update_2026-05-06.md` |
| N-106 | Hillcrest Annex | Roster: expired; Audit: expired | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | Roster: conditional pass pending; Audit: conditional pass pending | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | Roster: certified; Audit: certified | certified | `03_storage_audit_2026-04-18.csv` and consistent with `02_site_roster.csv`; no newer change listed in `04_storage_update_2026-05-06.md` |

## Non-controlling context sources

- `09_future_wave_requests.md` is future-wave planning context only and does not override current first-wave rules.
- `10_archived_policy_excerpt.md` is archived context only and does not override current first-wave rules.
- `11_optional_addons.md` covers optional add-ons that do not affect first-wave eligibility or required budget calculations.
