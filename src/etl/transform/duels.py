import pandas as pd

def transform_duel_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the DuelTypes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    duel_types = []

    for match in event_files:

        for event in match["data"]:

            duel = event.get("duel", {})
            duel_type = duel.get("type", {})

            if not duel_type:
                continue

            row_data = {
                "duel_type_id": duel_type.get("id"),
                "duel_type_name": duel_type.get("name"),
            }

            duel_types.append(row_data)

    duel_types_df = (
        pd.DataFrame(duel_types)
        .drop_duplicates(subset=["duel_type_id"])
        .sort_values("duel_type_id")
        .reset_index(drop=True)
    )

    return duel_types_df

def transform_duel_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the DuelOutcomes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    duel_outcomes = []

    for match in event_files:

        for event in match["data"]:

            duel = event.get("duel", {})
            outcome = duel.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "duel_outcome_id": outcome.get("id"),
                "duel_outcome_name": outcome.get("name"),
            }

            duel_outcomes.append(row_data)

    duel_outcomes_df = (
        pd.DataFrame(duel_outcomes)
        .drop_duplicates(subset=["duel_outcome_id"])
        .sort_values("duel_outcome_id")
        .reset_index(drop=True)
    )

    return duel_outcomes_df

def transform_duel_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the DuelEvents table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    duel_events = []

    for match in event_files:

        for event in match["data"]:

            duel = event.get("duel", {})

            if not duel:
                continue

            duel_type = duel.get("type", {})
            outcome = duel.get("outcome", {})

            row_data = {
                "event_id": event["id"],

                "duel_type_id": duel_type.get("id"),

                "duel_outcome_id": outcome.get("id"),
            }

            duel_events.append(row_data)

    duel_events_df = (
        pd.DataFrame(duel_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return duel_events_df