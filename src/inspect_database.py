import pandas as pd

from etl.transform import (transform_seasons,transform_competitions)

competitions = pd.read_json("data/raw/competitions.json")


matches_df = pd.read_json("data/raw/matches/27.json")

print(transform_competitions(matches_df))