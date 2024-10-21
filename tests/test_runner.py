"""Test WaldieRunner."""

# pylint: disable=protected-access

from typing import Optional

import pytest

from waldiez import Waldie, WaldieIOStream, WaldieRunner
from waldiez.models import WaldieFlow


def test_runner(waldie_flow: WaldieFlow) -> None:
    """Test WaldieRunner.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    runner = WaldieRunner(waldie)
    assert runner.waldie == waldie
    assert not runner.running

    prompt_input: Optional[str] = None
    stream: WaldieIOStream

    def on_prompt_input(prompt: str) -> None:
        nonlocal prompt_input, stream
        prompt_input = prompt
        stream.forward_input("Reply to prompt\n")

    stream = WaldieIOStream(
        on_prompt_input=on_prompt_input,
        print_function=print,
    )
    with WaldieIOStream.set_default(stream):
        runner.run(stream)
    assert not runner.running
    assert runner._stream.get() is None
    assert prompt_input is not None
    stream.close()


def test_waldie_with_invalid_requirement(
    capsys: pytest.CaptureFixture[str],
    waldie_flow: WaldieFlow,
) -> None:
    """Test Waldie with invalid requirement.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    flow_dict = waldie_flow.model_dump(by_alias=True)
    # add an invalid requirement
    flow_dict["requirements"] = ["invalid_requirement"]
    waldie = Waldie.from_dict(data=flow_dict)
    runner = WaldieRunner(waldie)
    runner._install_requirements()
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )
