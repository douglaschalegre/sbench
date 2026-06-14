# Source Resolution

## Checkpoint 1: Source Reliability Rule

From `01_selection_rules.md`:

- When two files disagree about the same clinic eligibility field, use the newest dated source for that field.
- Files titled or labeled as archived, future wave, or optional add-ons are planning context only and do not override current first-wave selection rules.
- The clinic roster gives baseline information, but newer storage updates control storage status where they conflict.

`04_storage_update_2026-05-06.md` is newer than both `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv`, so it controls any storage-status conflict for first-wave decisions.

## Effective Storage Status By Clinic

| Clinic ID | Clinic | Baseline / Older Status | Effective Storage Status | Controlling Source |
| --- | --- | --- | --- | --- |
| N-101 | Maple Junction Clinic | `certified` in roster and 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-102 | Riverbend Health | `conditional pass pending` in roster and 2026-04-18 audit | `certified after mitigation complete` | `04_storage_update_2026-05-06.md` |
| N-103 | Pine Ridge Outreach | `certified` in roster and 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-104 | Lakeside Family Care | `certified` in roster and 2026-04-18 audit | `suspended` | `04_storage_update_2026-05-06.md` |
| N-105 | Cedar Works Clinic | `certified` in roster and 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |
| N-106 | Hillcrest Annex | `expired` in roster and 2026-04-18 audit | `certified` | `04_storage_update_2026-05-06.md` |
| N-107 | Old Mill Clinic | `conditional pass pending` in roster and 2026-04-18 audit | `conditional pass pending` | `04_storage_update_2026-05-06.md` |
| S-201 | South Gate Clinic | `certified` in roster and 2026-04-18 audit | `certified` | `02_site_roster.csv` and `03_storage_audit_2026-04-18.csv` (no newer conflict noted in `04_storage_update_2026-05-06.md`) |

## Non-Controlling Context Sources

`09_future_wave_requests.md`, `10_archived_policy_excerpt.md`, and `11_optional_addons.md` are planning context only. They do not override the current first-wave selection rules in `01_selection_rules.md`, and optional add-ons are not part of first-wave eligibility or budget calculations.
