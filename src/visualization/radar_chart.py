import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Load dataset
df = pd.read_csv("reports/csv/player_comparison_dataset.csv")

player_name = "Lionel Andrés Messi Cuccittini"

metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes",
    "total_xg",
    "finishing_efficiency",
    "defensive_actions_per_match"
]

# Normalize metrics
scaler = MinMaxScaler()

df_scaled = df.copy()

df_scaled[metrics] = scaler.fit_transform(df[metrics])

# Select player
player = df_scaled[df_scaled["player_name"] == player_name]

if player.empty:
    print("Player not found")
    exit()

values = player[metrics].iloc[0].tolist()

# Close polygon
values += values[:1]

angles = np.linspace(
    0,
    2 * np.pi,
    len(metrics),
    endpoint=False
).tolist()

angles += angles[:1]

# Plot
fig, ax = plt.subplots(
    figsize=(8, 8),
    subplot_kw=dict(polar=True)
)

ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics)

plt.title(player_name)

plt.tight_layout()

plt.savefig(
    "reports/charts/messi_radar.png",
    dpi=300
)

plt.show()