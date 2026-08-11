-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Possession Performance
--
-- Business Question:
-- Which teams demonstrated the greatest control of possession throughout the
-- season based on possession time, possession frequency, and ball retention?
--
-- Description:
-- This analysis evaluates each team's possession characteristics by measuring
-- estimated possession percentage, possession frequency, possession duration,
-- events per possession, and passes completed within each possession sequence.
--
-- Metrics:
--   • Average Possession Percentage
--   • Total Possessions
--   • Average Possession Duration
--   • Average Events per Possession
--   • Average Passes per Possession
--
-- Methodology:
--   • Each unique (match_id, possession) represents one possession sequence.
--   • Possession time is estimated by summing the duration of all events
--     occurring while the team is in possession.
--   • Match possession percentage is calculated as:
--
--       Team Possession Time
--       ------------------------- × 100
--       Total Match Possession Time
--
--   • Season possession percentage is obtained by averaging the match-level
--     possession percentages across all league matches.
--
-- Note:
-- StatsBomb Open Data does not provide official possession percentages.
-- Possession statistics presented in this analysis are estimated using event
-- durations and possession sequences.
-- ============================================================================

WITH possession_stats AS (

    /* One row = One possession */

    SELECT
        match_id,
        possession,
        possession_team_id,

        SUM(duration) AS possession_time,
        COUNT(*) AS total_events,

        SUM(
            CASE
                WHEN event_type_id = (
                    SELECT event_type_id
                    FROM EventTypes
                    WHERE event_type_name = 'Pass'
                )
                THEN 1
                ELSE 0
            END
        ) AS total_passes

    FROM Events

    GROUP BY
        match_id,
        possession,
        possession_team_id
),

team_possession AS (

    /* Team totals inside each match */

    SELECT
        match_id,
        possession_team_id,

        SUM(possession_time) AS team_possession_time,

        COUNT(*) AS total_possessions,

        AVG(possession_time) AS avg_possession_duration,

        AVG(total_events) AS events_per_possession,

        AVG(total_passes) AS passes_per_possession

    FROM possession_stats

    GROUP BY
        match_id,
        possession_team_id
),

match_totals AS (

    /* Total possession time in every match */

    SELECT
        match_id,
        SUM(team_possession_time) AS total_match_time

    FROM team_possession

    GROUP BY
        match_id
)

SELECT

    t.team_name,

    ROUND(
        AVG(
            tp.team_possession_time * 100.0 /
            mt.total_match_time
        ),
    2) AS avg_possession_percentage,

    SUM(tp.total_possessions) AS total_possessions,

    ROUND(AVG(tp.avg_possession_duration),2)
        AS avg_possession_duration,

    ROUND(AVG(tp.events_per_possession),2)
        AS events_per_possession,

    ROUND(AVG(tp.passes_per_possession),2)
        AS passes_per_possession

FROM team_possession tp

JOIN match_totals mt
    ON tp.match_id = mt.match_id

JOIN Teams t
    ON tp.possession_team_id = t.team_id

GROUP BY
    t.team_id,
    t.team_name

ORDER BY
    avg_possession_percentage DESC;