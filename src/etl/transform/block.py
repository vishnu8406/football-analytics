import pandas as pd

def transform_block_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the BlockEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        BlockEvents table containing one row per block event.
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
    block_events = []

    for match in event_files:

        for event in match["data"]:

            block = event.get("block", {})

            if not block:
                continue

            row_data = {
                "event_id": event["id"],

                "deflection": block.get("deflection"),
                "offensive": block.get("offensive"),
                "save_block": block.get("save_block"),
            }

            block_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    block_events_df = (
        pd.DataFrame(block_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return block_events_df