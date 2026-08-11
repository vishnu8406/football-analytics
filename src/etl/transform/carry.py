import pandas as pd

def transform_carry_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the CarryEvents table.
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
    carry_events = []

    for match in event_files:

        for event in match["data"]:

            carry = event.get("carry", {})

            if not carry:
                continue

            end_location = carry.get("end_location", [])

            row_data = {
                "event_id": event["id"],

                "end_location_x":
                    end_location[0] if len(end_location) > 0 else None,

                "end_location_y":
                    end_location[1] if len(end_location) > 1 else None,
            }

            carry_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    carry_events_df = (
        pd.DataFrame(carry_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return carry_events_df