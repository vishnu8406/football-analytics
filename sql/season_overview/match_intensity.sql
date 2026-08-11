
-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Match Intensity
--
-- Business Question:
-- How physically demanding and active was the season based on the average
-- number of fouls committed, yellow cards issued, and corner kicks awarded
-- per match?
--
-- Description:
-- This analysis evaluates the overall intensity of the competition by
-- calculating the average number of fouls, yellow cards, and corner kicks
-- recorded per match throughout the season.
--
-- Metrics:
--   • Fouls Committed per Match
--   • Yellow Cards per Match
--   • Corner Kicks per Match
-- ============================================================================
SELECT 
    ROUND(((SELECT COUNT(*) FROM FoulCommittedEvents) *1.0 
    / (SELECT COUNT(*) FROM Matches)), 2) AS Foul_Committed_per_Match,

     ROUND(((SELECT COUNT(*) FROM FoulCommittedEvents fc
     INNER JOIN Cards c ON fc.card_id= c.card_id
     WHERE c.card_name = 'Yellow Card') + 
     (SELECT COUNT(*) FROM BadBehaviourEvents
     INNER JOIN Cards c ON BadBehaviourEvents.card_id = c.card_id
     WHERE c.card_name = 'Yellow Card')) * 1.0/
     (SELECT COUNT(*) FROM Matches), 2) AS Yellow_Card_per_match,

     ROUND((SELECT COUNT(*) FROM Events AS e
     INNER JOIN PassEvents pe ON e.event_id = pe.event_id
     INNER JOIN PassTypes p ON pe.pass_type_id = p.pass_type_id
     WHERE p.pass_type_name = 'Corner') * 1.0/
     (SELECT COUNT(*) FROM Matches), 2) AS Corner_per_match


