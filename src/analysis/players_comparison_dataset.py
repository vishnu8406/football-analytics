import pandas as pd

attacking = pd.read_csv("reports/csv/player_attacking.csv")
passing = pd.read_csv("reports/csv/player_passes.csv")
creative = pd.read_csv("reports/csv/player_creative.csv")
defensive = pd.read_csv("reports/csv/player_defensive.csv")
discipline = pd.read_csv("reports/csv/player_discipline.csv")
xg = pd.read_csv("reports/csv/player_xG.csv")


attacking = attacking[
    [
        "player_name",
        "goals",
        "assists",
        "shots"
    ]
]

passing = passing[
    [
        "player_name",
        "pass_accuracy",
        "key_passes"
    ]
]

defensive = defensive[
    [
        "player_name",
        "defensive_actions_per_match"
    ]
]


discipline = discipline[
    [
        "player_name",
        "cards_per_match"
    ]
]

xg = xg[
    [
        "player_name",
        "total_xg",
        "finishing_efficiency"
    ]
]


comparison = attacking

comparison = comparison.merge(
    passing,
    on="player_name",
    how="left"
)

comparison = comparison.merge(
    defensive,
    on="player_name",
    how="left"
)

comparison = comparison.merge(
    discipline,
    on="player_name",
    how="left"
)

comparison = comparison.merge(
    xg,
    on="player_name",
    how="left"
)


comparison.to_csv(
    "reports/csv/player_comparison_dataset.csv",
    index=False
)

print("Player comparison dataset created")