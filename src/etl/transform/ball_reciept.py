import pandas as pd

def transform_ball_receipt_outcomes(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BallReceiptOutcomes table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        BallReceiptOutcomes table containing one row per unique outcome.
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
    ball_receipt_outcomes = []

    for match in event_files:

        for event in match["data"]:

            ball_receipt = event.get("ball_receipt", {})
            outcome = ball_receipt.get("outcome", {})

            if not outcome:
                continue

            row_data = {
                "ball_receipt_outcome_id": outcome.get("id"),
                "ball_receipt_outcome_name": outcome.get("name"),
            }

            ball_receipt_outcomes.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    ball_receipt_outcomes_df = (
        pd.DataFrame(ball_receipt_outcomes)
        .drop_duplicates(subset=["ball_receipt_outcome_id"])
        .sort_values("ball_receipt_outcome_id")
        .reset_index(drop=True)
    )

    return ball_receipt_outcomes_df

def transform_ball_receipt_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BallReceiptEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        BallReceiptEvents table containing one row per ball receipt event.
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
    ball_receipt_events = []

    for match in event_files:

        for event in match["data"]:

            ball_receipt = event.get("ball_receipt", {})

            if not ball_receipt:
                continue

            outcome = ball_receipt.get("outcome", {})

            row_data = {
                "event_id": event["id"],
                "ball_receipt_outcome_id": outcome.get("id"),
            }

            ball_receipt_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    ball_receipt_events_df = (
        pd.DataFrame(ball_receipt_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return ball_receipt_events_df