from config import MATCHES_PATH, LINEUPS_PATH, DATABASE_PATH

from etl.extract import (
    extract,
    extract_match_files,
)

from etl.transform import (
    transform_teams,
    transform_stadiums,
    transform_referees,
    transform_competitions,
    transform_seasons,
    transform_matches,
    transform_players,
    transform_positions,
    transform_match_players,
    transform_players_positions,
)

from etl.load import (
    create_connection,
    load_dataframe,
    close_connection,
)

from database.schema import create_tables


def main() -> None:
    """
    Run the complete ETL pipeline.
    """

    connection = create_connection(DATABASE_PATH)

    try:
        # ----------------------------------
        # Create Database Schema
        # ----------------------------------
        create_tables(connection)

        # ----------------------------------
        # Extract Match Data
        # ----------------------------------
        matches_df = extract(MATCHES_PATH)

        match_ids = matches_df["match_id"].tolist()

        lineup_files = extract_match_files(
            LINEUPS_PATH,
            match_ids,
        )

        # ----------------------------------
        # Transform Match Tables
        # ----------------------------------
        teams_df = transform_teams(matches_df)
        stadiums_df = transform_stadiums(matches_df)
        referees_df = transform_referees(matches_df)
        competitions_df = transform_competitions(matches_df)
        seasons_df = transform_seasons(matches_df)
        matches_table_df = transform_matches(matches_df)

        # ----------------------------------
        # Transform Lineup Tables
        # ----------------------------------
        players_df = transform_players(lineup_files)
        positions_df = transform_positions(lineup_files)
        match_players_df = transform_match_players(lineup_files)
        player_positions_df = transform_players_positions(lineup_files)

        # ----------------------------------
        # Load Match Tables
        # ----------------------------------
        load_dataframe(competitions_df, "Competitions", connection)
        load_dataframe(seasons_df, "Seasons", connection)
        load_dataframe(teams_df, "Teams", connection)
        load_dataframe(stadiums_df, "Stadiums", connection)
        load_dataframe(referees_df, "Referees", connection)
        load_dataframe(matches_table_df, "Matches", connection)

        # ----------------------------------
        # Load Lineup Tables
        # ----------------------------------
        load_dataframe(players_df, "Players", connection)
        load_dataframe(positions_df, "Positions", connection)
        load_dataframe(match_players_df, "MatchPlayers", connection)
        load_dataframe(player_positions_df, "PlayerPositions", connection)

        print("✅ ETL pipeline completed successfully.")

    finally:
        close_connection(connection)


if __name__ == "__main__":
    main()