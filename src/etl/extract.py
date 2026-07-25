from pathlib import Path
import pandas as pd


def extract(file_path: str | Path) -> pd.DataFrame:
    """
    Reads a JSON file and returns its contents as a Pandas DataFrame.

    Parameters
    ----------
    file_path : str | Path
        Path to the JSON file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the extracted data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    ValueError
        If the file is not a JSON file or contains invalid JSON.
    """

    # Convert input to a Path object
    file_path = Path(file_path)

    # Check whether the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Ensure the file is a JSON file
    if file_path.suffix.lower() != ".json":
        raise ValueError(
            f"Expected a JSON file, got '{file_path.suffix}' instead."
        )

    # Read the JSON file
    try:
        df = pd.read_json(file_path)
    except ValueError as e:
        raise ValueError(
            f"Invalid JSON structure in '{file_path.name}'."
        ) from e

    return df
