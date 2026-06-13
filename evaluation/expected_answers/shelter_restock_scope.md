# Shelter Restock Scope Control Expected Deliverables

Hidden local note. Do not place this file in any agent-facing task folder.

Expected deliverables:

## `answer/core_purchase_list.md`

Must screen every request in `02_supply_requests.csv`.

Expected request decisions:

| Request ID | Selected | Line total | Expected reason |
| --- | --- | ---: | --- |
| R-101 | yes | `480.00` | Phase 1, approved, medical category, vendor can deliver by 2026-07-01. |
| R-102 | yes | `900.00` | Phase 1, approved, shelter category, vendor can deliver by 2026-07-01. |
| R-103 | yes | `420.00` | Phase 1, approved, power category, vendor can deliver by 2026-07-01. |
| R-104 | no | `0.00` | Communications banner is outside restock categories even though phase is 1. |
| R-105 | no | `0.00` | Phase 2 media request, not approved Phase 1 restock. |
| R-106 | yes | `330.00` | Phase 1, approved, water category, vendor can deliver by 2026-07-01. |

Selected total: `480 + 900 + 420 + 330 = 2130`.

Remaining budget: `$70.00` from the `$2,200.00` budget.

## `answer/scope_control.md`

Expected scope-control facts:

- Core objective is Phase 1 North Shelter restock purchases only.
- In-scope rule requires phase `1`, approved status, category in medical/shelter/power/water, on-time vendor delivery, and fit within budget.
- Banner design is deferred or out of scope.
- Volunteer training agenda is deferred or out of scope.
- Drone battery selection is deferred or out of scope.
- Phase-two signage planning is deferred or out of scope.
- The answer should not actually design the banner, draft the training agenda, select media gear as a core item, or plan phase-two signage.

## `answer/final_restock_note.md`

Expected final summary facts:

- Select R-101 First aid refill kits, R-102 Thermal blankets, R-103 LED lanterns, and R-106 Water storage jugs.
- Total cost is `$2,130.00`.
- Remaining budget is `$70.00`.
- Exclude R-104 as communications/out of restock category and R-105 as phase-two media/requested status.
- Defer secondary communications, training, media, and phase-two planning requests.
