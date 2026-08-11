WITH MatchesPlayed AS (

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
),

KeyPasses AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS key_passes

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN ShotEvents se
        ON e.event_id = se.key_pass_event_id

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
)

SELECT

    mp.player_name,

    mp.matches_played,

    COALESCE(kp.key_passes,0) AS key_passes,

    COALESCE(a.assists,0) AS assists,

    ROUND(
        COALESCE(kp.key_passes,0) * 1.0 /
        mp.matches_played,
        2
    ) AS key_passes_per_match,

    ROUND(
        COALESCE(a.assists,0) * 1.0 /
        mp.matches_played,
        2
    ) AS assists_per_match,

    ROUND(
        COALESCE(a.assists,0) * 100.0 /
        NULLIF(kp.key_passes,0),
        2
    ) AS assist_conversion_percentage

FROM MatchesPlayed mp

LEFT JOIN KeyPasses kp
    ON mp.player_id = kp.player_id

LEFT JOIN Assists a
    ON mp.player_id = a.player_id

WHERE COALESCE(kp.key_passes,0) > 0

ORDER BY
    key_passes DESC,
    assists DESC

LIMIT 50;