import pandas as pd

def transform_interception_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the InterceptionOutcomes table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    interception_outcomes = []

    for match in event_files:

        for event in match["data"]:

            interception = event.get("interception", {})
            outcome = interception.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "interception_outcome_id": outcome.get("id"),
                "interception_outcome_name": outcome.get("name"),
            }

            interception_outcomes.append(row_data)

    interception_outcomes_df = (
        pd.DataFrame(interception_outcomes)
        .drop_duplicates(subset=["interception_outcome_id"])
        .sort_values("interception_outcome_id")
        .reset_index(drop=True)
    )

    return interception_outcomes_df

def transform_interception_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the InterceptionEvents table.
    """

    if not isinstance(event_files, list):
        raise TypeError("Input must be a list.")

    if not event_files:
        raise ValueError("Input list is empty.")

    interception_events = []

    for match in event_files:

        for event in match["data"]:

            interception = event.get("interception", {})

            if not interception:
                continue

            outcome = interception.get("outcome", {})

            row_data = {
                "event_id": event["id"],
                "interception_outcome_id": outcome.get("id"),
            }

            interception_events.append(row_data)

    interception_events_df = (
        pd.DataFrame(interception_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return interception_events_df