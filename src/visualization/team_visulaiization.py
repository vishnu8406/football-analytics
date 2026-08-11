from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]

csv_path = BASE_DIR / "reports" / "csv" / "points_table.csv"
output_dir = BASE_DIR / "reports" / "images" / "team"

output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(csv_path)

# Points Table
plt.figure(figsize=(12,6))
plt.bar(df["team_name"], df["points"])
plt.xticks(rotation=45)
plt.title("League Points")
plt.tight_layout()

plt.savefig(output_dir / "points_table.png")
plt.close()

# Goal Difference
plt.figure(figsize=(12,6))
plt.bar(df["team_name"], df["goal_difference"])
plt.xticks(rotation=45)
plt.title("Goal Difference")
plt.tight_layout()

plt.savefig(output_dir / "goal_difference.png")
plt.close()

# Win Percentage
plt.figure(figsize=(12,6))
plt.bar(df["team_name"], df["win_percentage"])
plt.xticks(rotation=45)
plt.title("Win Percentage")
plt.tight_layout()

plt.savefig(output_dir / "win_percentage.png")
plt.close()

print("Team charts generated")