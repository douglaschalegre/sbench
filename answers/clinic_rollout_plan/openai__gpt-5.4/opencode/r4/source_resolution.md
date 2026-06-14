## Source Resolution

The controlling source reliability rule from `01_selection_rules.md` is: when two files disagree about the same clinic eligibility field, use the newest dated source for that field. Archived, future-wave, and optional add-on files are planning context only and do not override current first-wave selection rules.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls storage-status conflicts.

| Clinic ID | Clinic | Baseline / older storage evidence | Effective storage status | Controlling source |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-102 | Riverbend Health | `conditional pass pending` in roster; `conditional pass pending` in 2026-04-18 audit | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-104 | Lakeside Family Care | `certified` in roster; `certified` in 2026-04-18 audit | `suspended` | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |
| N-106 | Hillcrest Annex | `expired` in roster; `expired` in 2026-04-18 audit | `certified` | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | `conditional pass pending` in roster; `conditional pass pending` in 2026-04-18 audit | `conditional pass pending` | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | `certified` in roster; `certified` in 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict) |

Archived policy excerpts, future-wave requests, and optional add-ons were reviewed as context only. They do not change first-wave eligibility, storage acceptance, selection count, or budget calculations.
