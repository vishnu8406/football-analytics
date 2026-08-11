WITH GoalkeeperActions AS (

    SELECT
        e.player_id,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name = 'Shot Faced'
                THEN 1
            END
        ) AS shots_faced,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name IN
                ('Save','Shot Saved')
                THEN 1
            END
        ) AS saves,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name = 'Goal Conceded'
                THEN 1
            END
        ) AS goals_conceded,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name = 'Penalty Saved'
                THEN 1
            END
        ) AS penalties_saved,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name = 'Punch'
                THEN 1
            END
        ) AS punches,

        COUNT(
            CASE
                WHEN gt.goalkeeper_type_name = 'Keeper Sweeper'
                THEN 1
            END
        ) AS sweeper_actions

    FROM Events e

    JOIN GoalkeeperEvents ge
        ON e.event_id = ge.event_id

    JOIN GoalkeeperTypes gt
        ON ge.goalkeeper_type_id = gt.goalkeeper_type_id

    GROUP BY e.player_id
),

MatchesPlayed AS (

    SELECT
        player_id,
        COUNT(DISTINCT match_id) AS matches_played

    FROM MatchPlayers

    GROUP BY player_id
)

SELECT

    p.player_name,

    mp.matches_played,

    ga.shots_faced,

    ga.saves,

    ga.goals_conceded,

    ROUND(
        ga.saves * 100.0 /
        NULLIF(ga.shots_faced,0),
        2
    ) AS save_percentage,

    ga.penalties_saved,

    ga.punches,

    ga.sweeper_actions,

    ROUND(
        ga.saves * 1.0 /
        mp.matches_played,
        2
    ) AS saves_per_match,

    ROUND(
        ga.goals_conceded * 1.0 /
        mp.matches_played,
        2
    ) AS goals_conceded_per_match

FROM GoalkeeperActions ga

JOIN Players p
    ON ga.player_id = p.player_id

JOIN MatchesPlayed mp
    ON ga.player_id = mp.player_id

WHERE mp.matches_played >= 10

ORDER BY save_percentage DESC;