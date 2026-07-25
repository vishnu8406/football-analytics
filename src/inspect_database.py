import pandas as pd

competitions = pd.read_json("data/raw/competitions.json")


matchs = pd.read_json("data/raw/matches/27.json")

print(matchs.loc[0, "metadata"])

