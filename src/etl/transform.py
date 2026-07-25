import pandas as pd


def transform_teams(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique teams from the matches DataFrame.

    Parameters
    ----------
    matches_df : pd.DataFrame
        Raw matches DataFrame returned by extract().

    Returns
    -------
    pd.DataFrame
        DataFrame containing unique teams.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"home_team", "away_team"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Home Teams
    # -----------------------------
    home_teams = (
        matches_df["home_team"]
        .apply(pd.Series)[["home_team_id", "home_team_name"]]
        .rename(
            columns={
                "home_team_id": "team_id",
                "home_team_name": "team_name",
            }
        )
    )

    # -----------------------------
    # Away Teams
    # -----------------------------
    away_teams = (
        matches_df["away_team"]
        .apply(pd.Series)[["away_team_id", "away_team_name"]]
        .rename(
            columns={
                "away_team_id": "team_id",
                "away_team_name": "team_name",
            }
        )
    )

    # -----------------------------
    # Combine
    # -----------------------------
    teams_df = pd.concat(
        [home_teams, away_teams],
        ignore_index=True,
    )

    teams_df = (
        teams_df
        .drop_duplicates(subset=["team_id"])
        .sort_values("team_id")
        .reset_index(drop=True)
    )

    return teams_df


def transform_stadiums(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique stadiums from the matches DataFrame.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"stadium"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Transformation
    # -----------------------------
    stadiums_df = (
        matches_df["stadium"]
        .dropna()
        .apply(pd.Series)[["id", "name"]]
        .rename(
            columns={
                "id": "stadium_id",
                "name": "stadium_name",
            }
        )
        .drop_duplicates(subset=["stadium_id"])
        .sort_values("stadium_id")
        .reset_index(drop=True)
    )

    return stadiums_df


def transform_referees(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique referees from the matches DataFrame.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {"referee"}

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Transformation
    # -----------------------------
    referees_df = (
        matches_df["referee"]
        .dropna()
        .apply(pd.Series)[["id", "name"]]
        .rename(
            columns={
                "id": "referee_id",
                "name": "referee_name",
            }
        )
        .drop_duplicates(subset=["referee_id"])
        .sort_values("referee_id")
        .reset_index(drop=True)
    )

    return referees_df


def transform_matches(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the matches DataFrame into the Matches table.
    """

    # -----------------------------
    # Validation
    # -----------------------------
    if not isinstance(matches_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if matches_df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = {
        "match_id",
        "competition",
        "season",
        "home_team",
        "away_team",
        "stadium",
        "home_score",
        "away_score",
    }

    if not required_columns.issubset(matches_df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(matches_df.columns)}"
        )

    # -----------------------------
    # Extract nested IDs
    # -----------------------------
    competition_id = (
        matches_df["competition"]
        .apply(pd.Series)["competition_id"]
        .rename("competition_id")
    )

    season_id = (
        matches_df["season"]
        .apply(pd.Series)["season_id"]
        .rename("season_id")
    )

    home_team_id = (
        matches_df["home_team"]
        .apply(pd.Series)["home_team_id"]
        .rename("home_team_id")
    )

    away_team_id = (
        matches_df["away_team"]
        .apply(pd.Series)["away_team_id"]
        .rename("away_team_id")
    )

    stadium_id = (
        matches_df["stadium"]
        .apply(pd.Series)["id"]
        .rename("stadium_id")
    )

    # -----------------------------
    # Build Matches Table
    # -----------------------------
    matches_table = pd.concat(
        [
            matches_df["match_id"],
            competition_id,
            season_id,
            home_team_id,
            away_team_id,
            stadium_id,
            matches_df["home_score"],
            matches_df["away_score"],
        ],
        axis=1,
    )

    matches_table = matches_table.reset_index(drop=True)

    return matches_table