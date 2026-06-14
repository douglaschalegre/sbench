# Clinic Screen

## Budget reference

- First-wave budget: **$20,000** (`07_budget_and_costs.md`)
- Rollout cost formula: **setup_cost + transport_cost**

## Screening table

| Clinic ID | Clinic name | Region | Clinic status | Effective storage status | Coordinator full-window availability | Delivery by | Total rollout cost if otherwise eligible | Eligible | Blocking reason if ineligible |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | North | open | certified | yes | 2026-06-06 | $7,400 | yes | — |
| N-102 | Riverbend Health | North | open | certified after mitigation complete | yes | 2026-06-07 | $6,450 | yes | — |
| N-103 | Pine Ridge Outreach | North | open | certified | no | 2026-06-05 | $5,500 | no | Coordinator not available for full 2026-06-10 to 2026-06-14 launch window (blackout 2026-06-12). |
| N-104 | Lakeside Family Care | North | open | suspended | yes | 2026-06-06 | $5,350 | no | Storage status suspended; not accepted for first-wave use. |
| N-105 | Cedar Works Clinic | North | closed maintenance | certified | yes | 2026-06-08 | $4,100 | no | Clinic not open for launch window; delivery also misses 2026-06-07 cutoff. |
| N-106 | Hillcrest Annex | North | open | certified | yes | 2026-06-07 | $4,950 | yes | — |
| N-107 | Old Mill Clinic | North | open | conditional pass pending | yes | 2026-06-05 | $4,200 | no | Storage status conditional pass pending; not accepted for first-wave use. |
| S-201 | South Gate Clinic | South | open | certified | yes | 2026-06-05 | $4,400 | no | Wrong region; first-wave requires North region. |

## Selected-clinic total cost calculation

Eligible clinics meeting all hard requirements:
- N-101 Maple Junction Clinic: $6,200 setup + $1,200 transport = **$7,400**
- N-102 Riverbend Health: $5,500 setup + $950 transport = **$6,450**
- N-106 Hillcrest Annex: $4,100 setup + $850 transport = **$4,950**

Selected-clinic total:
- **$7,400 + $6,450 + $4,950 = $18,800**

Budget check:
- First-wave budget: **$20,000**
- Remaining budget: **$20,000 - $18,800 = $1,200**
