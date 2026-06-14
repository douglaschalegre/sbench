## First-Wave Budget

- Budget: `$20,000`
- Cost formula: `setup_cost` from `02_site_roster.csv` + `transport_cost` from `06_transport_quotes.csv`

## Clinic Screening Checkpoint

| Clinic ID | Clinic Name | Effective Storage Status | Coordinator Full Window | Transport Delivery Date | Total Rollout Cost | Eligible | Blocking Reason |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | `certified` | yes | 2026-06-06 | $7,400 | yes | None |
| N-102 | Riverbend Health | `certified after mitigation complete` | yes | 2026-06-07 | $6,450 | yes | None |
| N-103 | Pine Ridge Outreach | `certified` | no | 2026-06-05 | $5,500 | no | Coordinator unavailable for the full launch window due to 2026-06-12 blackout. |
| N-104 | Lakeside Family Care | `suspended` | yes | 2026-06-06 | $5,350 | no | Effective storage status `suspended` is not accepted for first-wave use. |
| N-105 | Cedar Works Clinic | `certified` | yes | 2026-06-08 | $4,100 | no | Clinic status is `closed maintenance`; delivery also misses the 2026-06-07 cutoff. |
| N-106 | Hillcrest Annex | `certified` | yes | 2026-06-07 | $4,950 | yes | None |
| N-107 | Old Mill Clinic | `conditional pass pending` | yes | 2026-06-05 | $4,100 | no | Effective storage status `conditional pass pending` is not accepted for first-wave use. |
| S-201 | South Gate Clinic | `certified` | yes | 2026-06-05 | $4,400 | no | Region is `South`, but first-wave selection is limited to `North` clinics. |

## Selected-Clinic Total Cost Calculation

- Maple Junction Clinic: `$6,200 + $1,200 = $7,400`
- Riverbend Health: `$5,500 + $950 = $6,450`
- Hillcrest Annex: `$4,100 + $850 = $4,950`
- Selected-clinic total: `$7,400 + $6,450 + $4,950 = $18,800`

Only three clinics meet all hard first-wave requirements, so all three eligible clinics are selected.
