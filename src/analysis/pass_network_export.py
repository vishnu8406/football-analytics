import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database/football.db")

query = """
SELECT
    e.match_id,
    e.team_id,
    t.team_name,

    passer.player_name AS passer,
    receiver.player_name AS receiver,

    e.location_x,
    e.location_y,

    pe.end_location_x,
    pe.end_location_y,

    pe.pass_length

FROM PassEvents pe

JOIN Events e
ON pe.event_id = e.event_id

JOIN Teams t
ON e.team_id = t.team_id

JOIN Players passer
ON e.player_id = passer.player_id

JOIN Players receiver
ON pe.recipient_id = receiver.player_id

WHERE
    e.player_id IS NOT NULL
    AND pe.recipient_id IS NOT NULL
"""

df = pd.read_sql(query, conn)

df.to_csv(
    "reports/csv/pass_network.csv",
    index=False
)

print(df.head())

conn.close()