import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/database/football.db")

query = """
WITH
-- =====================================================
-- MINUTES PLAYED
-- =====================================================
player_minutes_raw AS (

    SELECT
        match_id,
        player_id,
        position_id,

        CAST(substr(from_time,1,2) AS REAL)
        +
        CAST(substr(from_time,4,2) AS REAL)/60.0
        AS start_min,

        CASE
            WHEN to_time IS NULL OR to_time = ''
            THEN 90.0
            ELSE
                CAST(substr(to_time,1,2) AS REAL)
                +
                CAST(substr(to_time,4,2) AS REAL)/60.0
        END AS end_min

    FROM PlayerPositions
),

player_minutes AS (

    SELECT
        match_id,
        player_id,

        MAX(position_id) AS position_id,

        ROUND(
            SUM(end_min - start_min),
            2
        ) AS minutes_played

    FROM player_minutes_raw

    GROUP BY
        match_id,
        player_id
),

-- =====================================================
-- BASE PLAYERS
-- =====================================================

players_in_match AS (

    SELECT DISTINCT

        e.match_id,
        e.player_id,

        p.player_name,
        t.team_name,
        e.team_id

    FROM Events e

    JOIN Players p
        ON e.player_id = p.player_id

    JOIN Teams t
        ON e.team_id = t.team_id
),

-- =====================================================
-- PASSING
-- =====================================================

passes AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS total_passes,

        SUM(
            CASE
                WHEN pe.pass_outcome_id IS NULL
                THEN 1
                ELSE 0
            END
        ) AS completed_passes

    FROM PassEvents pe

    JOIN Events e
        ON pe.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- SHOTS + GOALS + XG
-- =====================================================

shots AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS shots,

        SUM(
            COALESCE(se.statsbomb_xg,0)
        ) AS total_xg,

        SUM(
            CASE
                WHEN se.shot_outcome_id = 97
                THEN 1
                ELSE 0
            END
        ) AS goals

    FROM ShotEvents se

    JOIN Events e
        ON se.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- ASSISTS
-- =====================================================

assists AS (

    SELECT

        assist_event.match_id,
        assist_event.player_id,

        COUNT(*) AS assists

    FROM ShotEvents se

    JOIN Events shot_event
        ON se.event_id = shot_event.event_id

    JOIN Events assist_event
        ON se.key_pass_event_id = assist_event.event_id

    WHERE
        se.shot_outcome_id = 97
        AND se.key_pass_event_id IS NOT NULL

    GROUP BY
        assist_event.match_id,
        assist_event.player_id
),

-- =====================================================
-- INTERCEPTIONS
-- =====================================================

interceptions AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS interceptions

    FROM InterceptionEvents ie

    JOIN Events e
        ON ie.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- RECOVERIES
-- =====================================================

recoveries AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS recoveries

    FROM BallRecoveryEvents bre

    JOIN Events e
        ON bre.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- BLOCKS
-- =====================================================

blocks AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS blocks

    FROM BlockEvents be

    JOIN Events e
        ON be.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- CLEARANCES
-- =====================================================

clearances AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS clearances

    FROM ClearanceEvents ce

    JOIN Events e
        ON ce.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- GOALKEEPER
-- =====================================================

goalkeepers AS (

    SELECT

        e.match_id,
        e.player_id,

        COUNT(*) AS goalkeeper_actions

    FROM GoalkeeperEvents ge

    JOIN Events e
        ON ge.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- CARDS
-- =====================================================

cards AS (

    SELECT

        e.match_id,
        e.player_id,

        SUM(
            CASE
                WHEN bbe.card_id = 7
                THEN 1
                ELSE 0
            END
        ) AS yellow_cards,

        SUM(
            CASE
                WHEN bbe.card_id IN (5,6)
                THEN 1
                ELSE 0
            END
        ) AS red_cards

    FROM BadBehaviourEvents bbe

    JOIN Events e
        ON bbe.event_id = e.event_id

    GROUP BY
        e.match_id,
        e.player_id
),

-- =====================================================
-- GOALS SCORED BY TEAM
-- =====================================================

team_goals AS (

    SELECT

        e.match_id,
        e.team_id,

        COUNT(*) AS goals_scored

    FROM ShotEvents se

    JOIN Events e
        ON se.event_id = e.event_id

    WHERE se.shot_outcome_id = 97

    GROUP BY
        e.match_id,
        e.team_id
),

-- =====================================================
-- GOALS CONCEDED
-- =====================================================

team_goals_conceded AS (

    SELECT

        m.match_id,
        m.home_team_id AS team_id,

        COALESCE(away.goals_scored,0) AS goals_conceded

    FROM Matches m

    LEFT JOIN team_goals away
        ON m.match_id = away.match_id
        AND m.away_team_id = away.team_id

    UNION ALL

    SELECT

        m.match_id,
        m.away_team_id AS team_id,

        COALESCE(home.goals_scored,0) AS goals_conceded

    FROM Matches m

    LEFT JOIN team_goals home
        ON m.match_id = home.match_id
        AND m.home_team_id = home.team_id
)

SELECT

    pm.match_id,
    pm.player_id,
    pm.player_name,
    pm.team_name,
    pm.team_id,

    mins.position_id,
    mins.minutes_played,

    tg.goals_conceded,

    COALESCE(s.goals,0) AS goals,
    COALESCE(a.assists,0) AS assists,

    COALESCE(s.shots,0) AS shots,

    ROUND(
        COALESCE(s.total_xg,0),
        3
    ) AS total_xg,

    COALESCE(p.total_passes,0) AS total_passes,
    COALESCE(p.completed_passes,0) AS completed_passes,

    COALESCE(i.interceptions,0) AS interceptions,
    COALESCE(r.recoveries,0) AS recoveries,
    COALESCE(b.blocks,0) AS blocks,
    COALESCE(c.clearances,0) AS clearances,

    COALESCE(g.goalkeeper_actions,0)
        AS goalkeeper_actions,

    COALESCE(cd.yellow_cards,0)
        AS yellow_cards,

    COALESCE(cd.red_cards,0)
        AS red_cards

FROM players_in_match pm

LEFT JOIN player_minutes mins
ON pm.match_id = mins.match_id
AND pm.player_id = mins.player_id

LEFT JOIN team_goals_conceded tg
ON pm.match_id = tg.match_id
AND pm.team_id = tg.team_id

LEFT JOIN passes p
ON pm.match_id = p.match_id
AND pm.player_id = p.player_id

LEFT JOIN shots s
ON pm.match_id = s.match_id
AND pm.player_id = s.player_id

LEFT JOIN assists a
ON pm.match_id = a.match_id
AND pm.player_id = a.player_id

LEFT JOIN interceptions i
ON pm.match_id = i.match_id
AND pm.player_id = i.player_id

LEFT JOIN recoveries r
ON pm.match_id = r.match_id
AND pm.player_id = r.player_id

LEFT JOIN blocks b
ON pm.match_id = b.match_id
AND pm.player_id = b.player_id

LEFT JOIN clearances c
ON pm.match_id = c.match_id
AND pm.player_id = c.player_id

LEFT JOIN goalkeepers g
ON pm.match_id = g.match_id
AND pm.player_id = g.player_id

LEFT JOIN cards cd
ON pm.match_id = cd.match_id
AND pm.player_id = cd.player_id
"""
match_info = pd.read_sql_query("""
SELECT
    m.match_id,
    ht.team_name AS home_team,
    at.team_name AS away_team

FROM Matches m

JOIN Teams ht
    ON m.home_team_id = ht.team_id

JOIN Teams at
    ON m.away_team_id = at.team_id
""", conn)

