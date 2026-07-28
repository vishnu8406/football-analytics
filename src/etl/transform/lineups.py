import pandas as pd 

def transform_players(
    match_files: list[dict]
) -> pd.DataFrame:
    """
    Transform extracted lineup data into a Players table.

    Parameters
    ----------
    match_files : list[dict]
        List of extracted lineup JSON files.

    Returns
    -------
    pd.DataFrame
        Players table containing one row per unique player.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(match_files, list):
        raise TypeError("Input must be a list.")

    if not match_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    players = []

    for match in match_files:

        for team in match["data"]:

            for player in team["lineup"]:
                country = player.get("country", {})

                row_data = {
                    "player_id": player["player_id"],
                    "player_name": player["player_name"],
                    "player_nickname": player["player_nickname"],
                    
                    "country_id": country.get("id"),
                    "country_name": country.get("name"),
                }

                players.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    players_df = pd.DataFrame(players)

    players_df = (
        players_df
        .drop_duplicates(subset=["player_id"])
        .sort_values("player_id")
        .reset_index(drop=True)
    )

    return players_df

def transform_match_players(
    match_files: list[dict]
) -> pd.DataFrame:
    """
    Transform extracted lineup data into a MatchPlayers table.

    Parameters
    ----------
    match_files : list[dict]
        List of extracted lineup JSON files.

    Returns
    -------
    pd.DataFrame
        MatchPlayers table containing one row per player appearance.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(match_files, list):
        raise TypeError("Input must be a list.")

    if not match_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    match_players = []

    for match in match_files:

        for team in match["data"]:

            for player in team["lineup"]:

                row_data = {
                    "match_id": match["match_id"],
                    "team_id": team["team_id"],
                    "player_id": player["player_id"],
                    "jersey_number": player["jersey_number"],
                }

                match_players.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    match_players_df = pd.DataFrame(match_players)

    match_players_df = (
        match_players_df
        .sort_values(["match_id", "team_id", "player_id"])
        .reset_index(drop=True)
    )

    return match_players_df



def transform_players_positions(
    match_files: list[dict]
) -> pd.DataFrame:
    """
    Transform extracted lineup data into a player position table.

    Parameters
    ----------
    match_files : list[dict]
        List of extracted lineup JSON files.

    Returns
    -------
    pd.DataFrame
        Player position table containing one row per player position in the Match
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(match_files, list):
        raise TypeError("Input must be a list.")

    if not match_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    player_positions = []

    for match in match_files:

        for team in match["data"]:

            for player in team["lineup"]:

                for position in player["positions"]:

                    row_data = {
                        "match_id": match["match_id"],
                        "player_id": player["player_id"],

                        "position_id": position["position_id"],
                        "position_name": position["position"],

                        "from_time": position["from"],
                        "to_time": position["to"],

                        "from_period": position["from_period"],
                        "to_period": position["to_period"],

                        "start_reason": position["start_reason"],
                        "end_reason": position["end_reason"],
                    }

                    player_positions.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    player_position_df = pd.DataFrame(player_positions)

    player_position_df = (
        player_position_df
        .sort_values(["match_id", "player_id","position_id"])
        .reset_index(drop=True)
    )
    return player_position_df

def transform_positions(
    lineup_files: list[dict],
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted lineup and event data into the Positions table.

    Parameters
    ----------
    lineup_files : list[dict]
        List of extracted lineup JSON files.

    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        Positions table containing one row per unique position.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(lineup_files, list):
        raise TypeError("lineup_files must be a list.")

    if not isinstance(event_files, list):
        raise TypeError("event_files must be a list.")

    if not lineup_files:
        raise ValueError("lineup_files is empty.")

    if not event_files:
        raise ValueError("event_files is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    positions = []

    # -----------------------------
    # Positions from lineups
    # -----------------------------
    for match in lineup_files:

        for team in match["data"]:

            for player in team["lineup"]:

                for position in player["positions"]:

                    row_data = {
                        "position_id": position["position_id"],
                        "position_name": position["position"],
                    }

                    positions.append(row_data)

    # -----------------------------
    # Positions from events
    # -----------------------------
    for match in event_files:

        for event in match["data"]:

            position = event.get("position", {})

            if not position:
                continue

            row_data = {
                "position_id": position.get("id"),
                "position_name": position.get("name"),
            }

            positions.append(row_data)

            # Goalkeeper-specific position (if present)
            goalkeeper = event.get("goalkeeper", {})
            goalkeeper_position = goalkeeper.get("position", {})

            if goalkeeper_position:

                row_data = {
                    "position_id": goalkeeper_position.get("id"),
                    "position_name": goalkeeper_position.get("name"),
                }

                positions.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    positions_df = (
        pd.DataFrame(positions)
        .drop_duplicates(subset=["position_id"])
        .sort_values("position_id")
        .reset_index(drop=True)
    )

    return positions_df
