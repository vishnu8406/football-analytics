import pandas as pd


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

            sources = [

                event.get("pass", {}).get("body_part", {}),

                event.get("shot", {}).get("body_part", {}),

                event.get("clearance", {}).get("body_part", {}),

                event.get("goalkeeper", {}).get("body_part", {}),

            ]

            for body_part in sources:

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
    body_parts_df = (
        pd.DataFrame(body_parts)
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
                "pass_outcome_id": outcome.get("id"),
                "pass_outcome_name": outcome.get("name"),
            }

            pass_outcomes.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    pass_outcomes_df = pd.DataFrame(pass_outcomes)

    pass_outcomes_df = (
        pass_outcomes_df
        .drop_duplicates(subset=["pass_outcome_id"])
        .sort_values("pass_outcome_id")
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

                "pass_outcome_id": outcome.get("id"),
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