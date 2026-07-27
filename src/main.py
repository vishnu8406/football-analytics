from config import MATCHES_PATH, LINEUPS_PATH,EVENTS_PATH, DATABASE_PATH

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
    transform_body_parts,
    transform_event_types,
    transform_events,
    transform_pass_events,
    transform_pass_heights,
    transform_pass_outcomes,
    transform_pass_types,
    transform_play_pattern
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
        event_files = extract_match_files(EVENTS_PATH,match_ids)
        print("EXTRACTION FINISHES")

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

        #----------------------------------
        #Transform Events
        #----------------------------------
        event_types_df = transform_event_types(event_files)
        play_patterns_df = transform_play_pattern(event_files)
        pass_heights_df = transform_pass_heights(event_files)
        pass_types_df = transform_pass_types(event_files)
        body_parts_df = transform_body_parts(event_files)
        pass_outcomes_df = transform_pass_outcomes(event_files)
        events_df = transform_events(event_files)
        pass_events_df = transform_pass_events(event_files)
        print("transform finished")




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

        #-----------------------------------
        # Load Events and Pass Events
        #-----------------------------------



        load_dataframe(event_types_df, "EventTypes", connection)

        load_dataframe(play_patterns_df, "PlayPatterns", connection)

        load_dataframe(pass_heights_df, "PassHeights", connection)

        load_dataframe(pass_types_df, "PassTypes", connection)

        load_dataframe(body_parts_df, "BodyParts", connection)

        load_dataframe(pass_outcomes_df, "PassOutcomes", connection)
        print("Missing Matches:")
        print(set(events_df["match_id"]) - set(matches_table_df["match_id"]))

        print("Missing Teams:")
        print(set(events_df["team_id"]) - set(teams_df["team_id"]))

        print("Missing Players:")
        print(set(events_df["player_id"].dropna().astype(int)) - set(players_df["player_id"]))

        print("Missing Positions:")
        print(set(events_df["position_id"].dropna().astype(int)) - set(positions_df["position_id"]))

        print("Missing Event Types:")
        print(set(events_df["event_type_id"]) - set(event_types_df["event_type_id"]))

        print("Missing Play Patterns:")
        print(set(events_df["play_pattern_id"]) - set(play_patterns_df["play_pattern_id"]))

        load_dataframe(events_df, "Events", connection)

        load_dataframe(pass_events_df, "PassEvents", connection)

        print("✅ ETL pipeline completed successfully.")

    finally:
        close_connection(connection)


if __name__ == "__main__":
    main()