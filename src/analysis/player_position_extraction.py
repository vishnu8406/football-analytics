import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database/football.db")

df = pd.read_sql(
    "SELECT * FROM PlayerPositions LIMIT 10",
    conn
)

print(df.columns.tolist())
print(df.head())