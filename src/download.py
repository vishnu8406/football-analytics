"""
Extract all available La Liga data from the StatsBomb Open Data repository.

Folder structure created:

data/
│
└── raw/
    ├── competitions.json
    ├── matches/
    ├── events/
    └── lineups/
"""

import json
import shutil
from pathlib import Path

# ==========================================================
# CHANGE THIS TO YOUR STATSBOMB OPEN-DATA/data DIRECTORY
# Example:
# SOURCE = Path("/home/vishnu/Downloads/open-data/data")
# ==========================================================

SOURCE = Path("/path/to/open-data/data")

# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW = PROJECT_ROOT / "data" / "raw"

MATCH_DIR = RAW / "matches"
EVENT_DIR = RAW / "events"
LINEUP_DIR = RAW / "lineups"

MATCH_DIR.mkdir(parents=True, exist_ok=True)
EVENT_DIR.mkdir(parents=True, exist_ok=True)
LINEUP_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------

print("Loading competitions...")

with open(SOURCE / "competitions.json", encoding="utf-8") as f:
    competitions = json.load(f)

laliga = [
    c for c in competitions
    if c["competition_name"] == "La Liga"
]

print(f"\nFound {len(laliga)} La Liga seasons:\n")

for season in laliga:
    print(
        f"{season['season_name']:>12}    "
        f"Season ID: {season['season_id']}"
    )

# Copy competitions file
shutil.copy2(
    SOURCE / "competitions.json",
    RAW / "competitions.json"
)

total_matches = 0
total_events = 0

print("\nExtracting...\n")

for season in laliga:

    season_id = season["season_id"]

    season_file = (
        SOURCE
        / "matches"
        / str(season["competition_id"])
        / f"{season_id}.json"
    )

    if not season_file.exists():
        print(f"Skipping missing season {season_id}")
        continue

    shutil.copy2(
        season_file,
        MATCH_DIR / season_file.name
    )

    with open(season_file, encoding="utf-8") as f:
        matches = json.load(f)

    total_matches += len(matches)

    for match in matches:

        match_id = str(match["match_id"])

        event_file = (
            SOURCE
            / "events"
            / f"{match_id}.json"
        )

        lineup_file = (
            SOURCE
            / "lineups"
            / f"{match_id}.json"
        )

        if event_file.exists():
            shutil.copy2(
                event_file,
                EVENT_DIR / event_file.name
            )
            total_events += 1

        if lineup_file.exists():
            shutil.copy2(
                lineup_file,
                LINEUP_DIR / lineup_file.name
            )

print("\n======================================")
print("Extraction Complete")
print("======================================")
print(f"La Liga Seasons : {len(laliga)}")
print(f"Matches         : {total_matches}")
print(f"Event Files     : {total_events}")
print(f"Output Folder   : {RAW}")
print("======================================")