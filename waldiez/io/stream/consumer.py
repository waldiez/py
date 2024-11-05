"""TCP socket input consumer.

It connects to a TCP server,
listens for `INPUT:` messages to get the user's input,
and sends `REQUEST:` messages to prompt the user,
"""

import socket
import time
from types import TracebackType
from typing import Optional, Type

END_OF_MESSAGE = b"\r\n"


class TCPConsumer:
    """TCP socket input consumer."""

    def __init__(
        self, host: str, port: int, timeout: Optional[float] = None
    ) -> None:
        """Create a new input consumer.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect to.
        timeout : float, optional
            The timeout for the consumer, by default None (no timeout).
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._running = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    def __enter__(self) -> "TCPConsumer":
        """Enter the context."""
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the context."""
        self.stop()

    def is_running(self) -> bool:
        """Check if the consumer is running.

        Returns
        -------
        bool
            True is the consumer is running, else False
        """
        return self._running

    def start(self) -> None:
        """Start the consumer."""
        if self._running:
            return
        self._running = True
        self.socket.connect((self.host, self.port))
        self.socket.sendall("CONSUMER\r\n".encode("utf-8"))

    def _get_response_no_timeout(self) -> Optional[str]:
        """Get the response."""
        data = self.socket.recv(1024)
        while not data.endswith(END_OF_MESSAGE):
            data += self.socket.recv(1024)
        if data.startswith(b"INPUT:"):
            response = data[len(b"INPUT:") :]
            if response.endswith(END_OF_MESSAGE):
                response = response[: -len(END_OF_MESSAGE)]
            return response.decode("utf-8")
        return None

    def _get_response_with_timeout(self, timeout: float) -> Optional[str]:
        """Get the response using a timeout."""
        start_time = time.monotonic()
        data = b""
        self.socket.settimeout(timeout)
        while time.monotonic() - start_time < timeout:
            try:
                data += self.socket.recv(1024)
            except TimeoutError:
                return None
            if data.endswith(END_OF_MESSAGE):
                break
        if not data:
            return None
        if data.startswith(b"INPUT:"):
            response = data[len(b"INPUT:") :]
            if response.endswith(END_OF_MESSAGE):
                response = response[: -len(END_OF_MESSAGE)]
            return response.decode("utf-8")
        return None

    def get_response(self) -> Optional[str]:
        """Get the response.

        Returns
        -------
        Optional[str]
            The response if available, None otherwise.
        """
        if not self._running:
            self.start()
        if self.timeout is None or self.timeout < 1:
            return self._get_response_no_timeout()
        return self._get_response_with_timeout(self.timeout)

    def send_prompt(self, prompt: str) -> None:
        """Send a prompt.

        Parameters
        ----------
        prompt : str
            The prompt to send.
        """
        if not self._running:
            self.start()
        message = f"REQUEST:{prompt}" + "\r\n"
        self.socket.sendall(message.encode("utf-8"))

    def stop(self) -> None:
        """Close the consumer."""
        try:
            self.socket.close()
        except OSError:
            pass
        del self.socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._running = False
