"""TCP socket input provider.

It connects to a TCP server,
listens for `PROVIDE:` messages to receive prompts,
and sends `USE:` messages to pass the response.
"""

import logging
import socket
import threading
import time
from types import TracebackType
from typing import Optional, Type

END_OF_MESSAGE = b"\r\n"
LOGGER = logging.getLogger("tcp::provider")


class InputProviderThread(threading.Thread):
    """Input provider thread."""

    def __init__(
        self,
        host: str,
        port: int,
        response: Optional[str],
        timeout: Optional[float] = None,
    ) -> None:
        """Create a new input provider thread.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect to.
        response : str, optional
            The response to send.
        timeout : float, optional
            The timeout for the provider, by default None (no timeout).
        """
        super().__init__(
            name="InputProviderThread",
            daemon=True,
            target=self.run,
        )
        self.host = host
        self.port = port
        self.timeout = timeout
        self._response = response
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.running = False

    @property
    def response(self) -> Optional[str]:
        """Get the response."""
        return self._response

    @response.setter
    def response(self, response: str) -> None:
        """Set the response.

        Parameters
        ----------
        response : str
            The response to set.
        """
        self._response = response

    def _run_no_timeout(self) -> None:
        """Start the provider."""
        self.socket.connect((self.host, self.port))
        self.socket.sendall("PROVIDER\r\n".encode("utf-8"))
        self.running = True
        while self.running:
            data = b""
            while not data.endswith(END_OF_MESSAGE):
                try:
                    data += self.socket.recv(1024)
                except BaseException:  # pylint: disable=broad-except
                    break
            if not data:
                break
            if data.startswith(b"PROVIDE:"):
                prompt = data[len(b"PROVIDE:") : -len(END_OF_MESSAGE)]
                LOGGER.debug("Got a prompt: %s", prompt)
                if self.response:
                    message = f"USE:{self.response}" + "\r\n"
                    self.socket.sendall(message.encode("utf-8"))
        self.socket.close()
        self.running = False

    def _run_with_timeout(self, timeout: float) -> None:
        """Start the provider with a timeout."""
        self.socket.connect((self.host, self.port))
        self.socket.sendall("PROVIDER\r\n".encode("utf-8"))
        self.running = True
        start_time = time.monotonic()
        while self.running:
            data = b""
            while time.monotonic() - start_time < timeout:
                try:
                    data += self.socket.recv(1024)
                except BaseException:  # pylint: disable=broad-except
                    break
                if data.endswith(END_OF_MESSAGE):
                    break
            if not data:
                break
            if data.startswith(b"PROVIDE:"):
                prompt = data[len(b"PROVIDE:") : -len(END_OF_MESSAGE)]
                LOGGER.debug("Got a prompt: %s", prompt)
                if self.response:
                    message = f"USE:{self.response}" + "\r\n"
                    self.socket.sendall(message.encode("utf-8"))
        self.socket.close()
        self.running = False

    def run(self) -> None:
        """Run the provider."""
        if self.timeout is None or self.timeout < 1:
            self._run_no_timeout()
        else:
            self._run_with_timeout(self.timeout)


class InputProviderWrapper:
    """Input provider wrapper."""

    thread: Optional[InputProviderThread] = None

    def __init__(
        self,
        host: str,
        port: int,
        response: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """Create a new input provider wrapper.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect to.
        response : str, optional
            The response to send.
        timeout : float, optional
            The timeout for the provider, by default None (no timeout).
        """
        self._host = host
        self._port = port
        self._timeout = timeout
        self._response = response

    @property
    def response(self) -> Optional[str]:
        """Get the response."""
        if self.thread:
            return self.thread.response
        return self._response

    def start(self) -> None:
        """Start the provider."""
        self.thread = InputProviderThread(
            self._host, self._port, self._response, self._timeout
        )
        self.thread.daemon = True
        self.thread.start()

    def set_response(self, response: str) -> None:
        """Set the response.

        Parameters
        ----------
        response : str
            The response to set.
        """
        self._response = response
        if self.thread:
            self.thread.response = response

    def stop(self) -> None:
        """Stop the provider."""
        if self.thread:
            self.thread.running = False
            self.thread.join(timeout=1)
            del self.thread
            self.thread = None


class TCPProvider:
    """Input provider."""

    _wrapper: Optional[InputProviderWrapper] = None

    def __init__(
        self,
        host: str,
        port: int,
        response: Optional[str] = None,
        timeout: Optional[float] = 30,
    ) -> None:
        """Create a new input provider.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect to.
        response : str, optional
            The response to send.
        timeout : float, optional
            The timeout for the provider, by default 30.
        """
        self._host = host
        self._port = port
        self._response = response
        self._timeout = timeout
        self._start_called = False
        self._init_wrapper()

    def __enter__(self) -> "TCPProvider":
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

    @property
    def thread(self) -> Optional[InputProviderThread]:
        """Get the thread."""
        if not self._wrapper:
            return None
        return self._wrapper.thread

    @property
    def response(self) -> Optional[str]:
        """Get the response."""
        if self._wrapper:
            return self._wrapper.response
        return self._response

    def _init_wrapper(self) -> None:
        """Initialize the wrapper."""
        self._wrapper = InputProviderWrapper(
            host=self._host,
            port=self._port,
            response=self._response,
            timeout=self._timeout,
        )

    def is_running(self) -> bool:
        """Check if the provider is running.

        Returns
        -------
        bool
            True if the provider is running, False otherwise.
        """
        if not self._wrapper:
            return False
        if not self.thread:
            return False
        return self.thread.running is True

    def wait(self, timeout: float) -> None:
        """Wait until the provider is running.

        Parameters
        ----------
        timeout : float
            The timeout to wait.
        """
        start_time = time.time()
        while not self.is_running():
            if time.time() - start_time > timeout:
                break
            time.sleep(1)

    def start(self) -> None:
        """Start the provider.

        Raises
        ------
        RuntimeError
            If the wrapper is not initialized.
        """
        # avoid starting the provider multiple times
        # (if the wrapped thread has not yet started)
        if self._start_called is True:
            return
        self._start_called = True
        if self.is_running():
            return
        if not self._wrapper:
            raise RuntimeError("Wrapper not initialized")
        self._wrapper.start()

    def set_response(self, response: str) -> None:
        """Set the response.

        Parameters
        ----------
        response : str
            The response to set.

        Raises
        ------
        RuntimeError
            If the wrapper is not initialized.
        """
        if not self._wrapper:
            raise RuntimeError("Wrapper not initialized")
        self._wrapper.set_response(response or "\n")

    def stop(self) -> None:
        """Stop the provider."""
        self._start_called = False
        if not self.is_running():
            return
        if self._wrapper:
            self._wrapper.stop()
        del self._wrapper
        self._init_wrapper()

    def restart(self) -> None:
        """Restart the provider."""
        self.stop()
        self.start()
