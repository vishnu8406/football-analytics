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

def transform_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the Events table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        Events table containing one row per event.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    events = []

    for match in event_files:

        for event in match["data"]:

            player = event.get("player", {})
            position = event.get("position", {})
            location = event.get("location", [])
            team = event.get("team", {})
            event_type = event.get("type", {})
            possession_team = event.get("possession_team", {})
            play_pattern = event.get("play_pattern", {})
            player_id = player.get("id")
            position_id = position.get("id")

            if position_id == 0:
                position_id = None

            row_data = {
                "event_id": event["id"],
                "match_id": match["match_id"],
                "event_index": event["index"],

                "period": event["period"],
                "minute": event["minute"],
                "second": event["second"],
                "timestamp": event["timestamp"],

                "event_type_id": event_type.get("id"),

                "team_id": team.get("id"),
                "player_id": player_id,
                "position_id": position_id,

                "possession": event["possession"],
                "possession_team_id": possession_team.get("id"),
                "play_pattern_id": play_pattern.get("id"),

                "duration": event.get("duration"),

                "location_x": location[0] if len(location) > 0 else None,
                "location_y": location[1] if len(location) > 1 else None,
            }

            events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    events_df = pd.DataFrame(events)

    events_df = (
        events_df
        .sort_values(["match_id", "event_index"])
        .reset_index(drop=True)
    )

    return events_df
def transform_event_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the EventTypes table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        EventTypes table containing one row per unique event type.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    event_types = []

    for match in event_files:

        for event in match["data"]:

            event_type = event.get("type", {})

            row_data = {
                "event_type_id": event_type.get("id"),
                "event_type_name": event_type.get("name"),
            }

            event_types.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    event_types_df = pd.DataFrame(event_types)

    event_types_df = (
        event_types_df
        .drop_duplicates(subset=["event_type_id"])
        .sort_values("event_type_id")
        .reset_index(drop=True)
    )

    return event_types_df


def transform_play_pattern(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the PlayPattern table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        play pattern table containing one row per unique event type.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    play_patterns = []

    for match in event_files:

        for event in match["data"]:

            play_pattern = event.get("play_pattern", {})

            row_data = {
                "play_pattern_id": play_pattern.get("id"),
                "play_pattern_name": play_pattern.get("name"),
            }

            play_patterns.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    play_pattern_df = pd.DataFrame(play_patterns)

    play_pattern_df = (
        
        play_pattern_df.drop_duplicates(subset=["play_pattern_id"])
        .sort_values("play_pattern_id")
        .reset_index(drop=True)
    )

    return play_pattern_df

def transform_pass_heights(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the PassHeights table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        PassHeights table containing one row per unique pass height.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    pass_heights = []

    for match in event_files:

        for event in match["data"]:

            pass_data = event.get("pass", {})
            height = pass_data.get("height", {})

            if not height:
                continue

            row_data = {
                "pass_height_id": height.get("id"),
                "pass_height_name": height.get("name"),
            }

            pass_heights.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    pass_heights_df = pd.DataFrame(pass_heights)

    pass_heights_df = (
        pass_heights_df
        .drop_duplicates(subset=["pass_height_id"])
        .sort_values("pass_height_id")
        .reset_index(drop=True)
    )

    return pass_heights_df


def transform_pass_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the PassTypes table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        PassTypes table containing one row per unique pass type.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    pass_types = []

    for match in event_files:

        for event in match["data"]:

            pass_data = event.get("pass", {})
            pass_type = pass_data.get("type", {})

            if not pass_type:
                continue

            row_data = {
                "pass_type_id": pass_type.get("id"),
                "pass_type_name": pass_type.get("name"),
            }

            pass_types.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    pass_types_df = pd.DataFrame(pass_types)

    pass_types_df = (
        pass_types_df
        .drop_duplicates(subset=["pass_type_id"])
        .sort_values("pass_type_id")
        .reset_index(drop=True)
    )

    return pass_types_df

def transform_body_parts(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BodyParts table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        BodyParts table containing one row per unique body part.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    body_parts = []

    for match in event_files:

        for event in match["data"]:

            pass_data = event.get("pass", {})
            body_part = pass_data.get("body_part", {})

            if not body_part:
                continue

            row_data = {
                "body_part_id": body_part.get("id"),
                "body_part_name": body_part.get("name"),
            }

            body_parts.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    body_parts_df = pd.DataFrame(body_parts)

    body_parts_df = (
        body_parts_df
        .drop_duplicates(subset=["body_part_id"])
        .sort_values("body_part_id")
        .reset_index(drop=True)
    )

    return body_parts_df

def transform_pass_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the PassOutcomes table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        PassOutcomes table containing one row per unique pass outcome.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    pass_outcomes = []

    for match in event_files:

        for event in match["data"]:

            pass_data = event.get("pass", {})
            outcome = pass_data.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "outcome_id": outcome.get("id"),
                "outcome_name": outcome.get("name"),
            }

            pass_outcomes.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    pass_outcomes_df = pd.DataFrame(pass_outcomes)

    pass_outcomes_df = (
        pass_outcomes_df
        .drop_duplicates(subset=["outcome_id"])
        .sort_values("outcome_id")
        .reset_index(drop=True)
    )

    return pass_outcomes_df

def transform_pass_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the PassEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        PassEvents table containing one row per pass event.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    # -----------------------------
    # Transformation
    # -----------------------------
    pass_events = []

    for match in event_files:

        for event in match["data"]:

            pass_data = event.get("pass", {})

            if not pass_data:
                continue

            recipient = pass_data.get("recipient", {})
            pass_height = pass_data.get("height", {})
            pass_type = pass_data.get("type", {})
            body_part = pass_data.get("body_part", {})
            outcome = pass_data.get("outcome", {})
            end_location = pass_data.get("end_location", [])

            row_data = {
                "event_id": event["id"],
                "recipient_id": recipient.get("id"),

                "pass_type_id": pass_type.get("id"),
                "pass_height_id": pass_height.get("id"),
                "body_part_id": body_part.get("id"),

                "pass_length": pass_data.get("length"),
                "pass_angle": pass_data.get("angle"),

                "end_location_x": end_location[0] if len(end_location) > 0 else None,
                "end_location_y": end_location[1] if len(end_location) > 1 else None,

                "outcome_id": outcome.get("id"),
            }

            pass_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    pass_events_df = pd.DataFrame(pass_events)

    pass_events_df = (
        pass_events_df
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return pass_events_df