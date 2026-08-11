import pandas as pd

# ==========================================
# LOAD FILES
# ==========================================

overall = pd.read_csv("reports/csv/player_attacking.csv")

passing = pd.read_csv("reports/csv/player_passes.csv")

creativity = pd.read_csv("reports/csv/player_creative.csv")

defensive = pd.read_csv("reports/csv/player_defensive.csv")

discipline = pd.read_csv("reports/csv/player_discipline.csv")

xg = pd.read_csv("reports/csv/player_xG.csv")

# ==========================================
# START WITH OVERALL PERFORMANCE
# ==========================================

radar = overall.copy()

# ==========================================
# PASSING
# ==========================================

passing_cols = [
    "player_name",
    "passes_per_match",
    "key_passes",
    "long_passes"
]

radar = radar.merge(
    passing[passing_cols],
    on="player_name",
    how="left"
)

# ==========================================
# CREATIVITY
# ==========================================

creativity_cols = [
    "player_name",
    "key_passes_per_match",
    "assists_per_match",
    "assist_conversion_percentage"
]

radar = radar.merge(
    creativity[creativity_cols],
    on="player_name",
    how="left"
)

# ==========================================
# DEFENSIVE
# ==========================================
print(defensive.columns.tolist())
defensive_cols = [
    "player_name",
    "tackles_won",
    "interceptions",
    "recoveries",
    "clearances",
    "blocks",
    "defensive_actions_per_match"
]

radar = radar.merge(
    defensive[defensive_cols],
    on="player_name",
    how="left"
)

# ==========================================
# DISCIPLINE
# ==========================================

discipline_cols = [
    "player_name",
    "yellow_cards",
    "red_cards",
    "cards_per_match"
]

radar = radar.merge(
    discipline[discipline_cols],
    on="player_name",
    how="left"
)

# ==========================================
# XG
# ==========================================

xg_cols = [
    "player_name",
    "total_xg",
    "xg_per_match",
    "avg_xg_per_shot",
    "goals_minus_xg",
    "finishing_efficiency"
]

radar = radar.merge(
    xg[xg_cols],
    on="player_name",
    how="left"
)

# ==========================================
# CLEANING
# ==========================================

numeric_cols = radar.select_dtypes(include="number").columns

radar[numeric_cols] = radar[numeric_cols].fillna(0)

radar[numeric_cols] = radar[numeric_cols].round(2)

# ==========================================
# SAVE
# ==========================================

radar.to_csv(
    "reports/player_radar_dataset.csv",
    index=False
)

print("Player Radar Dataset Created")
print(f"Players: {len(radar)}")

print("\nColumns:")
print(radar.columns.tolist())

print("\nPreview:")
print(radar.head())