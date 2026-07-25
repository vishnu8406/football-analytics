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
    team_df = matches_df[["team_id,home_team_id"]]

    