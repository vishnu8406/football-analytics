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

Fouls AS (

    SELECT
        e.player_id,
        COUNT(*) AS total_fouls

    FROM Events e
    JOIN FoulCommittedEvents fc
        ON e.event_id = fc.event_id

    WHERE e.player_id IS NOT NULL

    GROUP BY e.player_id
),

AllCards AS (

    SELECT
        e.player_id,
        c.card_name

    FROM Events e
    JOIN FoulCommittedEvents fc
        ON e.event_id = fc.event_id
    JOIN Cards c
        ON fc.card_id = c.card_id

    WHERE e.player_id IS NOT NULL

    UNION ALL

    SELECT
        e.player_id,
        c.card_name

    FROM Events e
    JOIN BadBehaviourEvents bb
        ON e.event_id = bb.event_id
    JOIN Cards c
        ON bb.card_id = c.card_id

    WHERE e.player_id IS NOT NULL
),

CardSummary AS (

    SELECT
        player_id,

        COUNT(
            CASE
                WHEN card_name = 'Yellow Card'
                THEN 1
            END
        ) AS yellow_cards,

        COUNT(
            CASE
                WHEN card_name = 'Red Card'
                THEN 1
            END
        ) AS red_cards,

        COUNT(
            CASE
                WHEN card_name = 'Second Yellow Card'
                THEN 1
            END
        ) AS second_yellow_cards

    FROM AllCards

    GROUP BY player_id
)

SELECT

    mp.player_name,

    mp.matches_played,

    COALESCE(f.total_fouls,0) AS total_fouls,

    COALESCE(cs.yellow_cards,0) AS yellow_cards,

    COALESCE(cs.red_cards,0) AS red_cards,

    COALESCE(cs.second_yellow_cards,0) AS second_yellow_cards,

    (
        COALESCE(cs.yellow_cards,0)
        +
        COALESCE(cs.red_cards,0)
        +
        COALESCE(cs.second_yellow_cards,0)
    ) AS total_cards,

    ROUND(
        COALESCE(f.total_fouls,0) * 1.0
        / mp.matches_played,
        2
    ) AS fouls_per_match,

    ROUND(
        (
            COALESCE(cs.yellow_cards,0)
            +
            COALESCE(cs.red_cards,0)
            +
            COALESCE(cs.second_yellow_cards,0)
        ) * 1.0
        / mp.matches_played,
        2
    ) AS cards_per_match

FROM MatchesPlayed mp

LEFT JOIN Fouls f
    ON mp.player_id = f.player_id

LEFT JOIN CardSummary cs
    ON mp.player_id = cs.player_id

WHERE mp.matches_played >= 10

ORDER BY
    total_cards DESC,
    total_fouls DESC;