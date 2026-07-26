import pandas as pd


def transform_teams(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique teams from the matches DataFrame.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Raw matches DataFrame returned by extract().

    Returns
    -------
    pd.DataFrame
        DataFrame containing unique teams.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"home_team", "away_team"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Home Teams
    # -----------------------------
    home_teams = (
        matches_df["home_team"]
        .apply(pd.Series)[["home_team_id", "home_team_name"]]
        .rename(
            columns={
                "home_team_id": "team_id",
                "home_team_name": "team_name",
            }
        )
    )

    # -----------------------------
    # Away Teams
    # -----------------------------
    away_teams = (
        matches_df["away_team"]
        .apply(pd.Series)[["away_team_id", "away_team_name"]]
        .rename(
            columns={
                "away_team_id": "team_id",
                "away_team_name": "team_name",
            }
        )
    )

    # -----------------------------
    # Combine
    # -----------------------------
    teams_df = pd.concat(
        [home_teams, away_teams],
        ignore_index=True,
    )

    teams_df = (
        teams_df
        .drop_duplicates(subset=["team_id"])
        .sort_values("team_id")
        .reset_index(drop=True)
    )

    return teams_df


def transform_stadiums(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique stadiums from the matches DataFrame.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"stadium"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Transformation
    # -----------------------------
    stadiums_df = (
        matches_df["stadium"]
        .dropna()
        .apply(pd.Series)[["id", "name"]]
        .rename(
            columns={
                "id": "stadium_id",
                "name": "stadium_name",
            }
        )
        .drop_duplicates(subset=["stadium_id"])
        .sort_values("stadium_id")
        .reset_index(drop=True)
    )

    return stadiums_df


def transform_referees(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique referees from the matches DataFrame.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"referee"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Transformation
    # -----------------------------
    referees_df = (
        matches_df["referee"]
        .dropna()
        .apply(pd.Series)[["id", "name"]]
        .rename(
            columns={
                "id": "referee_id",
                "name": "referee_name",
            }
        )
        .drop_duplicates(subset=["referee_id"])
        .sort_values("referee_id")
        .reset_index(drop=True)
    )

    return referees_df


def transform_matches(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the matches DataFrame into the Matches table.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {
        "match_id",
        "competition",
        "season",
        "home_team",
        "away_team",
        "stadium",
        "home_score",
        "away_score",
    }

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Extract nested IDs
    # -----------------------------
    competition_id = (
        matches_df["competition"]
        .apply(pd.Series)["competition_id"]
        .rename("competition_id")
    )

    season_id = (
        matches_df["season"]
        .apply(pd.Series)["season_id"]
        .rename("season_id")
    )

    home_team_id = (
        matches_df["home_team"]
        .apply(pd.Series)["home_team_id"]
        .rename("home_team_id")
    )

    away_team_id = (
        matches_df["away_team"]
        .apply(pd.Series)["away_team_id"]
        .rename("away_team_id")
    )

    stadium_id = (
        matches_df["stadium"]
        .apply(pd.Series)["id"]
        .rename("stadium_id")
    )
    referee_id = (
            matches_df["referee"]
            .apply(pd.Series)["id"]
            .rename("referee_id")
        )


    # -----------------------------
    # Build Matches Table
    # -----------------------------
    matches_table = pd.concat(
        [
            matches_df["match_id"],
            competition_id,
            season_id,
            home_team_id,
            away_team_id,
            stadium_id,
            referee_id,
            matches_df["home_score"],
            matches_df["away_score"],
            matches_df["match_week"],
            matches_df["match_date"],
            matches_df["kick_off"]


        ],
        axis=1,
    )

    matches_table = matches_table.reset_index(drop=True)

    return matches_table
def transform_seasons(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw match data into the Seasons table.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Raw matches DataFrame.

    Returns
    -------
    pd.DataFrame
        Seasons table.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"season", "competition"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Transformation
    # -----------------------------
    season_df = pd.concat(
        [
            matches_df["season"].apply(pd.Series)[["season_id", "season_name"]],
            matches_df["competition"].apply(pd.Series)["competition_id"],
        ],
        axis=1,
    )

    season_df = (
        season_df
        .drop_duplicates(subset=["season_id"])
        .sort_values("season_id")
        .reset_index(drop=True)
    )

    return season_df

def transform_competitions(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"competition"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    competition_df = (matches_df["competition"].apply(pd.Series)[["competition_id","competition_name"]].
                 drop_duplicates(subset=["competition_id"]).
                 reset_index(drop=True)
                 )

    return competition_df
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
    match_files: list[dict]
) -> pd.DataFrame:
    """
    Transform extracted lineup data into a Positions table.

    Parameters
    ----------
    match_files : list[dict]
        List of extracted lineup JSON files.

    Returns
    -------
    pd.DataFrame
        Positions table containing one row per unique football position.
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
    positions = []

    for match in match_files:

        for team in match["data"]:

            for player in team["lineup"]:

                for position in player["positions"]:

                    row_data = {
                        "position_id": position["position_id"],
                        "position_name": position["position"],
                    }

                    positions.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    positions_df = pd.DataFrame(positions)

    positions_df = (
        positions_df
        .drop_duplicates(subset=["position_id"])
        .sort_values("position_id")
        .reset_index(drop=True)
    )

    return positions_df