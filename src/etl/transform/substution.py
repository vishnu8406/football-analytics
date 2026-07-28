import pandas as pd

def transform_substitution_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the SubstitutionOutcomes table.
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
    substitution_outcomes = []

    for match in event_files:

        for event in match["data"]:

            substitution = event.get("substitution", {})
            outcome = substitution.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "substitution_outcome_id": outcome.get("id"),
                "substitution_outcome_name": outcome.get("name"),
            }

            substitution_outcomes.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    substitution_outcomes_df = (
        pd.DataFrame(substitution_outcomes)
        .drop_duplicates(subset=["substitution_outcome_id"])
        .sort_values("substitution_outcome_id")
        .reset_index(drop=True)
    )

    return substitution_outcomes_df

def transform_substitution_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the SubstitutionEvents table.
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
    substitution_events = []

    for match in event_files:

        for event in match["data"]:

            substitution = event.get("substitution", {})

            if not substitution:
                continue

            outcome = substitution.get("outcome", {})
            replacement = substitution.get("replacement", {})

            row_data = {
                "event_id": event["id"],

                "replacement_player_id": replacement.get("id"),

                "substitution_outcome_id": outcome.get("id"),
            }

            substitution_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    substitution_events_df = (
        pd.DataFrame(substitution_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return substitution_events_df