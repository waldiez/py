"""Simple TCP server using twisted.

It listens for connections from an input provider and an input consumer,
and forwards messages between them.
"""

# pylint: disable=import-outside-toplevel,no-member,reimported,unused-import,redefined-outer-name,invalid-name  # noqa
import logging
import sys
from threading import Thread
from types import TracebackType
from typing import Dict, Optional, Type, cast

from twisted.internet.error import ReactorNotRestartable
from twisted.internet.interfaces import IReactorCore
from twisted.internet.protocol import Factory, Protocol, connectionDone
from twisted.internet.tcp import Port
from twisted.python.failure import Failure

LOGGER = logging.getLogger("tcp::server")
END_OF_MESSAGE = b"\r\n"


class ServerProtocol(Protocol):
    """Server protocol."""

    factory: "ServerFactory"

    def set_factory(self, factory: "ServerFactory") -> None:
        """Set the factory.

        Parameters
        ----------
        factory : ServerFactory
            The factory to set.
        """
        self.factory = factory

    def connectionLost(self, reason: Failure = connectionDone) -> None:
        """Handle connection lost event.

        Parameters
        ----------
        reason : Failure, optional
            The reason for the connection loss, by default connectionDone
        """
        if self.factory.clients["provider"] == self:
            self.factory.clients["provider"] = None
            LOGGER.info("Input provider disconnected.")
        elif self.factory.clients["consumer"] == self:
            self.factory.clients["consumer"] = None
            LOGGER.info("Input consumer disconnected.")
        super().connectionLost(reason)

    def message_received(self, message: str) -> None:
        """Handle a message received event.

        Parameters
        ----------
        message : str
            The message received.
        """
        if message.startswith("REQUEST:"):
            prompt = message[len("REQUEST:") :]
            if prompt.endswith("\r\n"):
                prompt = prompt[: -(len("\r\n"))]
            prompt = prompt.strip()
            LOGGER.debug("Received request: %s", prompt)
            if self.factory.clients["provider"]:
                msg = f"PROVIDE:{prompt}" + "\r\n"
                transport = self.factory.clients["provider"].transport
                transport.write(msg.encode("utf-8"))  # type: ignore
            else:
                LOGGER.error("No provider connected.")
        elif message.startswith("USE:"):
            response = message[len("USE:") :]
            if response.endswith("\r\n"):
                response = response[: -(len("\r\n"))]
            response = response.strip()
            LOGGER.debug("Received response: %s", response)
            if self.factory.clients["consumer"]:
                msg = f"INPUT:{response}" + "\r\n"
                transport = self.factory.clients["consumer"].transport
                transport.write(msg.encode("utf-8"))  # type: ignore
            else:
                LOGGER.error("No consumer connected.")

    def dataReceived(self, data: bytes) -> None:
        """Handle a data received event.

        Parameters
        ----------
        data : bytes
            The data received.
        """
        # we might get multiple messages in one chunk
        # i.e. CONSUMER\r\nREQUEST:prompt\r\n
        message = data.decode("utf-8")
        if message in ("PROVIDER\r\n", "PROVIDER\n", "PROVIDER"):
            LOGGER.debug("Input provider connected.")
            self.factory.clients["provider"] = self
            return
        if message.startswith("CONSUMER\r\n"):
            LOGGER.debug("Input consumer connected.")
            self.factory.clients["consumer"] = self
            rest = message[len("CONSUMER\r\n") :]
            if rest:
                self.message_received(rest)
            return
        self.message_received(message)


class ServerFactory(Factory):
    """Server factory."""

    protocol: "ServerProtocol"  # type: ignore
    clients: Dict[str, Optional["ServerProtocol"]]

    def __init__(self) -> None:
        """Initialize the factory."""
        super().__init__()
        self.clients = {
            "provider": None,
            "consumer": None,
        }

    def buildProtocol(self, addr: str) -> "ServerProtocol":
        """Build the protocol.

        Parameters
        ----------
        addr : str
            The address (ignored)

        Returns
        -------
        ServerProtocol
            The factory's protocol.
        """
        self.protocol = ServerProtocol()
        self.protocol.set_factory(self)
        return self.protocol


def get_reactor() -> IReactorCore:
    """Get the reactor from twisted.

    Returns
    -------
    IReactorCore
        The twisted's reactor
    """
    # dummy hack to allow restarting the reactor
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
    import twisted.internet.error
    from twisted.internet import reactor  # noqa
    from twisted.internet import default

    try:
        default.install()
    # pylint: disable=line-too-long
    except (
        twisted.internet.error.ReactorAlreadyInstalledError
    ):  # pragma: no cover
        pass
    # cast it so mypy doesn't complain a lot
    reactor_cast = cast(IReactorCore, reactor)
    return reactor_cast


class TCPServerThread(Thread):
    """Threaded TCP server."""

    reactor: Optional[IReactorCore] = None  # noqa
    factory: Optional[Factory] = None  # noqa

    def __init__(
        self,
        interface: str,
        port: int,
        timeout: Optional[float] = None,
    ) -> None:
        """Create a new TCP server.

        Parameters
        ----------
        interface : str
            Interface to listen on. Defaults to '' (all interfaces)
        port : int
            Port to listen on.
        timeout : Optional[float]
            Timeout for the server.
        """
        super().__init__(
            name="TCPServerThread",
            daemon=True,
            target=self.run,
        )
        from twisted.internet.endpoints import TCP4ServerEndpoint

        self.timeout = timeout
        self.reactor = get_reactor()
        self._port = port
        endpoint = TCP4ServerEndpoint(  # type: ignore[no-untyped-call]
            self.reactor,
            port,
            interface=interface,
        )
        server_factory = ServerFactory()
        deferred = endpoint.listen(server_factory)  # type: ignore
        deferred.addCallback(callback=self.on_start)

    @property
    def port(self) -> int:
        """Get the port."""
        return self._port

    def on_start(self, port: Port) -> None:
        """On connect callback.

        Parameters
        ----------
        port : Port
            The port to connect to.
        """
        socket = port.getHost()  # type: ignore[no-untyped-call]
        LOGGER.debug(
            "listening on %s:%s",
            socket.host,
            socket.port,
        )
        self._port = socket.port
        self.factory = port.factory

    def run(self) -> None:
        """Start the server.

        Raises
        ------
        RuntimeError
            If reactor is not initialized
        """
        if self.reactor is None:  # pragma: no cover (just for the linter)
            raise RuntimeError("reactor is not running")
        if not self.reactor.running:
            try:
                self.reactor.run(installSignalHandlers=False)  # type: ignore
            except ReactorNotRestartable:  # pragma: no cover
                self.reactor = get_reactor()
                self.reactor.run(installSignalHandlers=False)  # type: ignore


class ServerWrapper:
    """Server Wrapper."""

    server: TCPServerThread
    timeout: float

    def __init__(
        self,
        interface: str,
        port: int,
        timeout: Optional[float] = None,
    ) -> None:
        """Create a new TCP server.

        Parameters
        ----------
        interface : str
            Interface to listen on. Defaults to '' (all interfaces)
        port : int
            Port to listen on.
        """
        self.timeout = timeout if timeout is not None else 0.2
        self.server = TCPServerThread(
            interface=interface, port=port, timeout=self.timeout
        )

    @property
    def port(self) -> int:
        """Get the port.

        Raises
        ------
        RuntimeError
            If the server is not running
        """
        if self.server.factory is None:
            raise RuntimeError("server is not running")
        return self.server.port

    def start(self) -> None:
        """Start the server.

        Raises
        ------
        RuntimeError
            If the server is not running
        """
        if self.server is None:
            raise RuntimeError("server is not running")
        self.server.start()

    def stop(self) -> None:
        """Stop the server."""
        # pylint: disable=line-too-long
        self.server.reactor.callFromThread(self.server.reactor.stop)  # type: ignore  # noqa
        self.server.join()


class TCPServer:
    """TCP Server."""

    _wrapper: Optional[ServerWrapper] = None

    def __init__(
        self,
        port: int,
        timeout: Optional[float] = None,
        interface: str = "",
    ) -> None:
        """Create a new server.

        Parameters
        ----------
        port : int
            Port to listen on.
        timeout : Optional[float]
            Timeout for the server.
        interface : str
            Interface to listen on. Defaults to '' (all interfaces)
        """
        self._port = port
        self._timeout = timeout
        self._interface = interface
        self._init_wrapper()
        self._running = False

    @property
    def port(self) -> int:
        """Get the port."""
        if self._wrapper is None:
            return self._port
        return self._wrapper.port

    def _init_wrapper(self) -> None:
        """Initialize the wrapper."""
        self._wrapper = ServerWrapper(
            port=self._port,
            timeout=self._timeout,
            interface=self._interface,
        )

    def start(self) -> None:
        """Start the server.

        Raises
        ------
        RuntimeError
            If the wrapper is not initialized
        """
        if self._running:
            return
        if not self._wrapper:
            self._init_wrapper()
        if not self._wrapper:  # pragma: no cover (just for the linter)
            raise RuntimeError("Server wrapper is not initialized")
        self._wrapper.start()
        self._port = self._wrapper.port
        self._running = True

    def stop(self) -> None:
        """Stop the server."""
        if not self._running:
            return
        if not self._wrapper:  # pragma: no cover (just for the linter)
            return
        self._wrapper.stop()
        self._running = False
        del self._wrapper
        self._wrapper = None

    def is_running(self) -> bool:
        """Check if the server is running.

        Returns
        -------
        bool
            True if the server is running, else False.
        """
        return self._running

    def __enter__(self) -> "TCPServer":
        """Enter the context manager."""
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the context manager."""
        self.stop()

    def restart(self) -> None:
        """Restart the server."""
        self.stop()
        self._init_wrapper()
        self.start()
