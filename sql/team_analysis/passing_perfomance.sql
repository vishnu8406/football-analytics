-- ============================================================================
-- Football Analytics
-- Analysis : Team Analysis
-- Section  : Passing Performance
--
-- Business Question:
-- Which teams demonstrated the strongest passing performance throughout the
-- season based on passing volume, completion rate, pass distribution, and
-- passing style?
--
-- Description:
-- This analysis evaluates each team's passing characteristics by measuring
-- total passing volume, passing accuracy, pass height distribution, and pass
-- length distribution. Together, these metrics provide insights into a team's
-- preferred style of ball progression and overall passing efficiency.
--
-- Metrics:
--   • Total Passes
--   • Successful Passes
--   • Pass Accuracy
--   • High Passes
--   • Low Passes
--   • Ground Passes
--   • Average Pass Length
--   • Short Passes (0–15 m)
--   • Medium Passes (15–30 m)
--   • Long Passes (>30 m)
--
-- Note:
-- A completed pass is identified when pass_outcome_id IS NULL, following the
-- StatsBomb event model.
-- ============================================================================
SELECT
  t.team_name,
  (
    COUNT(
      CASE
        WHEN pt.pass_outcome_id IS NULL THEN 1
      END
    ) + COUNT(
      CASE
        WHEN pt.pass_outcome_id IS NOT NULL THEN 1
      END
    )
  ) AS total_passes,
  COUNT(
    CASE
      WHEN pt.pass_outcome_id IS NULL THEN 1
    END
  ) AS successful_passes,
  (
    COUNT(
      CASE
        WHEN pt.pass_outcome_id IS NULL THEN 1
      END
    ) * 100.0 / (
      COUNT(
        CASE
          WHEN pt.pass_outcome_id IS NULL THEN 1
        END
      ) + COUNT(
        CASE
          WHEN pt.pass_outcome_id IS NOT NULL THEN 1
        END
      )
    )
  ) AS pass_accuracy,
  COUNT(
    CASE
      WHEN ph.pass_height_name = 'High Pass' THEN 1
    END
  ) AS high_passes,
  COUNT(
    CASE
      WHEN ph.pass_height_name = 'Low Pass' THEN 1
    END
  ) AS low_passes,
  COUNT(
    CASE
      WHEN ph.pass_height_name = 'Ground Pass' THEN 1
    END
  ) AS ground,
  AVG(p.pass_length) AS avg_pass_length,
  COUNT(
    CASE
      WHEN p.pass_length BETWEEN 0
      AND 15 THEN 1
    END
  ) AS avg_pass_length_0_15,
  COUNT(
    CASE
      WHEN p.pass_length BETWEEN 15
      AND 30 THEN 1
    END
  ) AS avg_pass_length_15_30,
  COUNT(
    CASE
      WHEN p.pass_length > 30 THEN 1
    END
  ) AS avg_pass_length_30_plus
FROM
  teams t
  JOIN matches m ON t.team_id = m.home_team_id
  OR t.team_id = m.away_team_id
  JOIN Events e ON m.match_id = e.match_id
  AND e.team_id = t.team_id
  JOIN PassEvents p ON e.event_id = p.event_id
  LEFT JOIN PassOutcomes pt ON p.pass_outcome_id = pt.pass_outcome_id
  JOIN PassHeights ph ON p.pass_height_id = ph.pass_height_id
GROUP BY
  t.team_id,
  t.team_name
ORDER BY
  total_passes DESC;