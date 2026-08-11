import pandas as pd

def transform_ball_recovery_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BallRecoveryEvents table.
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
    ball_recovery_events = []

    for match in event_files:

        for event in match["data"]:

            ball_recovery = event.get("ball_recovery", {})

            if not ball_recovery:
                continue

            row_data = {
                "event_id": event["id"],
                "offensive": ball_recovery.get("offensive"),
                "recovery_failure": ball_recovery.get("recovery_failure"),
            }

            ball_recovery_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    ball_recovery_events_df = (
        pd.DataFrame(ball_recovery_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return ball_recovery_events_df