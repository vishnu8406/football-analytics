## Day 1

### Completed
- Explored competitions
- Explored matches
- Explored events
- Explored lineups

### Observations
- One events file represents one match.
- Match ID is inferred from the filename in lineups.
- Events have event-specific attributes.

### Design Decisions
- Teams will be a separate table.
- Players will be a separate table.
- Positions will be normalized into a lookup table.

### Questions
- Should event-specific attributes be split into separate tables?