match_info["match_name"] = (
    match_info["home_team"]
    + " vs "
    + match_info["away_team"]
)
# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_sql_query(query, conn)

# =====================================================
# PASS ACCURACY
# =====================================================

df["pass_accuracy"] = np.where(
    df["total_passes"] > 0,
    df["completed_passes"] / df["total_passes"] * 100,
    0
)

# =====================================================
# CLEAN SHEETS
# =====================================================

df["gk_clean_sheet"] = np.where(
    (df["goals_conceded"] == 0)
    & (df["minutes_played"] >= 60)
    & (df["position_id"] == 1),
    1,
    0
)

df["def_clean_sheet"] = np.where(
    (df["goals_conceded"] == 0)
    & (df["minutes_played"] >= 60)
    & (df["position_id"].isin([2,3,4,5,6,7,8])),
    1,
    0
)

df["dm_clean_sheet"] = np.where(
    (df["goals_conceded"] == 0)
    & (df["minutes_played"] >= 60)
    & (df["position_id"].isin([9,10,11])),
    1,
    0
)

attacking_positions = [
    17,18,19,20,21,
    22,23,24
]

df["finishing_bonus"] = np.where(
    df["position_id"].isin(attacking_positions),
    (df["goals"] - df["total_xg"]) * 0.7,
    0
)

# =====================================================
# RATING ENGINE
# =====================================================

df["rating"] = (
    6.3

    # ATTACK
    + df["goals"] * 1.2
    + df["assists"] * 0.9
    + df["total_xg"] * 0.25
    + df["shots"] * 0.03
    + df["finishing_bonus"]

    # PASSING
    + df["pass_accuracy"] * 0.002

    # DEFENDING
    + df["interceptions"] * 0.12
    + df["recoveries"] * 0.04
    + df["blocks"] * 0.12
    + df["clearances"] * 0.04

    # GOALKEEPER
    + df["goalkeeper_actions"] * 0.04

    # CLEAN SHEET
    + df["gk_clean_sheet"] * 0.75
    + df["def_clean_sheet"] * 0.50
    + df["dm_clean_sheet"] * 0.25

    # DISCIPLINE
    - df["yellow_cards"] * 0.30
    - df["red_cards"] * 1.50
)
# =====================================================
# FINALIZE
# =====================================================

df["rating"] = (
    df["rating"]
    .clip(0, 10)
    .round(2)
)


df["pass_accuracy"] = (
    df["pass_accuracy"]
    .round(2)
)

df = df.merge(
    match_info[
        [
            "match_id",
            "home_team",
            "away_team",
            "match_name"
        ]
    ],
    on="match_id",
    how="left"
)

# =====================================================
# SAVE
# =====================================================

output_file = (
    "reports/parquet/"
    "match_analysis/match_player_ratings.parquet"
)

df.to_parquet(
    output_file,
    index=False
)

print("\nSaved:", output_file)

print("\nTop Rated Performances")
print(
    df.sort_values(
        "rating",
        ascending=False
    ).head(20)[
        [
            "player_name",
            "team_name",
            "goals",
            "assists",
            "pass_accuracy",
            "rating"
        ]
    ]
)

conn.close()

ratings = pd.read_parquet(
    "reports/parquet/match_analysis/match_player_ratings.parquet"
)

print(ratings["rating"].describe())