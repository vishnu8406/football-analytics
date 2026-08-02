-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Disciplinary Statistics
--
-- Business Question:
-- What were the overall disciplinary characteristics of the season in terms
-- of fouls committed, bookings, dismissals, and referee decisions?
--
-- Description:
-- This analysis summarizes the disciplinary profile of the season by
-- reporting the total number of fouls committed, yellow cards, second-yellow
-- dismissals, straight red cards, and the frequency with which fouls resulted
-- in disciplinary action.
--
-- Metrics:
--   • Total Fouls Committed
--   • Total Yellow Cards
--   • Total Second Yellow Cards
--   • Total Straight Red Cards
--   • Yellow Cards per Foul
--   • Straight Red Cards per Foul
-- ============================================================================


SELECT

    /* Total Fouls */
    (SELECT COUNT(*)
     FROM FoulCommittedEvents) AS total_fouls,

    /* Yellow Cards */
    (
        (SELECT COUNT(*)
         FROM FoulCommittedEvents f
         JOIN Cards c
            ON f.card_id = c.card_id
         WHERE c.card_name = 'Yellow Card')

        +

        (SELECT COUNT(*)
         FROM BadBehaviourEvents b
         JOIN Cards c
            ON b.card_id = c.card_id
         WHERE c.card_name = 'Yellow Card')
    ) AS yellow_cards,

    /* Second Yellow Cards */
    (
        (SELECT COUNT(*)
         FROM FoulCommittedEvents f
         JOIN Cards c
            ON f.card_id = c.card_id
         WHERE c.card_name = 'Second Yellow')

        +

        (SELECT COUNT(*)
         FROM BadBehaviourEvents b
         JOIN Cards c
            ON b.card_id = c.card_id
         WHERE c.card_name = 'Second Yellow')
    ) AS second_yellow_cards,

    /* Straight Red Cards */
    (
        (SELECT COUNT(*)
         FROM FoulCommittedEvents f
         JOIN Cards c
            ON f.card_id = c.card_id
         WHERE c.card_name = 'Red Card')

        +

        (SELECT COUNT(*)
         FROM BadBehaviourEvents b
         JOIN Cards c
            ON b.card_id = c.card_id
         WHERE c.card_name = 'Red Card')
    ) AS straight_red_cards,

    (((
        (SELECT COUNT(*)
         FROM FoulCommittedEvents f
         JOIN Cards c
            ON f.card_id = c.card_id
         WHERE c.card_name = 'Yellow Card' OR c.card_name = 'Second Yellow')

    
    )*1.0 / (SELECT COUNT(*)
     FROM FoulCommittedEvents)) * 100 ) AS yellow_card_per_foul_rate,


     (((
        (SELECT COUNT(*)
         FROM FoulCommittedEvents f
         JOIN Cards c
            ON f.card_id = c.card_id
         WHERE c.card_name = 'Red Card')

        
    ) *1.0 / (SELECT COUNT(*)
     FROM FoulCommittedEvents)) * 100 ) AS Straight_red_card_per_foul_rate,

