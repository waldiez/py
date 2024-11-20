"""Test WaldiezRunner."""

# pylint: disable=protected-access

from pathlib import Path
from typing import Optional

import pytest

from waldiez import Waldiez, WaldiezRunner
from waldiez.io import WaldiezIOStream
from waldiez.models import WaldiezFlow


def test_runner(waldiez_flow: WaldiezFlow) -> None:
    """Test WaldiezRunner.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    runner = WaldiezRunner(waldiez)
    assert runner.waldiez == waldiez
    assert not runner.running

    prompt_input: Optional[str] = None
    stream: WaldiezIOStream

    def on_prompt_input(prompt: str) -> None:
        nonlocal prompt_input, stream
        prompt_input = prompt
        stream.set_input("Reply to prompt\n")

    stream = WaldiezIOStream(
        on_prompt_input=on_prompt_input,
        print_function=print,
        input_timeout=2,
    )
    with WaldiezIOStream.set_default(stream):
        runner.run(stream)
    assert not runner.running
    assert runner._stream.get() is None
    assert prompt_input is not None


def test_runner_with_uploads_root(
    waldiez_flow: WaldiezFlow, tmp_path: Path
) -> None:
    """Test WaldiezRunner with uploads root.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    uploads_root = tmp_path / "uploads"
    runner = WaldiezRunner(waldiez, uploads_root)
    assert runner.waldiez == waldiez
    assert not runner.running

    prompt_input: Optional[str] = None
    stream: WaldiezIOStream

    def on_prompt_input(prompt: str) -> None:
        nonlocal prompt_input, stream
        prompt_input = prompt
        stream.set_input("Reply to prompt\n")

    stream = WaldiezIOStream(
        on_prompt_input=on_prompt_input,
        print_function=print,
        input_timeout=2,
    )
    with WaldiezIOStream.set_default(stream):
        runner.run(stream, uploads_root=uploads_root)
    assert not runner.running
    assert runner._stream.get() is None
    assert prompt_input is not None
    assert uploads_root.exists()
    uploads_root.rmdir()


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
    runner._install_requirements()
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )
