"""Custom IOStream class to use with autogen.

It is meant to be used when we want to use custom
`print` and `input`. For example, when a websocket
is used to trigger a UI element that requires user input.
and sends back the user's input to the websocket. In the same
way, we can use it to forward what is meant to be printed.


We use:

- one tcp server to handle messaging between the clients
- one tcp client (provider) to set and forward the user's input
    that we got elsewhere (e.g. from a websocket connection)
- one tcp client (consumer) to ask and get the input from the provider
"""

import socket
from contextlib import closing
from typing import Any, Callable, Optional

from autogen.io import IOStream  # type: ignore[import-untyped]

from .stream import TCPConsumer, TCPProvider, TCPServer


class WaldiezIOStream(IOStream):
    """Custom IOStream class to handle the `print` and `input` functions."""

    def __init__(
        self,
        port: int = 0,
        input_timeout: float = 60,
        print_function: Optional[Callable[..., None]] = None,
        on_prompt_input: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Initialize the IOStream.

        Parameters
        ----------
        port : int, optional
            The port to use, by default 0 (auto-assign).
        input_timeout : float, optional
            The input timeout, by default 60.
        print_function : Optional[Callable[..., None]], optional
            The print function to use, by default None.
        on_prompt_input : Optional[Callable[[str], None]], optional
            The function to call for getting an input, by default None.
        """
        self._print_function = print_function
        if port == 0:
            port = get_available_port()
        self._port = port
        self._input_timeout = input_timeout
        self._server = TCPServer(port)
        self._server.start()
        self._provider = TCPProvider("localhost", port, response=None)
        self._on_prompt_input = on_prompt_input

    @property
    def print_function(self) -> Optional[Callable[..., None]]:
        """Get the print function."""
        return self._print_function

    def open(self) -> None:
        """Start the server."""
        if not self._server.is_running():
            self._server.start()

    def close(self) -> None:
        """Stop the server and the provider."""
        # pylint: disable=broad-except
        if self._server.is_running():
            try:
                self._server.stop()
            except BaseException:  # pragma: no cover
                pass
        try:
            self._provider.stop()
        except BaseException:  # pragma: no cover
            pass

    def __del__(self) -> None:  # pragma: no cover
        """Delete the instance."""
        self.close()

    def forward_input(self, input_data: str) -> None:
        """Forward the user's input to the provider.

        When we have the input data
            e.g. from 'input(..)' or from a websocket connection,
            we can forward it to the provider (the tcp client)
            to make it available to the consumer (the other tcp client).
        Parameters
        ----------
        input_data : str
            The input data to forward.
        """
        if not self._provider.is_running():
            self._provider.start()
        self._provider.set_response(input_data)

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """Mock the print function.

        Parameters
        ----------
        objects : Any
            The objects to print.
        sep : str, optional
            The separator, by default " ".
        end : str, optional
            The end, by default a new line.
        flush : bool, optional
            Whether to flush, by default False.
        """
        print_function: Callable[..., None] = self.print_function or print
        print_function(*objects, sep=sep, end=end, flush=flush)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """Mock the input function.

        Parameters
        ----------
        prompt : str, optional
            The prompt to show, by default "".
        password : bool, optional (not used)
            Whether to show the input as password, by default False.

        Returns
        -------
        str
            The user's input.
        """
        _prompt = prompt or "Your input:"
        if _prompt in (">", "> "):
            _prompt = "Your input:"
        if prompt:
            if self._on_prompt_input:
                self._on_prompt_input(_prompt)
            self.print(_prompt, end="")
        if not self._provider.is_running():
            self._provider.start()
        # wait for the provider to start
        self._provider.wait(timeout=self._input_timeout)
        if not self._provider.is_running():  # pragma: no cover
            self.print(
                "WARNING: Provider is not running. Was an input expected?"
            )
            return "\n"
        consumer = TCPConsumer(
            "localhost", self._port, timeout=self._input_timeout
        )
        consumer.start()
        # send the prompt and wait for the response
        consumer.send_prompt(_prompt)
        response = consumer.get_response()
        consumer.stop()
        self._provider.stop()
        # return the response or a line break (i.e. no input)
        return response or "\n"


def get_available_port() -> int:
    """Get an available port.

    Returns
    -------
    int
        Available port.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as soc:
        soc.bind(("", 0))
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return soc.getsockname()[1]
