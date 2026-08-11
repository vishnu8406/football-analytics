-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Overall Performance
--
-- Business Question:
-- Which teams performed best throughout the season based on league results,
-- goal statistics, and points accumulated?
--
-- Description:
-- This analysis generates the league table for all teams by summarizing
-- matches played, wins, draws, losses, goals scored, goals conceded,
-- goal difference, total points, win percentage, and points per match.
--
-- Metrics:
--   • Matches Played
--   • Wins
--   • Draws
--   • Losses
--   • Goals Scored
--   • Goals Conceded
--   • Goal Difference
--   • Points
--   • Win Percentage
--   • Points per Match
-- ============================================================================
SELECT
    t.team_name,
    COUNT(m.match_id) AS matches_played,
    (
        COUNT(
            CASE
                WHEN m.home_score > m.away_score
                AND m.home_team_id = t.team_id THEN 1
            END
        ) + COUNT(
            CASE
                WHEN m.away_score > m.home_score
                AND m.away_team_id = t.team_id THEN 1
            END
        )
    ) AS total_wins,
    COUNT(
        CASE
            WHEN m.home_score = m.away_score THEN 1
        END
    ) AS total_draws,
    (
        COUNT(
            CASE
                WHEN m.home_score < m.away_score
                AND m.home_team_id = t.team_id THEN 1
            END
        ) + COUNT(
            CASE
                WHEN m.away_score < m.home_score
                AND m.away_team_id = t.team_id THEN 1
            END
        )
    ) AS total_losses,
    (
        (
            COUNT(
                CASE
                    WHEN m.home_score > m.away_score
                    AND m.home_team_id = t.team_id THEN 1
                END
            ) + COUNT(
                CASE
                    WHEN m.away_score > m.home_score
                    AND m.away_team_id = t.team_id THEN 1
                END
            )
        ) * 3 + COUNT(
            CASE
                WHEN m.home_score = m.away_score THEN 1
            END
        ) * 1
    ) AS points,
    SUM(
        CASE
            WHEN m.home_team_id = t.team_id THEN m.home_score
            ELSE 0
        END
    ) + SUM(
        CASE
            WHEN m.away_team_id = t.team_id THEN m.away_score
            ELSE 0
        END
    ) AS goals_for,
    SUM(
        CASE
            WHEN m.home_team_id = t.team_id THEN m.away_score
            ELSE 0
        END
    ) + SUM(
        CASE
            WHEN m.away_team_id = t.team_id THEN m.home_score
            ELSE 0
        END
    ) AS goals_against,
    (
        (
            SUM(
                CASE
                    WHEN m.home_team_id = t.team_id THEN m.home_score
                    ELSE 0
                END
            ) + SUM(
                CASE
                    WHEN m.away_team_id = t.team_id THEN m.away_score
                    ELSE 0
                END
            )
        ) -(
            SUM(
                CASE
                    WHEN m.home_team_id = t.team_id THEN m.away_score
                    ELSE 0
                END
            ) + SUM(
                CASE
                    WHEN m.away_team_id = t.team_id THEN m.home_score
                    ELSE 0
                END
            )
        )
    ) AS goal_difference,
    ROUND(
        (
            (
                COUNT(
                    CASE
                        WHEN m.home_score > m.away_score
                        AND m.home_team_id = t.team_id THEN 1
                    END
                ) + COUNT(
                    CASE
                        WHEN m.away_score > m.home_score
                        AND m.away_team_id = t.team_id THEN 1
                    END
                )
            ) * 100.0 / COUNT(m.match_id)
        ),
        2
    ) AS win_percentage,
    ROUND(
        (
            (
                (
                    COUNT(
                        CASE
                            WHEN m.home_score > m.away_score
                            AND m.home_team_id = t.team_id THEN 1
                        END
                    ) + COUNT(
                        CASE
                            WHEN m.away_score > m.home_score
                            AND m.away_team_id = t.team_id THEN 1
                        END
                    )
                ) * 3 + COUNT(
                    CASE
                        WHEN m.home_score = m.away_score THEN 1
                    END
                ) * 1
            ) * 1.0 / COUNT(m.match_id)
        ),
        2
    ) AS points_per_match
FROM
    Teams t
    JOIN Matches m ON t.team_id = m.home_team_id
    OR t.team_id = m.away_team_id
GROUP BY
    t.team_id,
    t.team_name
ORDER BY
    points DESC,
    goal_difference DESC,
    goals_for DESC;