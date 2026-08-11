-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Attacking Performance
--
-- Business Question:
-- Which teams were the most effective in attack throughout the season based
-- on goal scoring, shot creation, shooting accuracy, and goal conversion?
--
-- Description:
-- This analysis evaluates the attacking performance of every team by
-- summarizing goal production, shooting volume, shooting accuracy,
-- conversion efficiency, and the contribution of different goal types,
-- including open-play, set-piece, and penalty goals.
--
-- Metrics:
--   • Goals Scored (Excluding Own Goals)
--   • Goals per Match
--   • Total Shots
--   • Shots on Target
--   • Shot Accuracy
--   • Shot Conversion Rate
--   • Open Play Goals
--   • Set Piece Goals
--   • Penalty Goals
--
-- Note:
-- Goals Scored are derived from successful Shot Events and therefore exclude
-- opponent own goals. As a result, these values may differ slightly from the
-- official Goals For (GF) reported in the league table.
-- ============================================================================
SELECT
    t.team_name,
    COUNT(
        CASE
            WHEN (
                t.team_id = m.home_team_id
                OR t.team_id = m.away_team_id
            )
            AND so.shot_outcome_name = 'Goal' THEN 1
        END
    ) AS goals_scored,
    ROUND(
        (
            COUNT(
                CASE
                    WHEN (
                        t.team_id = m.home_team_id
                        OR t.team_id = m.away_team_id
                    )
                    AND so.shot_outcome_name = 'Goal' THEN 1
                END
            ) * 1.0 / COUNT(DISTINCT m.match_id)
        ),
        2
    ) AS goals_per_match,
    COUNT(m.match_id) AS total_shots,
    COUNT(
        CASE
            WHEN (
                t.team_id = m.home_team_id
                OR t.team_id = m.away_team_id
            )
            AND so.shot_outcome_name IN ('Goal', 'Saved', 'Saved to Post') THEN 1
        END
    ) AS shots_on_target,
    ROUND(
        (
            COUNT(
                CASE
                    WHEN (
                        t.team_id = m.home_team_id
                        OR t.team_id = m.away_team_id
                    )
                    AND so.shot_outcome_name IN ('Goal', 'Saved', 'Saved to Post') THEN 1
                END
            ) * 100.0 / COUNT(m.match_id)
        ),
        2
    ) AS shots_accuracy,
    ROUND(
        (
            COUNT(
                CASE
                    WHEN (
                        t.team_id = m.home_team_id
                        OR t.team_id = m.away_team_id
                    )
                    AND so.shot_outcome_name = 'Goal' THEN 1
                END
            ) * 100.0 / COUNT(m.match_id)
        ),
        2
    ) AS shot_conversion_rate,
    COUNT(
        CASE
            WHEN (
                t.team_id = m.home_team_id
                OR t.team_id = m.away_team_id
            )
            AND so.shot_outcome_name = 'Goal'
            AND st.shot_type_name = 'Open Play' THEN 1
        END
    ) AS open_play_goals,
    COUNT(
        CASE
            WHEN (
                t.team_id = m.home_team_id
                OR t.team_id = m.away_team_id
            )
            AND so.shot_outcome_name = 'Goal'
            AND st.shot_type_name IN ('Corner', 'Free Kick') THEN 1
        END
    ) AS set_piece_goals,
    COUNT(
        CASE
            WHEN (
                t.team_id = m.home_team_id
                OR t.team_id = m.away_team_id
            )
            AND so.shot_outcome_name = 'Goal'
            AND st.shot_type_name = 'Penalty' THEN 1
        END
    ) AS penalty_goals
FROM
    teams t
    JOIN Matches m ON t.team_id = m.home_team_id
    OR t.team_id = m.away_team_id
    JOIN Events e ON m.match_id = e.match_id
    AND e.team_id = t.team_id
    JOIN ShotEvents se ON e.event_id = se.event_id
    JOIN ShotTypes st ON se.shot_type_id = st.shot_type_id
    JOIN ShotOutcomes so ON se.shot_outcome_id = so.shot_outcome_id
GROUP BY
    t.team_id,
    t.team_name
ORDER BY
    goals_per_match DESC,
    goals_scored DESC,
    shot_conversion_rate DESC;