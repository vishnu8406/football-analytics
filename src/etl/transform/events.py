import pandas as pd


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
