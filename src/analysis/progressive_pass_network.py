import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database/football.db")

query = """
WITH progressive_passes AS (
    SELECT
        e.event_id,
        e.match_id,

        t.team_name AS team_name,

        p1.player_name AS passer,
        p2.player_name AS receiver,

        e.location_x AS start_x,
        e.location_y AS start_y,

        pe.end_location_x,
        pe.end_location_y,

        pe.pass_outcome_id

    FROM PassEvents pe

    JOIN Events e
        ON pe.event_id = e.event_id

    JOIN Players p1
        ON e.player_id = p1.player_id

    LEFT JOIN Players p2
        ON pe.recipient_id = p2.player_id

    JOIN Teams t
        ON e.team_id = t.team_id

    WHERE pe.recipient_id IS NOT NULL
),

network AS (
    SELECT
        passer,
        receiver,
        team_name,

        COUNT(*) AS progressive_pass_count,

        SUM(
            CASE
                WHEN pass_outcome_id IS NULL THEN 1
                ELSE 0
            END
        ) AS successful_count,

        AVG(start_x) AS avg_x,
        AVG(start_y) AS avg_y,

        AVG(end_location_x) AS receiver_x,
        AVG(end_location_y) AS receiver_y,

        AVG(
            SQRT(
                POWER(end_location_x - start_x, 2) +
                POWER(end_location_y - start_y, 2)
            )
        ) AS avg_progress_distance

    FROM progressive_passes

    GROUP BY
        passer,
        receiver,
        team_name
)

SELECT *,
       ROUND(
           successful_count * 100.0 /
           progressive_pass_count,
           2
       ) AS success_rate

FROM network

WHERE progressive_pass_count >= 3

ORDER BY progressive_pass_count DESC;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df.head())

df.to_parquet(
    "reports/parquet/progressive_passes/progressive_pass_network.parquet",
    index=False
)

print("Saved: progressive_pass_network.parquet")
print("Rows:", len(df))