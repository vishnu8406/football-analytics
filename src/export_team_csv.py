import sqlite3
import pandas as pd
from pathlib import Path

# Database path
DB_PATH = "data/database/football.db"

# SQL folder
SQL_FOLDER = Path("sql/team_analysis")

# Output folder
OUTPUT_FOLDER = Path("reports/csv/team_analysis")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Connect database
conn = sqlite3.connect(DB_PATH)

for sql_file in SQL_FOLDER.glob("*.sql"):

    print(f"Running {sql_file.name}...")

    with open(sql_file, "r", encoding="utf-8") as f:
        query = f.read()

    try:
        df = pd.read_sql_query(query, conn)

        output_file = OUTPUT_FOLDER / f"{sql_file.stem}.csv"

        df.to_csv(output_file, index=False)

        print(f"Saved -> {output_file}")

    except Exception as e:
        print(f"Error in {sql_file.name}")
        print(e)

conn.close()

print("\nAll team analysis CSV files exported.")