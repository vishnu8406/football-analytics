-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Set Piece Statistics
--
-- Business Question:
-- How effective were attacking set pieces during the season in terms of
-- corner kicks and penalty kicks?
--
-- Description:
-- This analysis evaluates the effectiveness of two major attacking set
-- pieces by reporting the total number of corner kicks and penalties,
-- the goals scored from each, and their respective conversion rates.
--
-- Metrics:
--   • Total Corner Kicks
--   • Goals from Corners
--   • Corner Conversion Rate
--   • Total Penalties Awarded
--   • Penalty Goals
--   • Penalty Conversion Rate
-- ============================================================================

SELECT 
     (SELECT COUNT(*) FROM Events AS e
     INNER JOIN PassEvents pe ON e.event_id = pe.event_id
     INNER JOIN PassTypes p ON pe.pass_type_id = p.pass_type_id
     WHERE p.pass_type_name = 'Corner') AS total_corners,

     (SELECT COUNT(*) FROM Events AS e
     INNER JOIN PlayPatterns p ON e.play_pattern_id = p.play_pattern_id
     INNER JOIN ShotEvents se ON e.event_id = se.event_id
     INNER JOIN ShotOutcomes s ON se.shot_outcome_id = s.shot_outcome_id
     WHERE p.play_pattern_name = 'From Corner' AND s.shot_outcome_name = 'Goal') AS total_corner_goals,

     ROUND( 
     ((SELECT COUNT(*) FROM Events AS e
     INNER JOIN PlayPatterns p ON e.play_pattern_id = p.play_pattern_id
     INNER JOIN ShotEvents se ON e.event_id = se.event_id
     INNER JOIN ShotOutcomes s ON se.shot_outcome_id = s.shot_outcome_id
     WHERE p.play_pattern_name = 'From Corner' AND s.shot_outcome_name = 'Goal') *100.0/
     (SELECT COUNT(*) FROM Events AS e
     INNER JOIN PassEvents pe ON e.event_id = pe.event_id
     INNER JOIN PassTypes p ON pe.pass_type_id = p.pass_type_id
     WHERE p.pass_type_name = 'Corner')),2) AS Corner_Conversion_Rate,


     (SELECT COUNT(*) FROM ShotEvents se
     INNER JOIN ShotTypes st ON se.shot_type_id = st.shot_type_id
     WHERE st.shot_type_name = 'Penalty') AS total_penalties,

     (SELECT COUNT(*) FROM ShotEvents se
     INNER JOIN ShotTypes st ON se.shot_type_id = st.shot_type_id
     INNER JOIN ShotOutcomes s ON se.shot_outcome_id = s.shot_outcome_id
     WHERE st.shot_type_name = 'Penalty' AND s.shot_outcome_name = 'Goal') AS total_penalty_goals,

     ROUND((SELECT COUNT(*) FROM ShotEvents se
     INNER JOIN ShotTypes st ON se.shot_type_id = st.shot_type_id
     INNER JOIN ShotOutcomes s ON se.shot_outcome_id = s.shot_outcome_id
     WHERE st.shot_type_name = 'Penalty' AND s.shot_outcome_name = 'Goal') *100.0/
     (SELECT COUNT(*) FROM ShotEvents se
     INNER JOIN ShotTypes st ON se.shot_type_id = st.shot_type_id
     WHERE st.shot_type_name = 'Penalty'),2) AS Penalty_Conversion_Rate
    



       


     
 