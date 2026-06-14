## Clinic Screen

Current first-wave budget: `$20,000`.

Rollout cost formula: `setup_cost` from `02_site_roster.csv` + `transport_cost` from `06_transport_quotes.csv`.

| Clinic ID | Clinic | Region | Status in launch window | Effective storage status | Coordinator full-window availability | Delivery by | Total rollout cost if otherwise eligible | Eligible | Blocking reason if ineligible |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | North | open | certified | yes | 2026-06-06 | $7,400 | yes |  |
| N-102 | Riverbend Health | North | open | certified after mitigation complete | yes | 2026-06-07 | $6,450 | yes |  |
| N-103 | Pine Ridge Outreach | North | open | certified | no | 2026-06-05 | $5,500 | no | Coordinator unavailable for full 2026-06-10 to 2026-06-14 launch window |
| N-104 | Lakeside Family Care | North | open | suspended | yes | 2026-06-06 | $5,350 | no | Storage status `suspended`, which is not accepted for first-wave use |
| N-105 | Cedar Works Clinic | North | closed maintenance | certified | yes | 2026-06-08 | $4,100 | no | Clinic not open for launch window; delivery also misses 2026-06-07 cutoff |
| N-106 | Hillcrest Annex | North | open | certified | yes | 2026-06-07 | $4,950 | yes |  |
| N-107 | Old Mill Clinic | North | open | conditional pass pending | yes | 2026-06-05 | $4,100 | no | Storage status `conditional pass pending`, which is not accepted for first-wave use |
| S-201 | South Gate Clinic | South | open | certified | yes | 2026-06-05 | $4,400 | no | Region is South; first wave is limited to North clinics |

Selected-clinic total cost calculation:

- Maple Junction Clinic: `$6,200 + $1,200 = $7,400`
- Riverbend Health: `$5,500 + $950 = $6,450`
- Hillcrest Annex: `$4,100 + $850 = $4,950`
- Total: `$7,400 + $6,450 + $4,950 = $18,800`

Screening result: exactly three clinics are eligible, so the first-wave selection is `N-101`, `N-102`, and `N-106`. The total stays within the `$20,000` budget.
