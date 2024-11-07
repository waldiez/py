"""Custom IOStream class to use with autogen.

It is meant to be used when we want to use custom
`print` and `input`. For example, when a websocket
is used to trigger a UI element that requires user input.
and sends back the user's input to the websocket. In the same
way, we can use it to forward what is meant to be printed.
"""

import threading
from typing import Any, Callable, Optional

from autogen.io import IOStream  # type: ignore[import-untyped]


class WaldiezIOStream(IOStream):
    """Custom IOStream class to handle `print` and `input` functions."""

    def __init__(
        self,
        input_timeout: float = 60.0,
        print_function: Optional[Callable[..., None]] = None,
        on_prompt_input: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Initialize the IOStream.

        Parameters
        ----------
        input_timeout : float, optional
            The input timeout in seconds, by default 60.0.
        print_function : Optional[Callable[..., None]], optional
            The function to handle print operations, by default None.
        on_prompt_input : Optional[Callable[[str], None]], optional
            The function to call for processing input prompts, by default None.

        Notes
        -----
        - on_prompt_input: It does not return a string (like 'input' does).
            Instead, it is meant to be used to forward the prompt somewhere else
            (e.g., a websocket). When we get the input, we can call
            `waldiez_io_stream.set_input(input_data)` with the input data.
        """
        self.input_timeout = input_timeout  # Timeout for input
        self.print_function = print_function  # Custom print handler
        self._on_prompt_input = on_prompt_input  # Custom input prompt handler
        self.current_input: Optional[str] = None  # Store the current input
        self._input_event = threading.Event()  # Event to signal input readiness
        self.allow_input = True  # Flag to allow or block input setting

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """
        Mock the `print` function.

        Parameters
        ----------
        objects : Any
            The objects to print.
        sep : str, optional
            The separator, by default " ".
        end : str, optional
            The ending string, by default a new line.
        flush : bool, optional
            Whether to flush the output, by default False.
        """
        print_function: Callable[..., None] = self.print_function or print
        print_function(*objects, sep=sep, end=end, flush=flush)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """
        Mock the `input` function with optional timeout handling.

        Parameters
        ----------
        prompt : str, optional
            The prompt to show, by default "".
        password : bool, optional
            Whether to hide the input as password (not used), by default False.

        Returns
        -------
        str
            The user's input or '\n' if timeout occurs.
        """
        _prompt = prompt or "Your input:"
        if _prompt in (">", "> "):  # pragma: no cover
            _prompt = "Your input:"
        if prompt:
            if self._on_prompt_input:
                self._on_prompt_input(_prompt)
            self.print(_prompt, end="")

        # Only reset if no input is currently set
        # e.g. handle the case when we call set_input(..) before input(..)
        already_set = self._input_event.is_set()
        if not self._input_event.is_set():
            self.current_input = None  # Reset previous input
            self._input_event.clear()  # Clear the event before waiting

        # Wait for input or timeout
        if not self._input_event.wait(self.input_timeout):
            # Timeout occurred, return what we have so far
            to_return = (
                self.current_input if self.current_input is not None else "\n"
            )
            self.current_input = None
            self._input_event.clear()
            # if we had already set the input, return it
            return to_return if already_set else "\n"

        # Input is ready, return it
        to_return = (
            self.current_input if self.current_input is not None else "\n"
        )
        self.current_input = None
        self._input_event.clear()  # Clear the event after waiting
        return to_return

    def set_input(self, value: str) -> None:
        """
        Set the input value and signal that input is ready.

        Parameters
        ----------
        value : str
            The value to set as input.
        """
        if self.allow_input:  # Respect the allow_input flag
            self.current_input = value
            self._input_event.set()  # Signal that input is ready

    def reset_state(self) -> None:
        """Reset the IOStream state for testing."""
        self.current_input = None
        self._input_event.clear()
        self.allow_input = True  # Re-enable input setting
