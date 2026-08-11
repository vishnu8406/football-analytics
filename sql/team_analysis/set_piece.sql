
-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Set Piece Effectiveness
--
-- Business Question:
-- Which teams were most effective at converting attacking set-piece
-- opportunities into goals throughout the season?
--
-- Description:
-- This analysis evaluates each team's attacking efficiency from set-piece
-- situations, including corner kicks, penalty kicks, and direct free kicks.
-- It measures both the volume of set-piece opportunities and the success
-- rate of converting those opportunities into goals.
--
-- Metrics:
--   • Total Corners
--   • Corner Goals
--   • Corner Conversion Percentage
--   • Total Penalties
--   • Penalty Goals
--   • Penalty Conversion Percentage
--   • Direct Free Kick Goals
-- ============================================================================
WITH
Corners AS (

    SELECT
        e.team_id,
        COUNT(*) AS total_corners

    FROM Events e
    JOIN PassEvents pe
        ON e.event_id = pe.event_id
    JOIN PassTypes pt
        ON pe.pass_type_id = pt.pass_type_id

    WHERE pt.pass_type_name = 'Corner'

    GROUP BY e.team_id
),

CornerGoals AS (

    SELECT
        e.team_id,
        COUNT(*) AS corner_goals

    FROM Events e
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN PlayPatterns pp
        ON e.play_pattern_id = pp.play_pattern_id
    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE
        pp.play_pattern_name = 'From Corner'
        AND so.shot_outcome_name = 'Goal'

    GROUP BY e.team_id
),

Penalties AS (

    SELECT
        e.team_id,
        COUNT(*) AS total_penalties

    FROM Events e
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN ShotTypes st
        ON se.shot_type_id = st.shot_type_id

    WHERE st.shot_type_name = 'Penalty'

    GROUP BY e.team_id
),

PenaltyGoals AS (

    SELECT
        e.team_id,
        COUNT(*) AS penalty_goals

    FROM Events e
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN ShotTypes st
        ON se.shot_type_id = st.shot_type_id
    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE
        st.shot_type_name = 'Penalty'
        AND so.shot_outcome_name = 'Goal'

    GROUP BY e.team_id
),

FreeKickGoals AS (

    SELECT
        e.team_id,
        COUNT(*) AS free_kick_goals

    FROM Events e
    JOIN ShotEvents se
        ON e.event_id = se.event_id
    JOIN ShotTypes st
        ON se.shot_type_id = st.shot_type_id
    JOIN ShotOutcomes so
        ON se.shot_outcome_id = so.shot_outcome_id

    WHERE
        st.shot_type_name = 'Free Kick'
        AND so.shot_outcome_name = 'Goal'

    GROUP BY e.team_id
)

SELECT

    t.team_name,

    COALESCE(c.total_corners,0) AS total_corners,

    COALESCE(cg.corner_goals,0) AS corner_goals,

    ROUND(
        COALESCE(cg.corner_goals,0)*100.0/
        NULLIF(c.total_corners,0),
    2) AS corner_conversion_percentage,

    COALESCE(p.total_penalties,0) AS total_penalties,

    COALESCE(pg.penalty_goals,0) AS penalty_goals,

    ROUND(
        COALESCE(pg.penalty_goals,0)*100.0/
        NULLIF(p.total_penalties,0),
    2) AS penalty_conversion_percentage,

    COALESCE(fk.free_kick_goals,0) AS free_kick_goals

FROM Teams t

LEFT JOIN Corners c
    ON t.team_id = c.team_id

LEFT JOIN CornerGoals cg
    ON t.team_id = cg.team_id

LEFT JOIN Penalties p
    ON t.team_id = p.team_id

LEFT JOIN PenaltyGoals pg
    ON t.team_id = pg.team_id

LEFT JOIN FreeKickGoals fk
    ON t.team_id = fk.team_id

ORDER BY
    corner_goals DESC,
    penalty_goals DESC;





WITH TotalMatches AS (
    SELECT t.team_id,t.team_name, COUNT (DISTINCT match_id) AS total_matches

    FROM Teams t 
    JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id

    GROUP BY t.team_id,t.team_name

),
GoalsScored AS (
    SELECT t.team_id,t.team_name,(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.home_score END) + SUM(CASE WHEN m.away_team_id = t.team_id THEN m.away_score END)) AS goals_scored

    FROM Teams t
    JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id

    GROUP BY t.team_id,t.team_name
    
    
),

TeamStats AS (
    SELECT t.team_id,t.team_name,t.total_matches,g.goals_scored
FROM TotalMatches t 
JOIN  GoalsScored g ON t.team_id = g.team_id
    )

SELECT *
FROM TeamStats
ORDER BY g.goals_scored DESC