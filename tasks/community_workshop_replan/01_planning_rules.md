# Planning Rules

Effective date: 2026-06-03

## Source Reliability

- Use the newest dated facility source for room availability when facility notes conflict.
- Session requirements in `02_sessions.csv` control capacity, time block, equipment, and room-trait needs.
- Room traits and base costs come from `03_room_options.csv` unless a newer facility update changes room availability.

## Hard Requirements

- Assign every session to exactly one room.
- Use rooms that are available for the session time block.
- Room capacity must be at least the session attendee count.
- If a session needs a projector, demo table, quiet room, or loading access, the assigned room must provide it.
- Total room cost must be at or below `$800`.
- Prefer the lowest-cost valid room for each session unless preserving a correct existing assignment after an update is more important.

## Replanning Rule

If a coordinator update makes part of the initial plan invalid, repair only the affected part when possible. Preserve correct assignments that still satisfy all requirements.
