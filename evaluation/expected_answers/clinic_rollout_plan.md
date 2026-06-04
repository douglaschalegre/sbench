# Clinic Rollout Plan Expected Deliverables

Hidden local note. Do not place this file in any agent-facing task folder.

Expected deliverables:

## `answer/source_resolution.md`

Must apply the source reliability rule from `01_selection_rules.md`: newest dated source controls when files conflict about the same eligibility field, and archived, future-wave, or optional add-on files do not override current first-wave rules.

Must use `04_storage_update_2026-05-06.md` over `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` where storage status conflicts.

Expected effective storage statuses:

| Clinic ID | Clinic | Effective storage status | Source |
| --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, no newer change |
| N-102 | Riverbend Health | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, no newer change |
| N-104 | Lakeside Family Care | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, no newer storage change |
| N-106 | Hillcrest Annex | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | certified | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, no newer change |

Must note that `10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` are not controlling first-wave sources.

## `answer/clinic_screen.md`

Must screen every clinic in `02_site_roster.csv`.

Expected screening decisions:

| Clinic ID | Eligible | Rollout cost if otherwise eligible | Expected reason |
| --- | --- | ---: | --- |
| N-101 | yes | `7400` | North, open, certified storage, full coordinator coverage, delivery by 2026-06-06. |
| N-102 | yes | `6450` | North, open, storage certified after mitigation complete, full coordinator coverage, delivery by 2026-06-07. |
| N-103 | no | `5500` | Coordinator is not available for the full launch window because of 2026-06-12 blackout. |
| N-104 | no | `5350` | Newest storage update suspends certification until after the launch window. |
| N-105 | no | `4100` | Clinic is closed for maintenance and transport delivery is 2026-06-08, after the cutoff. |
| N-106 | yes | `4950` | North, open, recertified storage, full coordinator coverage, delivery by 2026-06-07. |
| N-107 | no | `4100` | Newest storage update leaves conditional pass pending, which is not accepted. |
| S-201 | no | `4400` | South region, not North. |

Budget facts:

- First-wave budget is `$20,000`.
- Selected-clinic total is `7400 + 6450 + 4950 = 18800`.
- Remaining budget is `$1,200`.

## `answer/launch_recommendation.md`

Expected selected clinics:

| Clinic ID | Clinic | Carrier | Delivery by | Rollout cost |
| --- | --- | --- | --- | ---: |
| N-101 | Maple Junction Clinic | SwiftRoute | 2026-06-06 | `7400` |
| N-102 | Riverbend Health | NorthLine | 2026-06-07 | `6450` |
| N-106 | Hillcrest Annex | Valley Freight | 2026-06-07 | `4950` |

Expected final recommendation facts:

- Select exactly `N-101` Maple Junction Clinic, `N-102` Riverbend Health, and `N-106` Hillcrest Annex.
- Total rollout cost is `$18,800`.
- Remaining budget is `$1,200` from the `$20,000` first-wave budget.
- Maple Junction Clinic is the donor continuity anchor.
- The donor continuity code is `MJ-14` from `00_intake_brief.md`.
- Rejected summary should cover Pine Ridge coordinator blackout, Lakeside suspended storage, Cedar Works closure or late delivery, Old Mill pending storage repair, and South Gate wrong region.
