import sqlite3
import pandas as pd
from pathlib import Path

# ----------------------------------
# Configuration
# ----------------------------------

DB_PATH = "data/database/football.db"

OUTPUT_DIR = Path(
    "reports/parquet/progressive_passes"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------
# Connect Database
# ----------------------------------

conn = sqlite3.connect(DB_PATH)

# ----------------------------------
# Extract Pass Events
# ----------------------------------

query = """
SELECT
    e.event_id,
    e.match_id,
    e.minute,

    p.player_name,
    t.team_name,

    e.location_x,
    e.location_y,

    pe.end_location_x,
    pe.end_location_y,

    pe.pass_outcome_id

FROM Events e

JOIN PassEvents pe
    ON e.event_id = pe.event_id

JOIN Players p
    ON e.player_id = p.player_id

JOIN Teams t
    ON e.team_id = t.team_id
"""

df = pd.read_sql(query, conn)

print(f"Loaded {len(df):,} passes")

# ----------------------------------
# Progressive Distance
# ----------------------------------

df["progress_distance"] = (
    df["end_location_x"]
    - df["location_x"]
)

# ----------------------------------
# Progressive Pass Definition
# ----------------------------------

PROGRESSIVE_THRESHOLD = 10

progressive = df[
    df["progress_distance"]
    >= PROGRESSIVE_THRESHOLD
].copy()

print(
    f"Progressive Passes: {len(progressive):,}"
)

# ----------------------------------
# Pass Completion
# ----------------------------------

progressive["successful"] = (
    progressive["pass_outcome_id"]
    .isna()
)

# ----------------------------------
# Save Event-Level Dataset
# ----------------------------------

progressive.to_parquet(
    OUTPUT_DIR / "progressive_passes.parquet",
    index=False
)

# ----------------------------------
# Player Metrics
# ----------------------------------

player_stats = (
    progressive
    .groupby(
        ["player_name", "team_name"]
    )
    .agg(
        progressive_passes=(
            "event_id",
            "count"
        ),
        successful_progressive_passes=(
            "successful",
            "sum"
        ),
        avg_progress_distance=(
            "progress_distance",
            "mean"
        ),
        max_progress_distance=(
            "progress_distance",
            "max"
        )
    )
    .reset_index()
)

player_stats["success_rate"] = (
    player_stats[
        "successful_progressive_passes"
    ]
    /
    player_stats[
        "progressive_passes"
    ]
    * 100
)

player_stats = player_stats.sort_values(
    "progressive_passes",
    ascending=False
)

player_stats.to_parquet(
    OUTPUT_DIR /
    "player_progressive_passes.parquet",
    index=False
)

# ----------------------------------
# Team Metrics
# ----------------------------------

team_stats = (
    progressive
    .groupby("team_name")
    .agg(
        progressive_passes=(
            "event_id",
            "count"
        ),
        successful_progressive_passes=(
            "successful",
            "sum"
        ),
        avg_progress_distance=(
            "progress_distance",
            "mean"
        )
    )
    .reset_index()
)

team_stats["success_rate"] = (
    team_stats[
        "successful_progressive_passes"
    ]
    /
    team_stats[
        "progressive_passes"
    ]
    * 100
)

team_stats = team_stats.sort_values(
    "progressive_passes",
    ascending=False
)

team_stats.to_parquet(
    OUTPUT_DIR /
    "team_progressive_passes.parquet",
    index=False
)

# ----------------------------------
# Summary
# ----------------------------------

print("\nTop Players")

print(
    player_stats[
        [
            "player_name",
            "team_name",
            "progressive_passes"
        ]
    ]
    .head(10)
)

print("\nTop Teams")

print(
    team_stats[
        [
            "team_name",
            "progressive_passes"
        ]
    ]
    .head(10)
)

print("\nFiles Created")

print(
    OUTPUT_DIR /
    "progressive_passes.parquet"
)

print(
    OUTPUT_DIR /
    "player_progressive_passes.parquet"
)

print(
    OUTPUT_DIR /
    "team_progressive_passes.parquet"
)

conn.close()

