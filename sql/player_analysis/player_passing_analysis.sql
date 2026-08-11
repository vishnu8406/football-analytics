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

PassingStats AS (

    SELECT
        p.player_id,
        p.player_name,

        COUNT(*) AS passes_attempted,

        COUNT(
            CASE
                WHEN pe.pass_outcome_id IS NULL
                THEN 1
            END
        ) AS passes_completed,

        ROUND(
            COUNT(
                CASE
                    WHEN pe.pass_outcome_id IS NULL
                    THEN 1
                END
            ) * 100.0 / COUNT(*),
            2
        ) AS pass_accuracy

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN PassEvents pe
        ON e.event_id = pe.event_id

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
),

LongPasses AS (

    SELECT
        p.player_id,
        p.player_name,

        COUNT(
            CASE
                WHEN pe.pass_length > 30
                THEN 1
            END
        ) AS long_passes

    FROM Players p

    JOIN Events e
        ON p.player_id = e.player_id

    JOIN PassEvents pe
        ON e.event_id = pe.event_id

    GROUP BY
        p.player_id,
        p.player_name
)

SELECT

    mp.player_name,

    mp.matches_played,

    ps.passes_attempted,
    ps.passes_completed,
    ps.pass_accuracy,

    ROUND(
        ps.passes_attempted * 1.0 /
        mp.matches_played,
        2
    ) AS passes_per_match,

    COALESCE(kp.key_passes,0) AS key_passes,
    COALESCE(a.assists,0) AS assists,

    COALESCE(lp.long_passes,0) AS long_passes
 
FROM MatchesPlayed mp

JOIN PassingStats ps
    ON mp.player_id = ps.player_id

LEFT JOIN KeyPasses kp
    ON mp.player_id = kp.player_id

LEFT JOIN Assists a
    ON mp.player_id = a.player_id

LEFT JOIN LongPasses lp
    ON mp.player_id = lp.player_id



ORDER BY
    key_passes DESC,
    assists DESC,
    pass_accuracy DESC;