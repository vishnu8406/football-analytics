import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/database/football.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    p.player_name,
    e.match_id,
    e.minute,
    e.event_type_id,
    e.location_x,
    e.location_y
FROM events e
JOIN players p
    ON e.player_id = p.player_id
WHERE e.location_x IS NOT NULL
AND e.location_y IS NOT NULL
AND e.player_id IS NOT NULL
"""

heatmap = pd.read_sql(query, conn)

output_dir = Path("reports/csv")
output_dir.mkdir(parents=True, exist_ok=True)

heatmap.to_csv(
    output_dir / "player_heatmap.csv",
    index=False
)

print(f"Rows exported: {len(heatmap):,}")
print("Saved: reports/csv/player_heatmap.csv")

conn.close()