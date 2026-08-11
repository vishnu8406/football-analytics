import pandas as pd

def transform_dribble_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the DribbleOutcomes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    dribble_outcomes = []

    for match in event_files:

        for event in match["data"]:

            dribble = event.get("dribble", {})
            outcome = dribble.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "dribble_outcome_id": outcome.get("id"),
                "dribble_outcome_name": outcome.get("name"),
            }

            dribble_outcomes.append(row_data)

    dribble_outcomes_df = (
        pd.DataFrame(dribble_outcomes)
        .drop_duplicates(subset=["dribble_outcome_id"])
        .sort_values("dribble_outcome_id")
        .reset_index(drop=True)
    )

    return dribble_outcomes_df


def transform_dribble_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the DribbleEvents table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    dribble_events = []

    for match in event_files:

        for event in match["data"]:

            dribble = event.get("dribble", {})

            if not dribble:
                continue

            outcome = dribble.get("outcome", {})

            row_data = {
                "event_id": event["id"],
                "dribble_outcome_id": outcome.get("id"),
                "overrun": dribble.get("overrun"),
            }

            dribble_events.append(row_data)

    dribble_events_df = (
        pd.DataFrame(dribble_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return dribble_events_df