
WITH MatchesPlayed AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(DISTINCT e.match_id) AS matches_played

    FROM Players p
    JOIN Events e
        ON p.player_id = e.player_id

    GROUP BY
        p.player_id,
        p.player_name
),

Goals AS (

    SELECT
        p.player_id,
        COUNT(*) AS goals

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN ShotEvents se
        ON e.event_id = se.event_id

    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE so.shot_outcome_name = 'Goal'

    GROUP BY p.player_id
),

xGStats AS (

    SELECT
        p.player_id,
        p.player_name,

        COUNT(*) AS total_shots,

        ROUND(SUM(se.statsbomb_xg),2) AS total_xg,

        ROUND(AVG(se.statsbomb_xg),3) AS avg_xg_per_shot

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN ShotEvents se
        ON e.event_id = se.event_id

    WHERE se.statsbomb_xg IS NOT NULL

    GROUP BY
        p.player_id,
        p.player_name
)

SELECT

    x.player_name,

    mp.matches_played,

    COALESCE(g.goals,0) AS goals,

    x.total_shots,

    x.total_xg,

    ROUND(
        x.total_xg /
        mp.matches_played,
        2
    ) AS xg_per_match,

    x.avg_xg_per_shot,

    ROUND(
        COALESCE(g.goals,0) - x.total_xg,
        2
    ) AS goals_minus_xg,

    ROUND(
        COALESCE(g.goals,0) * 100.0 /
        x.total_xg,
        2
    ) AS finishing_efficiency

FROM xGStats x

JOIN MatchesPlayed mp
    ON x.player_id = mp.player_id

LEFT JOIN Goals g
    ON x.player_id = g.player_id

WHERE mp.matches_played >= 10

ORDER BY x.total_xg DESC;