
-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Goal Statistics
--
-- Business Question:
-- What are the overall goal-scoring characteristics of the season?
--
-- Description:
-- This analysis summarizes the overall goal statistics for the season,
-- including goals scored by home and away teams, total goals, own goals,
-- open play goals, dead-ball goals, and the average number of goals per
-- match.
--
-- Metrics:
--   • Home Goals
--   • Away Goals
--   • Total Goals
--   • Own Goals
--   • Open Play Goals
--   • Dead-Ball Goals
--   • Average Goals per Match
-- ============================================================================
SELECT

    (SELECT SUM(home_score)
    FROM Matches ) AS home_score,

    (SELECT SUM(away_score)
    FROM Matches) AS away_score,

    (SELECT (SUM(away_score)+ SUM(home_score))
    FROM Matches) AS total_goals,


    (SELECT COUNT(*) FROM Events AS e
    INNER JOIN EventTypes et ON e.event_type_id = et.event_type_id
    WHERE et.event_type_name = 'Own Goal Against') AS own_goals,

    (SELECT COUNT(*) FROM ShotEvents AS se
    INNER JOIN ShotOutcomes so ON se.shot_outcome_id = so.shot_outcome_id
    INNER JOIN Events e ON se.event_id = e.event_id
    INNER JOIN PlayPatterns pp ON e.play_pattern_id = pp.play_pattern_id
    WHERE ((pp.play_pattern_name NOT IN ('Regular Play','From Counter')) 
    AND so.shot_outcome_name = 'Goal' )) AS Deadball_goals,

    (SELECT COUNT(*) FROM ShotEvents AS se
    INNER JOIN ShotOutcomes so ON se.shot_outcome_id = so.shot_outcome_id
    INNER JOIN Events e ON se.event_id = e.event_id
    INNER JOIN PlayPatterns pp ON e.play_pattern_id = pp.play_pattern_id
    WHERE ((pp.play_pattern_name = 'Regular Play' OR pp.play_pattern_name = 'From Counter')
     AND so.shot_outcome_name = 'Goal' )) AS open_play_goals,

     (SELECT ROUND(((SUM(away_score) + SUM(home_score)) * 1.0 / COUNT(*)), 2) 
FROM Matches) AS avg_goals_per_match 
    



