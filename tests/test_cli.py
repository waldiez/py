"""Test the CLI."""

import argparse
import sys
from pathlib import Path

import pytest

from waldiez import __version__
from waldiez.__main__ import main as waldiez_main  # type: ignore
from waldiez.cli import get_parser, main
from waldiez.models import WaldiezFlow


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


def test_empty_cli(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the CLI with no arguments.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    with pytest.raises(SystemExit):
        sys.argv = ["waldiez"]
        waldiez_main()
    captured = capsys.readouterr()
    assert "usage: waldiez" in captured.out


def test_cli_export(
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    waldiez_flow: WaldiezFlow,
) -> None:
    """Test exporting a WaldiezFlow using the CLI.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest fixture to capture logs.
    tmp_path : Path
        Pytest fixture to provide a temporary directory.
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    input_file = tmp_path / f"{waldiez_flow.name}.waldiez"
    with open(input_file, "w", encoding="utf-8") as file:
        file.write(waldiez_flow.model_dump_json(by_alias=True))
    output_file = tmp_path / f"{waldiez_flow.name}.ipynb"
    sys.argv = [
        "waldiez",
        "--export",
        "--output",
        str(output_file),
        str(input_file),
    ]
    waldiez_main()
    assert "Generated" in caplog.text
    assert output_file.exists()
    output_file.unlink(missing_ok=True)


def test_cli_run(
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    waldiez_flow_no_human_input: WaldiezFlow,
) -> None:
    """Test running a WaldiezFlow using the CLI.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest fixture to capture logs.
    tmp_path : Path
        Pytest fixture to provide a temporary directory.
    waldiez_flow_no_human_input : WaldiezFlow
        A WaldiezFlow instance with no human input.
    """
    input_file = tmp_path / f"{waldiez_flow_no_human_input.name}.waldiez"
    with open(input_file, "w", encoding="utf-8") as file:
        file.write(waldiez_flow_no_human_input.model_dump_json(by_alias=True))
    sys.argv = ["waldiez", str(input_file)]
    waldiez_main()
    assert "Summary" in caplog.text
