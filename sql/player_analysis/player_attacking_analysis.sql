
WITH Goals AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS goals_scored

    FROM Players p
    JOIN Events e
        ON p.player_id = e.player_id
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE so.shot_outcome_name = 'Goal'

    GROUP BY
        p.player_id,
        p.player_name

),
Assists AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS assists

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN ShotEvents se
        ON e.event_id = se.key_pass_event_id

    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE so.shot_outcome_name = 'Goal'

    GROUP BY
        p.player_id,
        p.player_name
),
Passes AS (
    SELECT p.player_id, p.player_name,
     COUNT(*) AS attempted_passes,
     COUNT(CASE WHEN pe.pass_outcome_id IS NULL THEN 1 END) AS completed_passes,
     (COUNT(CASE WHEN pe.pass_outcome_id IS NULL THEN 1 END)*100.0/COUNT(*)) AS pass_percentage

    FROM Players p
    JOIN Events e ON p.player_id = e.player_id
    JOIN PassEvents pe ON e.event_id = pe.event_id
    

    GROUP BY p.player_id,p.player_name

),

Shots AS (
    SELECT p.player_id,p.player_name, COUNT(*) AS attempted_shots

    FROM Players p
    JOIN Events e ON p.player_id = e.player_id
    JOIN ShotEvents se ON e.event_id = se.event_id

    GROUP BY p.player_id, p.player_name
    
),

MatchesPlayed AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(DISTINCT mp.match_id) AS matches_played

    FROM Players p
    JOIN MatchPlayers mp
        ON p.player_id = mp.player_id

    GROUP BY
        p.player_id,
        p.player_name
)

SELECT
    mp.player_name,
    mp.matches_played,

    COALESCE(g.goals_scored,0) AS goals,
    COALESCE(a.assists,0) AS assists,
    COALESCE(s.attempted_shots,0) AS shots,

    COALESCE(pa.attempted_passes,0) AS passes_attempted,
    COALESCE(pa.completed_passes,0) AS passes_completed,

    ROUND(
        COALESCE(pa.pass_percentage,0),
        2
    ) AS pass_accuracy
PRAGMA table_info(PassEvents);
FROM MatchesPlayed mp

LEFT JOIN Goals g
    ON mp.player_id = g.player_id

LEFT JOIN Assists a
    ON mp.player_id = a.player_id

LEFT JOIN Shots s
    ON mp.player_id = s.player_id

LEFT JOIN Passes pa
    ON mp.player_id = pa.player_id

ORDER BY goals DESC;