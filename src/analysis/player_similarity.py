import pandas as pd

df = pd.read_parquet(
    "reports/parquet/player_comparison_dataset.parquet"
)

print(df.columns.tolist())
print(df.head())