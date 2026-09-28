# Source resolution

## Controlling rules

Per `01_selection_rules.md` (effective 2026-05-08), when files conflict about the same clinic eligibility field, use the newest dated source for that field. The roster is baseline information, while newer storage updates control storage status where they conflict. Archived, future-wave, and optional-add-on files are planning context only; they do not override current first-wave rules.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` and therefore controls conflicting storage statuses. It reports no newer changes for the other clinics.

## Effective storage status by roster clinic

| Clinic ID | Clinic | Effective storage status | Controlling source |
| --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | No newer change; roster and 2026-04-18 audit agree. |
| N-102 | Riverbend Health | certified after mitigation complete | 2026-05-06 update: logger installation verified 2026-05-05. |
| N-103 | Pine Ridge Outreach | certified | No newer change; roster and 2026-04-18 audit agree. |
| N-104 | Lakeside Family Care | suspended | 2026-05-06 update: compressor fault; earliest retest after 2026-06-15. |
| N-105 | Cedar Works Clinic | certified | No newer storage change; roster and 2026-04-18 audit agree. Clinic closure is a separate eligibility field. |
| N-106 | Hillcrest Annex | certified | 2026-05-06 update: recertification completed 2026-05-05. |
| N-107 | Old Mill Clinic | conditional pass pending | 2026-05-06 update: repair delayed; status remains pending. |
| S-201 | South Gate Clinic | certified | No newer change; roster and 2026-04-18 audit agree. |

The archived two-clinic/lowest-transport guidance, later-wave requests, and optional add-ons do not override the current first-wave selection rules. Current rules require exactly three eligible North-region clinics and prioritize the donor anchor if eligible, then the lowest-cost other eligible clinics.
