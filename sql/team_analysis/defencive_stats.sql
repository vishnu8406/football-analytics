-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Defensive Performance
--
-- Business Question:
-- Which teams demonstrated the strongest defensive performance throughout the
-- season based on goals conceded, defensive consistency, clean sheets, and
-- goalkeeper saves?
--
-- Description:
-- This analysis evaluates each team's defensive performance by summarizing
-- goals conceded, average goals conceded per match, clean sheets, and total
-- goalkeeper saves across the season.
--
-- Metrics:
--   • Goals Conceded
--   • Goals Conceded per Match
--   • Clean Sheets
--   • Goalkeeper Saves
-- ============================================================================


SELECT
    t.team_name,
    COUNT(
        CASE
            WHEN gkt.goalkeeper_type_name = 'Goal Conceded' THEN 1
        END
    ) AS goals_conceded,
    ROUND(
        (
            COUNT(
                CASE
                    WHEN gkt.goalkeeper_type_name = 'Goal Conceded' THEN 1
                END
            ) * 1.0 / COUNT(DISTINCT m.match_id)
        ),
        2
    ) AS goal_conceded_per_match,
    (
        COUNT(
            DISTINCT CASE
                WHEN m.home_team_id = t.team_id
                AND m.away_score = 0 THEN m.match_id
            END
        ) + COUNT(
            DISTINCT CASE
                WHEN m.away_team_id = t.team_id
                AND m.home_score = 0 THEN m.match_id
            END
        )
    ) AS clean_sheets,
    COUNT(
        CASE
            WHEN gkt.goalkeeper_type_name IN (
                'Save',
                'Penalty Saved',
                'Shot Saved to Post',
                'Shot Saved Off Target',
                'Shot Saved'
            ) THEN 1
        END
    ) AS goalkeeper_saves
FROM
    teams t
    JOIN Matches m ON t.team_id = m.home_team_id
    OR t.team_id = m.away_team_id
    JOIN Events e ON m.match_id = e.match_id
    AND e.team_id = t.team_id
    JOIN GoalkeeperEvents gk ON e.event_id = gk.event_id
    JOIN GoalKeeperTypes gkt ON gk.goalkeeper_type_id = gkt.goalkeeper_type_id
GROUP BY
    t.team_id,
    t.team_name
ORDER BY
    clean_sheets DESC,
    goals_conceded ASC;