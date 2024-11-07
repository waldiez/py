# type: ignore
"""Tests for the `WaldiezIOStream` class."""

import threading
import time
from typing import Any, Optional

import pytest

from waldiez.io import WaldiezIOStream

# pylint: disable=line-too-long,redefined-outer-name, protected-access


def custom_print_function(*args: Any, sep: str = " ", **kwargs: Any) -> None:
    """Custom print function to collect printed outputs.

    Parameters
    ----------
    args : Any
        The print arguments.
    sep : str, optional
        The separator, by default " ".
    kwargs : Any
        Additional print arguments.
    """
    # Save the latest output for testing
    custom_print_function.output = sep.join(map(str, args)) + kwargs.get(
        "end", "\n"
    )


def custom_prompt_handler(prompt: str) -> None:
    """Custom input handler to simulate external input.

    Parameters
    ----------
    prompt : str
        The input prompt.
    """
    # Save the prompt for testing
    custom_prompt_handler.latest_prompt = prompt

    # Simulate asynchronous input after a delay
    def simulate_input() -> None:
        """Simulate asynchronous input."""
        time.sleep(1)  # Simulate delay for input
        custom_prompt_handler.stream.set_input("Test Input")

    threading.Thread(target=simulate_input, daemon=True).start()


@pytest.fixture
def setup_custom_stream() -> WaldiezIOStream:
    """Fixture to set up a `WaldiezIOStream` instance.

    Returns
    -------
    WaldiezIOStream
        The custom stream instance.
    """
    # Reset state
    custom_prompt_handler.latest_prompt = None  # Reset state
    custom_print_function.output = None  # Reset state

    stream = WaldiezIOStream(
        input_timeout=2,
        print_function=custom_print_function,
        on_prompt_input=custom_prompt_handler,
    )
    custom_prompt_handler.stream = (
        stream  # Pass the stream to the prompt handler
    )

    stream.reset_state()  # Ensure clean state
    return stream


def test_print_function(setup_custom_stream: WaldiezIOStream) -> None:
    """Test the custom print function.

    Parameters
    ----------
    setup_custom_stream : WaldiezIOStream
        The custom stream instance.
    """
    stream = setup_custom_stream
    stream.print("Hello, World!", sep=" ", end="!")
    assert (
        custom_print_function.output == "Hello, World!!"
    ), "Custom print function failed."


def test_input_with_prompt(setup_custom_stream: WaldiezIOStream) -> None:
    """Test the input functionality with a custom prompt handler.

    Parameters
    ----------
    setup_custom_stream : WaldiezIOStream
        The custom stream instance.
    """
    stream = setup_custom_stream
    user_input = stream.input("Enter your name:")
    assert (
        user_input == "Test Input"
    ), "Input did not return the expected value."
    assert (
        custom_prompt_handler.latest_prompt == "Enter your name:"
    ), "Prompt handler did not receive the correct prompt."


def test_input_timeout(setup_custom_stream: WaldiezIOStream) -> None:
    """Test input timeout functionality.

    Parameters
    ----------
    setup_custom_stream : WaldiezIOStream
        The custom stream instance.
    """
    stream = setup_custom_stream

    # Reset state to avoid interference
    stream.reset_state()

    # Temporarily disable input setting
    stream.allow_input = False

    user_input = stream.input("This will timeout:")
    assert user_input == "\n", "Input did not return '\\n' on timeout."

    # Re-enable input for subsequent tests
    stream.allow_input = True


def test_set_input(setup_custom_stream: WaldiezIOStream) -> None:
    """Test the `set_input` method directly.

    Parameters
    ----------
    setup_custom_stream : WaldiezIOStream
        The custom stream instance.
    """
    stream = setup_custom_stream

    # Reset state to avoid interference
    stream.reset_state()

    stream.set_input("Direct Input")
    assert (
        stream.current_input == "Direct Input"
    ), "set_input did not correctly set the input value."
    assert (
        stream._input_event.is_set()
    ), "set_input did not signal the input event."


def test_default_print() -> None:
    """Test default print behavior when no custom print function is provided."""
    # Create a stream with no custom print function
    stream = WaldiezIOStream(input_timeout=2)

    # Replace `print` temporarily
    default_print_output: Optional[str] = None

    def mock_print(*args: Any, **kwargs: Any) -> None:
        """Mock print function to capture default print output.

        Parameters
        ----------
        args : Any
            The print arguments.
        kwargs : Any
            Additional print arguments.
        """
        nonlocal default_print_output
        default_print_output = " ".join(map(str, args)) + kwargs.get(
            "end", "\n"
        )

    original_print = __builtins__["print"]  # type: ignore
    __builtins__["print"] = mock_print

    try:
        stream.print("Default print behavior", end="\n")
        assert (
            default_print_output == "Default print behavior\n"
        ), "Default print function failed."
    finally:
        __builtins__["print"] = original_print


def test_input_without_prompt_handler() -> None:
    """Test input functionality without a custom prompt handler."""
    stream = WaldiezIOStream(input_timeout=2)
    stream.set_input("Fallback Input")
    user_input = stream.input()
    assert (
        user_input == "Fallback Input"
    ), "Input did not return the expected value without a prompt handler."
