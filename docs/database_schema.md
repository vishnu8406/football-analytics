## Table : Competition

Purpose:
Stores information about football competitions.

Primary Key:
competition_id

Foreign Keys:
None

Referenced By:
Matches

Columns:
competition_id
competition_name
country_name
competition_gender
competition_youth
competition_international

Relationships:
One Competition → Many Matches

Notes:
Contains metadata about each competition.
## Table : Season
Purpose:
Stores season information for each competition.

Primary Key:
season_id

Foreign Keys:
competition_id

Referenced By:
Matches

Columns:
season_id
competition_id
season_name

Relationships:
One Competition → Many Seasons
One Season → Many Matches

Notes:
Separating seasons avoids repeating season information.
## Table : Teams
Purpose:
Stores unique information about football teams.

Primary Key:
team_id

Foreign Keys:
None

Referenced By:
Matches
Events
Lineups

Columns:
team_id
team_name

Relationships:
One Team → Many Matches
One Team → Many Events
One Team → Many Lineups

Notes:
Eliminates duplicate team names throughout the database.
## Table : Players
Purpose:
Stores unique information about football players.

Primary Key:
player_id

Foreign Keys:
None

Referenced By:
Events
Lineups

Columns:
player_id
player_name
player_nickname

Relationships:
One Player → Many Events
One Player → Many Lineups

Notes:
Stores player information only once.
## Table : Matchs
Purpose:
Stores information about individual football matches.

Primary Key:
match_id

Foreign Keys:
competition_id
season_id
home_team_id
away_team_id
stadium_id
referee_id

Referenced By:
Events
Lineups

Columns:
match_id
competition_id
season_id
match_date
kick_off
home_team_id
away_team_id
home_score
away_score
stadium_id
referee_id

Relationships:
One Match → Many Events
One Match → Many Lineups

Notes:
Acts as the central table connecting competitions, teams and events.

## Table: lineups
Purpose:
Stores player lineups for each match.

Primary Key:
(match_id, player_id)

Foreign Keys:
match_id
player_id
team_id
position_id

Referenced By:
None

Columns:
match_id
player_id
team_id
position_id
jersey_number
starting_position
captain
starter

Relationships:
One Match → Many Players
One Player → Many Matches

Notes:
Contains match-specific player information.
## Table: Events
Purpose:
Stores every event occurring during a football match.

Primary Key:
event_id

Foreign Keys:
match_id
team_id
player_id
event_type_id
play_pattern_id

Referenced By:
PassDetails
ShotDetails
CarryDetails (Future)

Columns:
event_id
match_id
minute
second
team_id
player_id
event_type_id
play_pattern_id
possession
duration
location_x
location_y

Relationships:
One Match → Many Events
One Player → Many Events
One Team → Many Events

Notes:
Core table of the database.

## Tables:Position

Purpose:
Stores football playing positions.

Primary Key:
position_id

Foreign Keys:
None

Referenced By:
Lineups

Columns:
position_id
position_name

Relationships:
One Position → Many Lineups

Notes:
Avoids repeating position names.

## Event types

Purpose:
Stores football event categories.

Primary Key:
event_type_id

Foreign Keys:
None

Referenced By:
Events

Columns:
event_type_id
event_type_name

Relationships:
One Event Type → Many Events

Notes:
Examples include Pass, Shot, Carry, Foul, Duel.


## Table: playpattern

Purpose:
Stores play pattern classifications.

Primary Key:
play_pattern_id

Foreign Keys:
None

Referenced By:
Events

Columns:
play_pattern_id
play_pattern_name

Relationships:
One Play Pattern → Many Events

Notes:
Examples include Regular Play, Corner, Throw In and Free Kick.

## Table: stadiums

Purpose:
Stores stadium information.

Primary Key:
stadium_id

Foreign Keys:
None

Referenced By:
Matches

Columns:
stadium_id
stadium_name

Relationships:
One Stadium → Many Matches

Notes:
Avoids repeating stadium names.

## Table: refree

Purpose:
Stores referee information.

Primary Key:
referee_id

Foreign Keys:
None

Referenced By:
Matches

Columns:
referee_id
referee_name

Relationships:
One Referee → Many Matches

Notes:
Stores referee information separately from matches.