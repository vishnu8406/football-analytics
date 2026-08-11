import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================
# CONFIG
# ==========================================

DB_PATH = "data/database/football.db"   # update if needed

OUTPUT_DIR = Path("reports/csv/match_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# ==========================================
# MATCH SUMMARY
# ==========================================

match_summary = pd.read_sql(
    """
    SELECT
        m.match_id,
        ht.team_name AS home_team,
        at.team_name AS away_team,
        m.home_score,
        m.away_score,
        m.match_week,
        m.match_date,
        m.kick_off
    FROM Matches m
    JOIN Teams ht
        ON m.home_team_id = ht.team_id
    JOIN Teams at
        ON m.away_team_id = at.team_id
    """,
    conn
)

match_summary.to_csv(
    OUTPUT_DIR / "match_summary.csv",
    index=False
)

print("✓ match_summary.csv")


# ==========================================
# MATCH LINEUPS
# ==========================================

match_lineups = pd.read_sql(
    """
    SELECT
        mp.match_id,
        t.team_name,
        p.player_name,
        mp.jersey_number
    FROM MatchPlayers mp
    JOIN Players p
        ON mp.player_id = p.player_id
    JOIN Teams t
        ON mp.team_id = t.team_id
    """,
    conn
)

match_lineups.to_csv(
    OUTPUT_DIR / "match_lineups.csv",
    index=False
)

print("✓ match_lineups.csv")


# ==========================================
# MATCH EVENTS
# ==========================================

match_events = pd.read_sql(
    """
    SELECT
        e.event_id,
        e.match_id,
        e.minute,
        e.second,
        t.team_name,
        p.player_name,
        et.event_type_name
    FROM Events e
    LEFT JOIN Teams t
        ON e.team_id = t.team_id
    LEFT JOIN Players p
        ON e.player_id = p.player_id
    LEFT JOIN EventTypes et
        ON e.event_type_id = et.event_type_id
    """
    ,
    conn
)

match_events.to_csv(
    OUTPUT_DIR / "match_events.csv",
    index=False
)

print("✓ match_events.csv")


# ==========================================
# SHOT EVENTS
# ==========================================

match_shots = pd.read_sql(
    """
    SELECT
        e.event_id,
        e.match_id,
        e.minute,
        e.second,
        t.team_name,
        p.player_name,
        e.location_x,
        e.location_y,
        s.statsbomb_xg,
        so.shot_outcome_name
    FROM Events e

    JOIN ShotEvents s
        ON e.event_id = s.event_id

    LEFT JOIN Players p
        ON e.player_id = p.player_id

    LEFT JOIN Teams t
        ON e.team_id = t.team_id

    LEFT JOIN ShotOutcomes so
        ON s.shot_outcome_id = so.shot_outcome_id
    """,
    conn
)

match_shots.to_csv(
    OUTPUT_DIR / "match_shots.csv",
    index=False
)

print("✓ match_shots.csv")


# ==========================================
# SUBSTITUTIONS
# ==========================================

substitutions = pd.read_sql(
    """
    SELECT
        e.match_id,
        e.minute,
        e.second,
        t.team_name,
        p.player_name AS player_off,
        rp.player_name AS player_on
    FROM SubstitutionEvents se

    JOIN Events e
        ON se.event_id = e.event_id

    LEFT JOIN Players p
        ON e.player_id = p.player_id

    LEFT JOIN Players rp
        ON se.replacement_player_id = rp.player_id

    LEFT JOIN Teams t
        ON e.team_id = t.team_id
    """,
    conn
)

substitutions.to_csv(
    OUTPUT_DIR / "substitutions.csv",
    index=False
)

print("✓ substitutions.csv")


# ==========================================
# CARDS
# ==========================================

cards = pd.read_sql(
    """
    SELECT
        e.match_id,
        e.minute,
        e.second,
        t.team_name,
        p.player_name,
        c.card_name
    FROM BadBehaviourEvents bb

    JOIN Events e
        ON bb.event_id = e.event_id

    LEFT JOIN Players p
        ON e.player_id = p.player_id

    LEFT JOIN Teams t
        ON e.team_id = t.team_id

    LEFT JOIN Cards c
        ON bb.card_id = c.card_id
    """,
    conn
)

cards.to_csv(
    OUTPUT_DIR / "cards.csv",
    index=False
)

print("✓ cards.csv")


# ==========================================
# GOALKEEPER EVENTS
# ==========================================

goalkeeper_events = pd.read_sql(
    """
    SELECT
        e.match_id,
        e.minute,
        e.second,
        t.team_name,
        p.player_name,
        gt.goalkeeper_type_name
    FROM GoalkeeperEvents g

    JOIN Events e
        ON g.event_id = e.event_id

    LEFT JOIN Players p
        ON e.player_id = p.player_id

    LEFT JOIN Teams t
        ON e.team_id = t.team_id

    LEFT JOIN GoalkeeperTypes gt
        ON g.goalkeeper_type_id = gt.goalkeeper_type_id
    """,
    conn
)

goalkeeper_events.to_csv(
    OUTPUT_DIR / "goalkeeper_events.csv",
    index=False
)

print("✓ goalkeeper_events.csv")


# ==========================================
# FINISH
# ==========================================

conn.close()

print("\nAll Match Analysis CSVs Exported Successfully")