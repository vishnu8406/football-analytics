WITH MatchesPlayed AS (

    SELECT
        mp.player_id,
        COUNT(DISTINCT mp.match_id) AS matches_played

    FROM MatchPlayers mp

    GROUP BY mp.player_id
),

Tackles AS (

    SELECT
        e.player_id,
        COUNT(*) AS tackles_won

    FROM Events e
    JOIN DuelEvents de
        ON e.event_id = de.event_id
    JOIN DuelOutcomes dout
        ON de.duel_outcome_id = dout.duel_outcome_id

    WHERE dout.duel_outcome_name = 'Won'

    GROUP BY e.player_id
),

Interceptions AS (

    SELECT
        e.player_id,
        COUNT(*) AS interceptions

    FROM Events e
    JOIN InterceptionEvents ie
        ON e.event_id = ie.event_id

    GROUP BY e.player_id
),

Recoveries AS (

    SELECT
        e.player_id,
        COUNT(*) AS recoveries

    FROM Events e
    JOIN BallRecoveryEvents bre
        ON e.event_id = bre.event_id

    GROUP BY e.player_id
),

Clearances AS (

    SELECT
        e.player_id,
        COUNT(*) AS clearances

    FROM Events e
    JOIN ClearanceEvents ce
        ON e.event_id = ce.event_id

    GROUP BY e.player_id
),

Blocks AS (

    SELECT
        e.player_id,
        COUNT(*) AS blocks

    FROM Events e
    JOIN BlockEvents be
        ON e.event_id = be.event_id

    GROUP BY e.player_id
)

SELECT

    p.player_name,

    mp.matches_played,

    COALESCE(t.tackles_won,0) AS tackles_won,
    COALESCE(i.interceptions,0) AS interceptions,
    COALESCE(r.recoveries,0) AS recoveries,
    COALESCE(c.clearances,0) AS clearances,
    COALESCE(b.blocks,0) AS blocks,

    (
        COALESCE(t.tackles_won,0) +
        COALESCE(i.interceptions,0) +
        COALESCE(r.recoveries,0) +
        COALESCE(c.clearances,0) +
        COALESCE(b.blocks,0)
    ) AS total_defensive_actions,

    ROUND(
        (
            COALESCE(t.tackles_won,0) +
            COALESCE(i.interceptions,0) +
            COALESCE(r.recoveries,0) +
            COALESCE(c.clearances,0) +
            COALESCE(b.blocks,0)
        ) * 1.0 / mp.matches_played,
        2
    ) AS defensive_actions_per_match

FROM Players p

JOIN MatchesPlayed mp
    ON p.player_id = mp.player_id

LEFT JOIN Tackles t
    ON p.player_id = t.player_id

LEFT JOIN Interceptions i
    ON p.player_id = i.player_id

LEFT JOIN Recoveries r
    ON p.player_id = r.player_id

LEFT JOIN Clearances c
    ON p.player_id = c.player_id

LEFT JOIN Blocks b
    ON p.player_id = b.player_id

WHERE mp.matches_played >= 10

ORDER BY total_defensive_actions DESC;