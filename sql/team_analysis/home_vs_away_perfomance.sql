-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Home vs Away Performance
--
-- Business Question:
-- How did each team's performance differ between home and away matches
-- throughout the season?
--
-- Description:
-- This analysis compares every team's performance at home and away by
-- evaluating match outcomes, goals scored, goals conceded, points earned,
-- and win percentages. The results highlight the influence of home advantage
-- and identify teams that consistently performed well regardless of venue.
--
-- Metrics:
--   • Home Wins
--   • Home Losses
--   • Home Draws
--   • Away Wins
--   • Away Losses
--   • Away Draws
--   • Home Goals Scored
--   • Away Goals Scored
--   • Home Goals Conceded
--   • Away Goals Conceded
--   • Home Points
--   • Away Points
--   • Home Win Percentage
--   • Away Win Percentage
-- ============================================================================

SELECT t.team_name,
COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score > m.away_score THEN 1 END) AS home_wins,
COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score < m.away_score THEN 1 END) AS home_losses,
COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score = m.away_score THEN 1 END) AS home_draws,

COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score > m.home_score THEN 1 END) AS away_wins,
COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score < m.home_score THEN 1 END) AS away_losses,
COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score = m.home_score THEN 1 END) AS away_draws,

SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_score END) AS total_home_goals_scored,
SUM(CASE WHEN m.away_team_id = t.team_id THEN m.away_score END) AS total_away_goals_scored,


SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_score END) AS total_home_goals_conceded,
SUM(CASE WHEN m.away_team_id = t.team_id THEN m.home_score END) AS total_away_goals_conceded,

(COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score > m.away_score THEN 1 END)*3 + COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score = m.away_score THEN 1 END)) AS home_points,
(COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score > m.home_score THEN 1 END)*3 + COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score = m.home_score THEN 1 END)) AS away_points,

ROUND(COUNT(CASE WHEN m.home_team_id = t.team_id AND m.home_score > m.away_score THEN 1 END) * 100.0/COUNT(CASE WHEN m.home_team_id = t.team_id THEN 1 END),2) AS home_win_percentage,
ROUND(COUNT(CASE WHEN m.away_team_id = t.team_id AND m.away_score > m.home_score THEN 1 END) * 100.0/COUNT(CASE WHEN m.away_team_id = t.team_id THEN 1 END),2) AS away_win_percentage

FROM Teams t
JOIN Matches m
    ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id

GROUP BY t.team_id, t.team_name
ORDER BY home_win_percentage DESC, away_win_percentage DESC;


