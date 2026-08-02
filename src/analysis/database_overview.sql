
/*
===========================================================
Football Analytics Platform

Analysis:
01 - Database Overview

Author:
Maiyarasu S

Description:
Explores the overall structure and contents of the
normalized football analytics database.

===========================================================
*/


-- no of matches
SELECT COUNT(*) FROM Matches

-- no of players
SELECT COUNT(*) FROM Players


SELECT card_name FROM Cards

SELECT pass_outcome_name FROM PassOutcomes
SELECT 
    t.team_name,
    COUNT(CASE WHEN so.shot_outcome_name = 'Goal' THEN 1 END) AS Goals_scored,
    COUNT(*) AS total_shots,
   
    ROUND(100.0 * COUNT(CASE WHEN so.shot_outcome_name = 'Goal'  THEN 1 END) / COUNT(*), 2) AS shot_conversion_rate
FROM Seasons AS s
JOIN Matches m ON s.season_id = m.season_id
JOIN Events e ON m.match_id = e.match_id
JOIN Teams t ON e.team_id = t.team_id
JOIN ShotEvents se ON e.event_id = se.event_id
JOIN ShotOutcomes so On se.shot_outcome_id = so.shot_outcome_id
GROUP BY t.team_id, t.team_name
HAVING COUNT(*) >= 50
ORDER BY shot_conversion_rate DESC;
