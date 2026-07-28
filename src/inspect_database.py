import pandas as pd

from pathlib import Path
from etl.transform import (transform_pass_heights)
from etl.extract import extract_match_files
competitions = pd.read_json("data/raw/competitions.json")


matches_df = pd.read_json("data/raw/matches/27.json")
match_ids = matches_df["match_id"].tolist()
match_folder = "data/raw/events"


events = extract_match_files(match_folder, match_ids)
print("extraction finished")
shot_keys = set()

for match in events:
    for events in match["data"]:
        shot = events.get("shot")
        if shot:
            shot_keys.update(shot.keys())

print(sorted(shot_keys))