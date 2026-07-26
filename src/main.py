from config import MATCHES_PATH, DATABASE_PATH

from etl.extract import extract
from etl.transform import (
    transform_teams,
    transform_stadiums,
    transform_referees,
    transform_competitions,
    transform_seasons,
    transform_matches,
)

from etl.load import (
    create_connection,
    load_dataframe,
    close_connection,
)

from database.schema import create_tables


def main():
    """
    Run the complete ETL pipeline.

    Steps
    -----
    1. Connect to the database.
    2. Create database tables.
    3. Extract raw data.
    4. Transform data into normalized tables.
    5. Load tables into SQLite.
    6. Close the database connection.
    """

    # ----------------------------------
    # Database
    # ----------------------------------
    connection = create_connection(DATABASE_PATH)
    create_tables(connection)

    # ----------------------------------
    # Extract
    # ----------------------------------
    matches_df = extract(MATCHES_PATH)

    # ----------------------------------
    # Transform
    # ----------------------------------
    teams = transform_teams(matches_df)
    stadiums = transform_stadiums(matches_df)
    referees = transform_referees(matches_df)
    competitions = transform_competitions(matches_df)
    seasons = transform_seasons(matches_df)
    matches = transform_matches(matches_df)

    # ----------------------------------
    # Load
    # ----------------------------------
    load_dataframe(teams, "Teams", connection)
    load_dataframe(stadiums, "Stadiums", connection)
    load_dataframe(referees, "Referees", connection)
    load_dataframe(competitions, "Competitions", connection)
    load_dataframe(seasons, "Seasons", connection)
    load_dataframe(matches, "Matches", connection)

    # ----------------------------------
    # Close Connection
    # ----------------------------------
    close_connection(connection)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()