
-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Match Competitiveness
--
-- Business Question:
-- How competitive and entertaining was the season based on match outcomes
-- and scoring patterns?
--
-- Description:
-- Summarizes match outcomes by reporting home wins, away wins, draws,
-- draw percentage, goalless draws, and high-scoring matches to evaluate
-- the competitiveness and entertainment value of the season.
--
-- Metrics:
--   • Total Matches
--   • Home Wins
--   • Away Wins
--   • Draws
--   • Draw Percentage
--   • Goalless Draws
--   • High-Scoring Matches (>3 Goals)
-- ============================================================================
SELECT 
  (SELECT COUNT(*)  FROM matches) AS total_matches,

    (SELECT COUNT(*)  FROM matches
    WHERE home_score > away_score) AS home_wins,

    (SELECT COUNT(*)  FROM matches
    WHERE home_score < away_score) AS away_wins,

    (SELECT COUNT(*)  FROM matches
    WHERE home_score = away_score) AS draws,

    (SELECT  COUNT(*) AS total_goalless_draws FROM matches
    WHERE home_score = 0 AND away_score = 0) AS total_goalless_draws,

    (SELECT COUNT(*) AS high_scoring_matches FROM matches
    WHERE (home_score+ away_score) > 3) AS high_scoring_matches,

    (SELECT 
        ROUND((COUNT(CASE WHEN home_score = away_score THEN 1 END) * 1.0 / COUNT(*)) * 100, 2)
    FROM Matches   
    ) AS draw_percentage

