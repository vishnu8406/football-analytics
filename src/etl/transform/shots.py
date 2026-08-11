import pandas as pd

def transform_shot_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the ShotOutcomes table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        ShotOutcomes table containing one row per unique shot outcome.
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
    shot_outcomes = []

    for match in event_files:

        for event in match["data"]:

            shot_data = event.get("shot", {})
            outcome = shot_data.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "shot_outcome_id": outcome.get("id"),
                "shot_outcome_name": outcome.get("name"),
            }

            shot_outcomes.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    shot_outcomes_df = pd.DataFrame(shot_outcomes)

    shot_outcomes_df = (
        shot_outcomes_df
        .drop_duplicates(subset=["shot_outcome_id"])
        .sort_values("shot_outcome_id")
        .reset_index(drop=True)
    )

    return shot_outcomes_df

def transform_shot_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the ShotTypes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    shot_types = []

    for match in event_files:

        for event in match["data"]:

            shot_data = event.get("shot", {})
            shot_type = shot_data.get("type", {})

            if not shot_type:
                continue

            row_data = {
                "shot_type_id": shot_type.get("id"),
                "shot_type_name": shot_type.get("name"),
            }

            shot_types.append(row_data)

    shot_types_df = pd.DataFrame(shot_types)

    shot_types_df = (
        shot_types_df
        .drop_duplicates(subset=["shot_type_id"])
        .sort_values("shot_type_id")
        .reset_index(drop=True)
    )

    return shot_types_df
def transform_shot_techniques(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the ShotEvents table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    shot_techniques = []

    for match in event_files:

        for event in match["data"]:

            shot_data = event.get("shot", {})
            technique = shot_data.get("technique", {})

            if not technique:
                continue

            row_data = {
                "shot_technique_id": technique.get("id"),
                "shot_technique_name": technique.get("name"),
            }

            shot_techniques.append(row_data)

    shot_techniques_df = pd.DataFrame(shot_techniques)

    shot_techniques_df = (
        shot_techniques_df
        .drop_duplicates(subset=["shot_technique_id"])
        .sort_values("shot_technique_id")
        .reset_index(drop=True)
    )

    return shot_techniques_df


def transform_shot_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the ShotTechniques table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    shot_events = []

    for match in event_files:

        for event in match["data"]:

            shot_data = event.get("shot", {})
            outcome = shot_data.get("outcome", {})
            shot_type = shot_data.get("type", {})
            technique = shot_data.get("technique", {})
            body_part = shot_data.get("body_part", {})

            end_location = shot_data.get("end_location", [])

            if not shot_data:
                continue

            row_data = {
                "event_id": event["id"],

                "shot_outcome_id": outcome.get("id"),
                "shot_type_id": shot_type.get("id"),
                "shot_technique_id": technique.get("id"),
                "body_part_id": body_part.get("id"),

                "statsbomb_xg": shot_data.get("statsbomb_xg"),

                "under_pressure": event.get("under_pressure"),

                "first_time": shot_data.get("first_time"),
                "deflected": shot_data.get("deflected"),
                "open_goal": shot_data.get("open_goal"),
                "one_on_one": shot_data.get("one_on_one"),

                "key_pass_event_id": shot_data.get("key_pass_id"),

                "end_location_x": end_location[0] if len(end_location) > 0 else None,
                "end_location_y": end_location[1] if len(end_location) > 1 else None,
                "end_location_z": end_location[2] if len(end_location) > 2 else None,
            }
            shot_events.append(row_data)


    shot_events_df = (
    pd.DataFrame(shot_events)
    .sort_values("event_id")
    .reset_index(drop=True)
)

    return shot_events_df


