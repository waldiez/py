"""Path check utility functions."""

import os
from pathlib import Path

# pylint: disable=broad-except


def _is_local_path(string: str) -> bool:
    """Check if a string is a local path.

    Parameters
    ----------
    string : str
        The string to check.

    Returns
    -------
    bool
        True if the path is a local path.
    """
    try:
        path = Path(string).resolve()
        return path.exists()
    except Exception:  # pragma: no cover
        return False


def get_path_string(string: str) -> str:
    """Get the path string.

    Parameters
    ----------
    string : str
        The string to check.

    Returns
    -------
    str
        The local path string.
    """
    # On windows, we get paths like "C:\path\to\file"
    # if so, let's try to avoid invalid escape sequences
    if not _is_local_path(string):
        return string
    if os.name == "nt":  # pragma: no cover
        return f"r'{string}'"
    return f"'{string}'"
