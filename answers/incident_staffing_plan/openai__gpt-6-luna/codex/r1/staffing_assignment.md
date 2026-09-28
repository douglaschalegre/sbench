# Staffing assignment — INC-4472

**Incident ID:** INC-4472  
**Assignment window:** 2026-05-06 18:00–22:00  
**System:** Customer billing database

| Role | Responder |
|---|---|
| Primary | Ben |
| Backup | Deepa |

**Primary choice:** Ben is a Database Engineer scheduled for database on-call coverage throughout the window, available for the full window, has active `db-prod` access per the 2026-05-04 update, and has only 1 active incident. He is the sole candidate meeting all primary rules.

**Backup choice:** Deepa is an SRE with active `db-prod` access, full-window availability, and 0 active incidents. She is eligible under the backup rules and is distinct from Ben. Among backup-eligible candidates, the rules prefer the fewest active incidents; Deepa has fewer than Ben.

**Rejected-candidate summary:** Asha is already on 2 active incidents. Carmen's access was suspended in the newest update. Eli is an Incident Manager rather than a qualifying technical responder. Farah is only available from 20:00. Gabe lacks provisioned access. Deepa is not database on-call and therefore cannot be primary; Ben is selected as primary, so Ben cannot also be backup.
