"""Test WaldiezRunner."""

# pylint: disable=protected-access

import shutil
from pathlib import Path
from typing import Any

import pytest
from autogen.io import IOStream  # type: ignore

from waldiez import Waldiez, WaldiezRunner
from waldiez.models import WaldiezFlow


class CustomIOStream(IOStream):
    """Custom IOStream class."""

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """Print objects.

        Parameters
        ----------
        objects : Any
            Objects to print.
        sep : str, optional
            Separator, by default " ".
        end : str, optional
            End, by default 'eol'.
        flush : bool, optional
            Whether to flush, by default False.
        """
        print(*objects, sep=sep, end=end, flush=flush)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """Get user input.

        Parameters
        ----------
        prompt : str, optional
            Prompt, by default "".
        password : bool, optional
            Whether to read a password, by default False.

        Returns
        -------
        str
            User input.
        """
        return "User input"


def test_waldiez_runner(
    waldiez_flow: WaldiezFlow,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test WaldiezRunner.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    tmp_path : Path
        Pytest fixture to create temporary directory.
    capsys : pytest.CaptureFixture[Optional[str]]
        Pytest fixture to capture stdout and stderr.
    """
    waldiez = Waldiez.from_dict(data=waldiez_flow.model_dump(by_alias=True))
    output_path = tmp_path / "output.py"
    runner = WaldiezRunner(waldiez)
    with IOStream.set_default(CustomIOStream()):
        runner.run(output_path=output_path)
    std_out = capsys.readouterr().out
    assert "Starting workflow" in std_out
    assert (tmp_path / "waldiez_out").exists()
    shutil.rmtree(tmp_path / "waldiez_out")


def test_waldiez_with_invalid_requirement(
    capsys: pytest.CaptureFixture[str],
    waldiez_flow: WaldiezFlow,
) -> None:
    """Test Waldiez with invalid requirement.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    flow_dict = waldiez_flow.model_dump(by_alias=True)
    # add an invalid requirement
    flow_dict["requirements"] = ["invalid_requirement"]
    waldiez = Waldiez.from_dict(data=flow_dict)
    runner = WaldiezRunner(waldiez)
    runner._install_requirements(print)
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )
