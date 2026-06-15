# Source Resolution

## Checkpoint 1: Source Resolution

- Source reliability rule from `01_selection_rules.md`: when two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- `04_storage_update_2026-05-06.md` is newer than `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.
- Archived policy excerpts, future-wave requests, and optional add-ons are planning context only and do not override the current first-wave selection rules.

| Clinic ID | Clinic | Baseline / older storage evidence | Newer controlling source | Effective storage status | Source used |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | Roster `certified`; 2026-04-18 audit `certified` | No newer change noted | certified | `03_storage_audit_2026-04-18.csv` |
| N-102 | Riverbend Health | Roster `conditional pass pending`; 2026-04-18 audit `conditional pass pending` | 2026-05-06 update says logger verified on 2026-05-05 | certified after mitigation complete | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | Roster `certified`; 2026-04-18 audit `certified` | No newer change noted | certified | `03_storage_audit_2026-04-18.csv` |
| N-104 | Lakeside Family Care | Roster `certified`; 2026-04-18 audit `certified` | 2026-05-06 update says certification `suspended` after compressor fault | suspended | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | Roster `certified`; 2026-04-18 audit `certified` | No newer change noted | certified | `03_storage_audit_2026-04-18.csv` |
| N-106 | Hillcrest Annex | Roster `expired`; 2026-04-18 audit `expired` | 2026-05-06 update says recertification completed on 2026-05-05 | certified | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | Roster `conditional pass pending`; 2026-04-18 audit `conditional pass pending` | 2026-05-06 update says status remains `conditional pass pending` | conditional pass pending | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | Roster `certified`; 2026-04-18 audit `certified` | No newer change noted | certified | `03_storage_audit_2026-04-18.csv` |
