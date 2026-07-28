import pandas as pd

def transform_clearance_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the ClearanceEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        ClearanceEvents table containing one row per clearance event.
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
    clearance_events = []

    for match in event_files:

        for event in match["data"]:

            clearance = event.get("clearance", {})

            if not clearance:
                continue

            body_part = clearance.get("body_part", {})

            row_data = {
                "event_id": event["id"],

                "body_part_id": body_part.get("id"),

                "aerial_won": clearance.get("aerial_won"),
                "head": clearance.get("head"),
                "left_foot": clearance.get("left_foot"),
                "right_foot": clearance.get("right_foot"),
                "other": clearance.get("other"),

                "out": event.get("out"),
            }

            clearance_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    clearance_events_df = (
        pd.DataFrame(clearance_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return clearance_events_df