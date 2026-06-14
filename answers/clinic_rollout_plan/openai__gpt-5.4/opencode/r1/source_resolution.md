# Checkpoint 1: Source Resolution

## Controlling Rule

- `01_selection_rules.md` says that when two files disagree about the same clinic eligibility field, the newest dated source controls that field.
- The same rules file says the clinic roster is baseline information, but newer storage updates control storage status where they conflict.
- `04_storage_update_2026-05-06.md` is newer than `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.
- `10_archived_policy_excerpt.md`, `09_future_wave_requests.md`, and `11_optional_addons.md` are context only and do not override current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Effective storage status | Source used | Resolution note |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change; audit aligns with roster baseline. |
| N-102 | Riverbend Health | certified after mitigation complete | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit `conditional pass pending`. |
| N-103 | Pine Ridge Outreach | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change; audit aligns with roster baseline. |
| N-104 | Lakeside Family Care | suspended | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit `certified`. |
| N-105 | Cedar Works Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change; audit aligns with roster baseline. |
| N-106 | Hillcrest Annex | certified | `04_storage_update_2026-05-06.md` | Newer update overrides roster and 2026-04-18 audit `expired`. |
| N-107 | Old Mill Clinic | conditional pass pending | `04_storage_update_2026-05-06.md` | Newer update confirms status remains not accepted for first-wave use. |
| S-201 | South Gate Clinic | certified | `03_storage_audit_2026-04-18.csv` | No newer storage change; audit aligns with roster baseline. |
