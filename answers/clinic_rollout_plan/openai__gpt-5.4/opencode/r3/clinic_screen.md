# Clinic Screen

## Checkpoint 2: First-wave screening

- Current first-wave budget: `$20,000`.
- Per-clinic rollout cost = `setup_cost` from `02_site_roster.csv` + `transport_cost` from `06_transport_quotes.csv`.

| Clinic ID | Clinic | Effective storage status | Coordinator full-window availability | Transport delivery date | Total rollout cost if otherwise eligible | Eligible | Blocking reason when ineligible |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| N-101 | Maple Junction Clinic | `certified` | yes | 2026-06-06 | $7,400 | yes | |
| N-102 | Riverbend Health | `certified after mitigation complete` | yes | 2026-06-07 | $6,450 | yes | |
| N-103 | Pine Ridge Outreach | `certified` | no | 2026-06-05 | $5,500 | no | Coordinator unavailable for the full launch window due to 2026-06-12 blackout. |
| N-104 | Lakeside Family Care | `suspended` | yes | 2026-06-06 | $5,350 | no | Effective storage status is `suspended`, which is not accepted for first-wave use. |
| N-105 | Cedar Works Clinic | `certified` | yes | 2026-06-08 | $4,100 | no | Clinic status is `closed maintenance`, and delivery misses the 2026-06-07 cutoff. |
| N-106 | Hillcrest Annex | `certified` | yes | 2026-06-07 | $4,950 | yes | |
| N-107 | Old Mill Clinic | `conditional pass pending` | yes | 2026-06-05 | $4,100 | no | Effective storage status is `conditional pass pending`, which is not accepted for first-wave use. |
| S-201 | South Gate Clinic | `certified` | yes | 2026-06-05 | $4,400 | no | Region is `South`; first-wave selection is limited to North-region clinics. |

## Selected-clinic total cost calculation

- Maple Junction Clinic: `$6,200 + $1,200 = $7,400`
- Riverbend Health: `$5,500 + $950 = $6,450`
- Hillcrest Annex: `$4,100 + $850 = $4,950`
- Selected-clinic total: `$7,400 + $6,450 + $4,950 = $18,800`

Selection note: `01_selection_rules.md` requires exactly three clinics, includes the donor continuity anchor if eligible, and if more than three clinics are eligible chooses the anchor plus the lowest-cost eligible clinics. The only eligible clinics are `N-101`, `N-102`, and `N-106`, so all three are selected.
