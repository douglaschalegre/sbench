# Source Resolution

## Checkpoint 1: Governing Source Rules

- Source reliability rule from `01_selection_rules.md`: when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- The clinic roster is baseline only. For storage-status conflicts, `04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls where it provides an update.
- `10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` are context only and do not override the current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Baseline/Audit Status | Effective Storage Status | Controlling Source | Reason |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` / `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update; `04_storage_update_2026-05-06.md` says no newer change is available for other clinics. |
| N-102 | Riverbend Health | `conditional pass pending` / `conditional pass pending` | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` | Newer storage update verified temperature logger installation on 2026-05-05. |
| N-103 | Pine Ridge Outreach | `certified` / `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update; `04_storage_update_2026-05-06.md` says no newer change is available for other clinics. |
| N-104 | Lakeside Family Care | `certified` / `certified` | `suspended` | `04_storage_update_2026-05-06.md` | Newer storage update reports compressor fault and suspension. |
| N-105 | Cedar Works Clinic | `certified` / `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update; `04_storage_update_2026-05-06.md` says no newer change is available for other clinics. |
| N-106 | Hillcrest Annex | `expired` / `expired` | `certified` | `04_storage_update_2026-05-06.md` | Newer storage update reports recertification completed on 2026-05-05. |
| N-107 | Old Mill Clinic | `conditional pass pending` / `conditional pass pending` | `conditional pass pending` | `04_storage_update_2026-05-06.md` | Newer storage update confirms repair delay and says the status is not accepted for first-wave use. |
| S-201 | South Gate Clinic | `certified` / `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer conflicting storage update; `04_storage_update_2026-05-06.md` says no newer change is available for other clinics. |
