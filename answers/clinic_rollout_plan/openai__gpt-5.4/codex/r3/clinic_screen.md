# Checkpoint 2: Clinic Screening

Current first-wave budget: `$20,000`

Selected-clinic total cost calculation: Maple Junction Clinic `$7,400` + Riverbend Health `$6,450` + Hillcrest Annex `$4,950` = `$18,800`

| Clinic ID | Clinic | Effective Storage Status | Coordinator Full-Window Availability | Transport Delivery Date | Total Rollout Cost if Otherwise Eligible | Eligible | Blocking Reason |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | `certified` | `yes` | `2026-06-06` | `$7,400` | yes | None. |
| N-102 | Riverbend Health | `certified after mitigation complete` | `yes` | `2026-06-07` | `$6,450` | yes | None. |
| N-103 | Pine Ridge Outreach | `certified` | `no` | `2026-06-05` | `$5,500` | no | Coordinator Lena Torres is unavailable for the full 2026-06-10 to 2026-06-14 launch window. |
| N-104 | Lakeside Family Care | `suspended` | `yes` | `2026-06-06` | `$5,350` | no | Storage status `suspended` is not accepted for first-wave use. |
| N-105 | Cedar Works Clinic | `certified` | `yes` | `2026-06-08` | `$4,100` | no | Clinic status is `closed maintenance`, and transport also misses the 2026-06-07 cutoff. |
| N-106 | Hillcrest Annex | `certified` | `yes` | `2026-06-07` | `$4,950` | yes | None. |
| N-107 | Old Mill Clinic | `conditional pass pending` | `yes` | `2026-06-05` | `$4,100` | no | Storage status `conditional pass pending` is not accepted for first-wave use. |
| S-201 | South Gate Clinic | `certified` | `yes` | `2026-06-05` | `$4,400` | no | Region is `South`; first-wave selection is limited to North-region clinics. |

Cost basis for otherwise eligible clinics uses `setup_cost` from `02_site_roster.csv` plus `transport_cost` from `06_transport_quotes.csv`.
