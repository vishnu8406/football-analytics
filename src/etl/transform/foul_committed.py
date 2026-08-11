import pandas as pd

def transform_cards(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the Cards table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        Cards table containing one row per unique card.
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
    cards = []

    for match in event_files:

        for event in match["data"]:

            foul = event.get("foul_committed", {})
            card = foul.get("card", {})

            if not card:
                continue

            row_data = {
                "card_id": card.get("id"),
                "card_name": card.get("name"),
            }

            cards.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    cards_df = (
        pd.DataFrame(cards)
        .drop_duplicates(subset=["card_id"])
        .sort_values("card_id")
        .reset_index(drop=True)
    )

    return cards_df

def transform_foul_committed_types(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the FoulCommittedTypes table.
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
    foul_types = []

    for match in event_files:

        for event in match["data"]:

            foul = event.get("foul_committed", {})
            foul_type = foul.get("type", {})

            if not foul_type:
                continue

            row_data = {
                "foul_committed_type_id": foul_type.get("id"),
                "foul_committed_type_name": foul_type.get("name"),
            }

            foul_types.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    foul_types_df = (
        pd.DataFrame(foul_types)
        .drop_duplicates(subset=["foul_committed_type_id"])
        .sort_values("foul_committed_type_id")
        .reset_index(drop=True)
    )

    return foul_types_df

def transform_foul_committed_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the FoulCommittedEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        FoulCommittedEvents table containing one row per foul committed event.
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
    foul_events = []

    for match in event_files:

        for event in match["data"]:

            foul = event.get("foul_committed", {})

            if not foul:
                continue

            foul_type = foul.get("type", {})
            card = foul.get("card", {})

            row_data = {

                "event_id": event["id"],

                "foul_committed_type_id": foul_type.get("id"),

                "card_id": card.get("id"),

                "advantage": foul.get("advantage"),

                "offensive": foul.get("offensive"),

                "penalty": foul.get("penalty"),
            }

            foul_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    foul_events_df = (
        pd.DataFrame(foul_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return foul_events_df


def transform_foul_won_events(
    event_files: list[dict],
) -> pd.DataFrame:
    """
    Transform extracted event data into the FoulWonEvents table.

    Parameters
    ----------
    event_files : list[dict]
        List of extracted event JSON files.

    Returns
    -------
    pd.DataFrame
        FoulWonEvents table containing one row per foul won event.
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
    foul_won_events = []

    for match in event_files:

        for event in match["data"]:

            foul_won = event.get("foul_won", {})

            if not foul_won:
                continue

            row_data = {
                "event_id": event["id"],

                "advantage": foul_won.get("advantage"),
                "defensive": foul_won.get("defensive"),
                "penalty": foul_won.get("penalty"),
            }

            foul_won_events.append(row_data)

    # -----------------------------
    # Build DataFrame
    # -----------------------------
    foul_won_events_df = (
        pd.DataFrame(foul_won_events)
        .sort_values("event_id")
        .reset_index(drop=True)
    )

    return foul_won_events_df