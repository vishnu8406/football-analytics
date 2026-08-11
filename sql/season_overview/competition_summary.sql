-- ============================================================================
-- Football Analytics
-- Analysis : Season Overview
-- Section  : Competition Summary
--
-- Description:
-- Returns high-level competition statistics for the selected season,
-- including the number of matches, teams, players, and unique starting
-- XI players.
--
-- Metrics:
--   • Total Matches
--   • Total Teams
--   • Total Players
--   • Total Starting XI Players
-- ============================================================================

SELECT
    /* Total matches played */
    (SELECT COUNT(*)
     FROM Matches) AS total_matches,

    /* Total participating teams */
    (SELECT COUNT(*)
     FROM Teams) AS total_teams,

    /* Total registered players */
    (SELECT COUNT(*)
     FROM Players) AS total_players,

    /* Players who started at least one match */
    (SELECT COUNT(DISTINCT player_id)
     FROM PlayerPositions
     WHERE start_reason = 'Starting XI') AS total_starting_xi_players;
