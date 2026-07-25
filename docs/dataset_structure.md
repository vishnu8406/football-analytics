# Competitions

Purpose:
Stores competition metadata.

One file:
competitions.json

One row:
One competition in one season.

Primary Identifier:
competition_id + season_id (to be verified)

Relationships:
Matches belong to competitions.


Matches
--------
Purpose:
Stores one row per football match.

Primary Key:
match_id

Possible Foreign Keys:
competition_id
season_id
home_team_id
away_team_id
stadium_id
referee_id

Potential New Tables:
Teams
Stadiums
Referees
Managers
home_scores
away_scores