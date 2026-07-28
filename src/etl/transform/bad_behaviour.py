import pandas as pd

def transform_bad_behaviour_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BadBehaviourEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        BadBehaviourEvents table containing one row per bad behaviour event.
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
    bad_behaviour_events = []

    for match in event_files:

        for event in match["data"]:

            bad_behaviour = event.get("bad_behaviour", {})

            if not bad_behaviour:
                continue

            card = bad_behaviour.get("card", {})

            row_data = {
                "event_id": event["id"],
                "card_id": card.get("id"),
            }

            bad_behaviour_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    bad_behaviour_events_df = (
        pd.DataFrame(bad_behaviour_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return bad_behaviour_events_df