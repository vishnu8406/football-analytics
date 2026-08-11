
-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Discipline Performance
--
-- Business Question:
-- Which teams displayed the highest and lowest levels of discipline
-- throughout the season?
--
-- Description:
-- This analysis evaluates each team's disciplinary record by measuring
-- fouls committed, yellow cards, second yellow dismissals, straight red
-- cards, total cards received, and per-match disciplinary averages.
--
-- Metrics:
--   • Total Fouls
--   • Yellow Cards
--   • Straight Red Cards
--   • Second Yellow Cards
--   • Total Cards
--   • Fouls per Match
--   • Yellow Cards per Match
--   • Red Cards per Match
--   • Second Yellow Cards per Match
-- ============================================================================


WITH Fouls AS (

    SELECT
        e.team_id,
        COUNT(*) AS total_fouls
    FROM Events e
    JOIN FoulCommittedEvents f
        ON e.event_id = f.event_id
    GROUP BY e.team_id

),

AllCards AS (

    SELECT
        team_id,

        COUNT(CASE WHEN card_name = 'Yellow Card' THEN 1 END) AS yellow_cards,

        COUNT(CASE WHEN card_name = 'Red Card' THEN 1 END) AS red_cards,

        COUNT(CASE WHEN card_name = 'Second Yellow' THEN 1 END) AS second_yellow_cards

    FROM (

        SELECT
            e.team_id,
            c.card_name
        FROM Events e
        JOIN FoulCommittedEvents f
            ON e.event_id = f.event_id
        JOIN Cards c
            ON f.card_id = c.card_id

        UNION ALL

        SELECT
            e.team_id,
            c.card_name
        FROM Events e
        JOIN BadBehaviourEvents b
            ON e.event_id = b.event_id
        JOIN Cards c
            ON b.card_id = c.card_id

    )

    GROUP BY team_id
),
MatchesPlayed AS (

    SELECT
        t.team_id,
        COUNT(m.match_id) AS matches_played

    FROM Teams t
    JOIN Matches m
        ON t.team_id = m.home_team_id
        OR t.team_id = m.away_team_id

    GROUP BY
        t.team_id
)


SELECT
    t.team_name,
    f.total_fouls ,
    ac.yellow_cards,
    ac.red_cards,
ac.second_yellow_cards,
(ac.yellow_cards+ac.red_cards+ac.second_yellow_cards) AS total_cards,
  ROUND(((ac.yellow_cards+ac.red_cards+ac.second_yellow_cards)*1.0/f.total_fouls),2) AS cards_per_match,
    ROUND((f.total_fouls * 1.0 / mp.matches_played),2) AS fouls_per_match,
    ROUND((ac.yellow_cards * 1.0 / mp.matches_played),2) AS yellow_cards_per_match,
    ROUND((ac.red_cards * 1.0 / mp.matches_played),2) AS red_cards_per_match,
    ROUND((ac.second_yellow_cards * 1.0 / mp.matches_played),2) AS second_yellow_cards_per_match
   

FROM Teams t

LEFT JOIN Fouls f
    ON t.team_id = f.team_id

LEFT JOIN MatchesPlayed mp
    ON t.team_id = mp.team_id

LEFT JOIN AllCards ac
    ON t.team_id = ac.team_id

ORDER BY total_cards DESC ,f.total_fouls DESC ;