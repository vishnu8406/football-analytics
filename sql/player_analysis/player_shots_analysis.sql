
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

Goals AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS goals

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

Shots AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS total_shots

    FROM Players p
    JOIN Events e
        ON p.player_id = e.player_id
    JOIN ShotEvents se
        ON e.event_id = se.event_id

    GROUP BY
        p.player_id,
        p.player_name
),

ShotsOnTarget AS (

    SELECT
        p.player_id,
        p.player_name,
        COUNT(*) AS shots_on_target

    FROM Players p
    JOIN Events e
        ON p.player_id = e.player_id
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE so.shot_outcome_name IN
    (
        'Goal',
        'Saved',
        'Saved to Post'
    )

    GROUP BY
        p.player_id,
        p.player_name
)

SELECT

    mp.player_name,

    mp.matches_played,

    COALESCE(g.goals,0) AS goals,

    COALESCE(s.total_shots,0) AS total_shots,

    COALESCE(st.shots_on_target,0) AS shots_on_target,

    ROUND(
        COALESCE(st.shots_on_target,0) * 100.0 /
        NULLIF(s.total_shots,0),
        2
    ) AS shot_accuracy,

    ROUND(
        COALESCE(g.goals,0) * 100.0 /
        NULLIF(s.total_shots,0),
        2
    ) AS shot_conversion_rate,

    ROUND(
        COALESCE(s.total_shots,0) * 1.0 /
        NULLIF(mp.matches_played,0),
        2
    ) AS shots_per_match,

    ROUND(
        COALESCE(g.goals,0) * 1.0 /
        NULLIF(mp.matches_played,0),
        2
    ) AS goals_per_match

FROM MatchesPlayed mp

LEFT JOIN Goals g
    ON mp.player_id = g.player_id

LEFT JOIN Shots s
    ON mp.player_id = s.player_id

LEFT JOIN ShotsOnTarget st
    ON mp.player_id = st.player_id

WHERE COALESCE(s.total_shots,0) > 20

ORDER BY goals DESC;