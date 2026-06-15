# Checkpoint 1: Source Resolution

## Controlling Rule

From [01_selection_rules.md](/Users/douglas/code/masters/sbench/tasks/clinic_rollout_plan/01_selection_rules.md): when two files disagree about the same clinic eligibility field, use the newest dated source for that field. The clinic roster is baseline only, and newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls any storage-status conflict it addresses.

Archived policy excerpts, future-wave requests, and optional add-ons are planning context only. They do not override the current first-wave selection rules.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Baseline / Older Status | Effective Storage Status | Controlling Source | Reason |
| --- | --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer storage change was listed. |
| N-102 | Riverbend Health | `conditional pass pending` | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` | Newer update verified logger installation on 2026-05-05. |
| N-103 | Pine Ridge Outreach | `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer storage change was listed. |
| N-104 | Lakeside Family Care | `certified` | `suspended` | `04_storage_update_2026-05-06.md` | Newer update reported compressor fault and suspended certification. |
| N-105 | Cedar Works Clinic | `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer storage change was listed. |
| N-106 | Hillcrest Annex | `expired` | `certified` | `04_storage_update_2026-05-06.md` | Newer update says recertification was completed on 2026-05-05. |
| N-107 | Old Mill Clinic | `conditional pass pending` | `conditional pass pending` | `04_storage_update_2026-05-06.md` | Newer update confirms repair delay and says status is not accepted for first wave. |
| S-201 | South Gate Clinic | `certified` | `certified` | `03_storage_audit_2026-04-18.csv` | No newer storage change was listed. |
