"""Test waldiez.exporting.utils.path_check.*."""

import os

from waldiez.exporting.utils.path_check import get_path_string


def test_get_path_string() -> None:
    """Test get_path_string."""
    # Given
    path = __file__
    # When
    result = get_path_string(path)
    # Then
    if os.name == "nt":
        assert result == f"r'{path}'"
    else:
        assert result == f"{path}"


def test_get_path_string_not_local() -> None:
    """Test get_path_string with a non-local path."""
    # Given
    path = "https://example.com"
    # When
    result = get_path_string(path)
    # Then
    assert result == path


def test_get_path_string_no_path() -> None:
    """Test get_path_string with a non-path string."""
    # Given
    path = "exa~/e\\mp/le"
    # When
    result = get_path_string(path)
    # Then
    assert result == path
