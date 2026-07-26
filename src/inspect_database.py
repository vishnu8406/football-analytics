import pandas as pd
from pathlib import Path
from etl.transform import (transform_seasons,transform_players_positions,transform_positions, transform_competitions,transform_players,transform_match_players)
from etl.extract import extract_match_files
competitions = pd.read_json("data/raw/competitions.json")


matches_df = pd.read_json("data/raw/matches/27.json")
match_ids = matches_df["match_id"].tolist()
match_folder = "data/raw/lineups"

match_files = extract_match_files(match_folder,match_ids)

players_df = transform_players_positions(match_files)

print(players_df.head())