# Checkpoint 1: Source Resolution

## Controlling rule

From [01_selection_rules.md](/Users/douglas/code/masters/sbench/tasks/clinic_rollout_plan/01_selection_rules.md): use the newest dated source for a conflicting clinic eligibility field. The clinic roster is baseline data, and newer storage updates control storage status where they conflict. Files labeled archived, future wave, or optional add-ons are planning context only and do not override current first-wave rules.

## Storage conflict note

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

## Effective storage status by clinic

| Clinic ID | Clinic | Baseline / older status | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` agree; no newer change |
| N-102 | Riverbend Health | `conditional pass pending` in roster and 2026-04-18 audit | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` agree; no newer change |
| N-104 | Lakeside Family Care | `certified` in roster and 2026-04-18 audit | `suspended` | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` agree; no newer change |
| N-106 | Hillcrest Annex | `expired` in roster and 2026-04-18 audit | `certified` | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | `conditional pass pending` in roster and 2026-04-18 audit | `conditional pass pending` | `04_storage_update_2026-05-06.md` confirms no accepted change |
| S-201 | South Gate Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` agree; no newer change |

## Non-controlling context

`10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` do not override the current first-wave selection rules and budget method.
