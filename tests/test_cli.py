"""Test the CLI."""

import argparse
import sys

import pytest

from waldiez import __version__
from waldiez.__main__ import main as waldiez_main  # type: ignore
from waldiez.cli import get_parser, main


def test_get_parser() -> None:
    """Test the get_parser function."""
    parser = get_parser()
    assert isinstance(parser, argparse.ArgumentParser)


def test_get_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_version function.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["waldiez", "--version"]
        main()
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the help message.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["waldiez", "--help"]
        waldiez_main()
    captured = capsys.readouterr()
    assert "usage: waldiez" in captured.out
