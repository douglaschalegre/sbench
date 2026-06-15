# Clinic Screen

## Checkpoint 2: Clinic Screening

- Current first-wave budget: `$20,000`.
- Rollout cost formula from `07_budget_and_costs.md`: `setup_cost` from `02_site_roster.csv` plus `transport_cost` from `06_transport_quotes.csv`.

| Clinic ID | Clinic | Effective storage status | Full-window coordinator availability | Delivery date | Total rollout cost | Eligible | Blocking reason |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | certified | yes | 2026-06-06 | $7,400 | yes | — |
| N-102 | Riverbend Health | certified after mitigation complete | yes | 2026-06-07 | $6,450 | yes | — |
| N-103 | Pine Ridge Outreach | certified | no | 2026-06-05 | $5,500 | no | Coordinator unavailable for the full 2026-06-10 to 2026-06-14 launch window. |
| N-104 | Lakeside Family Care | suspended | yes | 2026-06-06 | $5,350 | no | Storage status `suspended`, which is not accepted for first-wave use. |
| N-105 | Cedar Works Clinic | certified | yes | 2026-06-08 | $4,100 | no | Clinic status is `closed maintenance` during the launch window; delivery also misses the 2026-06-07 cutoff. |
| N-106 | Hillcrest Annex | certified | yes | 2026-06-07 | $4,950 | yes | — |
| N-107 | Old Mill Clinic | conditional pass pending | yes | 2026-06-05 | $4,100 | no | Storage status `conditional pass pending`, which is not accepted for first-wave use. |
| S-201 | South Gate Clinic | certified | yes | 2026-06-05 | $4,400 | no | Region is `South`; first-wave selection is limited to `North` clinics. |

### Selected-Clinic Cost Calculation

- Maple Junction Clinic: `$6,200` setup + `$1,200` transport = `$7,400`
- Riverbend Health: `$5,500` setup + `$950` transport = `$6,450`
- Hillcrest Annex: `$4,100` setup + `$850` transport = `$4,950`
- Selected-clinic total: `$7,400 + $6,450 + $4,950 = $18,800`

Exactly three clinics meet all hard requirements, so no lower-cost tie-break was needed beyond confirming those three fit within budget.
