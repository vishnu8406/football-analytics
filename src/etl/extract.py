from pathlib import Path
import pandas as pd
import json


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

def extract_match_files(
    folder_path: str | Path,
    match_ids: list[int],
) -> list[dict]:
    """
    Extract multiple match JSON files from a folder.

    Parameters
    ----------
    folder_path : str | Path
        Path to the folder containing match JSON files.

    match_ids : list[int]
        List of match IDs whose JSON files should be extracted.

    Returns
    -------
    list[dict]
        A list where each element contains:
        {
            "match_id": int,
            "data": dict | list
        }

    Raises
    ------
    FileNotFoundError
        If the folder does not exist.

    NotADirectoryError
        If the given path is not a directory.

    ValueError
        If match_ids is empty.
    """

    folder_path = Path(folder_path)

    # -----------------------------
    # Validation
    # -----------------------------
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"{folder_path} is not a directory.")

    if not match_ids:
        raise ValueError("match_ids list is empty.")

    # -----------------------------
    # Extraction
    # -----------------------------
    match_files = []

    for match_id in match_ids:

        file_path = folder_path / f"{match_id}.json"

        if not file_path.exists():
            print(f"Warning: {file_path.name} not found.")
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        match_files.append(
            {
                "match_id": match_id,
                "data": data,
            }
        )

    return match_files