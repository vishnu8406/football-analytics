from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    BASE_DIR / "reports/csv/player_master.csv"
)

player1 = "Lionel Andrés Messi Cuccittini"
player2 = "Cristiano Ronaldo dos Santos Aveiro"

p1 = df[df["player_name"] == player1].iloc[0]
p2 = df[df["player_name"] == player2].iloc[0]

metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes",
    "total_xg"
]

print("\nPLAYER COMPARISON\n")

for metric in metrics:

    v1 = p1[metric]
    v2 = p2[metric]

    print(f"{metric}")
    print(f"{player1[:20]:20} : {v1}")
    print(f"{player2[:20]:20} : {v2}")
    print("-"*40)
import matplotlib.pyplot as plt

metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes",
    "total_xg"
]

p1_values = [p1[m] for m in metrics]
p2_values = [p2[m] for m in metrics]

x = range(len(metrics))

plt.figure(figsize=(10,6))

plt.bar(
    [i-0.2 for i in x],
    p1_values,
    width=0.4,
    label="Player 1"
)

plt.bar(
    [i+0.2 for i in x],
    p2_values,
    width=0.4,
    label="Player 2"
)

plt.xticks(x, metrics, rotation=45)

plt.legend()

plt.tight_layout()

plt.savefig(
    BASE_DIR /
    "reports/images/comparison/comparison.png"
)

plt.close()