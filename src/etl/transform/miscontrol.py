import pandas as pd
def transform_miscontrol_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the MiscontrolEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        MiscontrolEvents table containing one row per miscontrol event.
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
    miscontrol_events = []

    for match in event_files:

        for event in match["data"]:

            miscontrol = event.get("miscontrol", {})

            if not miscontrol:
                continue

            row_data = {
                "event_id": event["id"],
                "aerial_won": miscontrol.get("aerial_won"),
            }

            miscontrol_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    miscontrol_events_df = (
        pd.DataFrame(miscontrol_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return miscontrol_events_df