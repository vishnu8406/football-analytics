import sqlite3
import pandas as pd
from pathlib import Path

"""
"""

def create_connection(
    db_path: str | Path,
) -> sqlite3.Connection:
    """
Create a connection to the SQLite database.

Parameters
----------
db_path : str | Path
    Path to the SQLite database.

Returns
-------
sqlite3.Connection
    Active database connection.
"""
    db_path = Path(db_path)

    try:

        connection = sqlite3.connect(db_path)

        return connection
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Could not connect: {e}")

def load_dataframe(
    df: pd.DataFrame,
    table_name: str,
    connection: sqlite3.Connection,
) -> None:
    """
Load a DataFrame into an existing SQLite table.

Parameters
----------
df : pd.DataFrame
    DataFrame to load into the database.

table_name : str
    Name of the destination table.

connection : sqlite3.Connection
    Active SQLite database connection.

Returns
-------
None
"""
    if not isinstance(df,pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    try:

        df.to_sql(
    table_name,
    connection,
    if_exists="append",
    index=False,
)
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to load '{table_name}': {e}")


def close_connection(connection : sqlite3.Connection) -> None:
    if connection:
        connection.close()

        