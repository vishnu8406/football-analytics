import pandas as pd

from pathlib import Path
from etl.transform import (transform_goalkeeper_types,
    transform_goalkeeper_techniques,
    transform_goalkeeper_outcomes,
    transform_goalkeeper_events,transform_events,transform_positions,transform_body_parts
)
# from etl.extract import extract_match_files
# competitions = pd.read_json("data/raw/competitions.json")


# matches_df = pd.read_json("data/raw/matches/27.json")
# match_ids = matches_df["match_id"].tolist()
# match_folder = "data/raw/lineups"
# event_folder = "data/raw/events"
# lineup_files = extract_match_files(match_folder,match_ids)
# event_files = extract_match_files(event_folder,match_ids)


formation =pd.read_parquet("reports/parquet/match_analysis/player_position.parquet")
lineups = pd.read_parquet("reports/parquet/match_analysis/match_lineups.parquet")

ratings = pd.read_parquet("reports/parquet/match_analysis/match_player_ratings.parquet")
formation = formation.drop_duplicates(
    subset=[
        "match_id",
        "team_name",
        "player_name"
    ]
)
print("FORMATION")
print(formation.columns.tolist())

print("\nLINEUPS")
print(lineups.columns.tolist())

print("\nRATINGS")
print(ratings.columns.tolist())


# print("extraction finished")
# print("Missing Events:")
# events_df = transform_events(event_files)
# for match in event_files:
#     for event in match["data"]:
#         goalkeeper = event.get("goalkeeper", {})
#         body_part = goalkeeper.get("body_part", {})

#         if body_part.get("id") == 35:
#             print(body_part)
#             raise SystemExit
# goalkeeper_outcomes_df = transform_goalkeeper_outcomes(event_files)
# goalkeeper_types_df = transform_goalkeeper_types(event_files)
# goalkeeper_techniques_df = transform_goalkeeper_techniques(event_files)
# goalkeeper_events_df = transform_goalkeeper_events(event_files)
# positions_df = transform_positions(lineup_files,event_files)
# body_parts_df = transform_body_parts(event_files)


# print(positions_df[positions_df["position_id"] == 44])

# print(body_parts_df[body_parts_df["body_part_id"] == 35])

# print(goalkeeper_outcomes_df[goalkeeper_outcomes_df["goalkeeper_outcome_id"] == 52])

# print(goalkeeper_types_df[goalkeeper_types_df["goalkeeper_type_id"] == 33])

# print(goalkeeper_techniques_df[goalkeeper_techniques_df["goalkeeper_technique_id"] == 46])