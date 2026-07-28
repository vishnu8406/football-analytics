import pandas as pd

def transform_goalkeeper_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the GoalkeeperOutcomes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    goalkeeper_outcomes = []

    for match in event_files:

        for event in match["data"]:

            goalkeeper = event.get("goalkeeper", {})
            outcome = goalkeeper.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "goalkeeper_outcome_id": outcome.get("id"),
                "goalkeeper_outcome_name": outcome.get("name"),
            }

            goalkeeper_outcomes.append(row_data)

    goalkeeper_outcomes_df = (
        pd.DataFrame(goalkeeper_outcomes)
        .drop_duplicates(subset=["goalkeeper_outcome_id"])
        .sort_values("goalkeeper_outcome_id")
        .reset_index(drop=True)
    )

    return goalkeeper_outcomes_df

def transform_goalkeeper_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the GoalkeeperTypes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    goalkeeper_types = []

    for match in event_files:

        for event in match["data"]:

            goalkeeper = event.get("goalkeeper", {})
            goalkeeper_type = goalkeeper.get("type", {})

            if not goalkeeper_type:
                continue

            row_data = {
                "goalkeeper_type_id": goalkeeper_type.get("id"),
                "goalkeeper_type_name": goalkeeper_type.get("name"),
            }

            goalkeeper_types.append(row_data)

    goalkeeper_types_df = (
        pd.DataFrame(goalkeeper_types)
        .drop_duplicates(subset=["goalkeeper_type_id"])
        .sort_values("goalkeeper_type_id")
        .reset_index(drop=True)
    )

    return goalkeeper_types_df


def transform_goalkeeper_techniques(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the GoalkeeperTechniques table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    goalkeeper_techniques = []

    for match in event_files:

        for event in match["data"]:

            goalkeeper = event.get("goalkeeper", {})
            technique = goalkeeper.get("technique", {})

            if not technique:
                continue

            row_data = {
                "goalkeeper_technique_id": technique.get("id"),
                "goalkeeper_technique_name": technique.get("name"),
            }

            goalkeeper_techniques.append(row_data)

    goalkeeper_techniques_df = (
        pd.DataFrame(goalkeeper_techniques)
        .drop_duplicates(subset=["goalkeeper_technique_id"])
        .sort_values("goalkeeper_technique_id")
        .reset_index(drop=True)
    )

    return goalkeeper_techniques_df


def transform_goalkeeper_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the GoalkeeperEvents table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    goalkeeper_events = []

    for match in event_files:

        for event in match["data"]:

            goalkeeper = event.get("goalkeeper", {})

            if not goalkeeper:
                continue

            outcome = goalkeeper.get("outcome", {})
            goalkeeper_type = goalkeeper.get("type", {})
            position = goalkeeper.get("position", {})
            technique = goalkeeper.get("technique", {})
            body_part = goalkeeper.get("body_part", {})
            end_location = goalkeeper.get("end_location", [])

            row_data = {

                "event_id": event["id"],

                "goalkeeper_outcome_id": outcome.get("id"),

                "goalkeeper_type_id": goalkeeper_type.get("id"),

                "position_id": position.get("id"),

                "goalkeeper_technique_id": technique.get("id"),

                "body_part_id": body_part.get("id"),

                "end_location_x":
                    end_location[0] if len(end_location) > 0 else None,

                "end_location_y":
                    end_location[1] if len(end_location) > 1 else None,

                "end_location_z":
                    end_location[2] if len(end_location) > 2 else None,

                "lost_in_play": goalkeeper.get("lost_in_play"),

                "lost_out": goalkeeper.get("lost_out"),

                "punched_out": goalkeeper.get("punched_out"),

                "shot_saved_off_target":
                    goalkeeper.get("shot_saved_off_target"),

                "shot_saved_to_post":
                    goalkeeper.get("shot_saved_to_post"),

                "success_in_play":
                    goalkeeper.get("success_in_play"),

                "success_out":
                    goalkeeper.get("success_out"),
            }

            goalkeeper_events.append(row_data)

    goalkeeper_events_df = (
        pd.DataFrame(goalkeeper_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return goalkeeper_events_df