from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

csv_dir = BASE_DIR / "reports" / "csv"

attacking = pd.read_csv(csv_dir / "player_attacking.csv")

passing = pd.read_csv(csv_dir / "player_passes.csv")[
    [
        "player_name",
        "passes_per_match",
        "long_passes"
    ]
]

creative = pd.read_csv(csv_dir / "player_creative.csv")[
    [
        "player_name",
        "key_passes",
        "key_passes_per_match",
        "assists_per_match",
        "assist_conversion_percentage"
    ]
]

defensive = pd.read_csv(csv_dir / "player_defensive.csv")[
    [
        "player_name",
        "tackles_won",
        "interceptions",
        "recoveries",
        "clearances",
        "blocks",
        "total_defensive_actions",
        "defensive_actions_per_match"
    ]
]

xg = pd.read_csv(csv_dir / "player_xG.csv")[
    [
        "player_name",
        "total_xg",
        "xg_per_match",
        "avg_xg_per_shot",
        "goals_minus_xg",
        "finishing_efficiency"
    ]
]

master = attacking.merge(
    passing,
    on="player_name",
    how="left"
)

master = master.merge(
    creative,
    on="player_name",
    how="left"
)

master = master.merge(
    defensive,
    on="player_name",
    how="left"
)

master = master.merge(
    xg,
    on="player_name",
    how="left"
)

master.to_csv(
    csv_dir / "player_master.csv",
    index=False
)

print(master.columns.tolist())
print(master.head())