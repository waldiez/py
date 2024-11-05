"""Test waldiez.io.stream.provider.*."""

import socket
import time
import unittest
from typing import Any
from unittest.mock import Mock, patch

import pytest

from waldiez.io.stream.provider import END_OF_MESSAGE, TCPProvider


class MockSocket(Mock):
    """Mock socket."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a new mock socket object."""
        super().__init__(*args, **kwargs)
        self.recv = Mock(return_value=b"")
        self.sendall = Mock(return_value=None)
        self.connect = Mock(return_value=None)
        self.close = Mock(return_value=None)


# pylint: disable=no-self-use
class TestTCPProvider(unittest.TestCase):
    """Test TCPProvider."""

    @patch("socket.socket")
    def test_init(self, mock_socket: MockSocket) -> None:
        """Test __init__.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        _ = TCPProvider("localhost", 1234, response="response")

        mock_socket.assert_not_called()  # `run` is not called
        mock_socket.connect.assert_not_called()

    @patch("socket.socket")
    def test_start(self, mock_socket: MockSocket) -> None:
        """Test start.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, timeout=2)
        provider.start()

        mock_socket.assert_called_once_with(
            socket.AF_INET, socket.SOCK_STREAM, 0
        )
        mock_socket.connect.assert_called_once_with(("localhost", 1234))
        mock_socket.sendall.assert_called_once_with(b"PROVIDER\r\n")
        provider.stop()

    @patch("socket.socket")
    def test_start_twice(self, mock_socket: MockSocket) -> None:
        """Test start twice.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        # if we add a side_effect, "running" will be set to False
        # cause a message will be sent and the loop will stop
        # mock_socket.recv.side_effect = [b"PROVIDE:prompt"]

        provider = TCPProvider(
            "localhost",
            1234,
            response="response",
            timeout=10,
        )
        # pylint: disable=protected-access
        provider.start()
        provider.wait(2)
        self.assertTrue(provider.is_running())
        provider.start()
        self.assertTrue(provider._start_called)
        provider._start_called = False
        self.assertTrue(provider.is_running())
        provider.start()
        provider.stop()
        mock_socket.assert_called_once_with(
            socket.AF_INET, socket.SOCK_STREAM, 0
        )
        mock_socket.connect.assert_called_once_with(("localhost", 1234))
        self.assertEqual(
            mock_socket.sendall.mock_calls[0].args, (b"PROVIDER\r\n",)
        )

    @patch("socket.socket")
    def test_run_stop_twice(self, mock_socket: MockSocket) -> None:
        """Test run and stop twice.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, response="response")
        provider.start()
        provider.stop()
        provider.stop()

        no_calls = mock_socket.sendall.call_count
        self.assertGreaterEqual(no_calls, 1)
        self.assertIsNone(provider.thread)

    @patch("socket.socket")
    def test_set_response(self, mock_socket: MockSocket) -> None:
        """Test set_response.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.recv.side_effect = [b"PROVIDE:prompt\r\n"]

        provider = TCPProvider("localhost", 1234, response="other")
        self.assertEqual(provider.response, "other")
        provider.set_response("response")
        self.assertEqual(provider.response, "response")
        provider.start()
        time.sleep(1)

        mock_socket.sendall.assert_called_with(b"USE:response\r\n")

    @patch("socket.socket")
    def test_stop(self, mock_socket: MockSocket) -> None:
        """Test stopping the provider.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, response="response")
        provider.start()
        provider.stop()

        no_calls = mock_socket.sendall.call_count
        self.assertGreaterEqual(no_calls, 1)
        self.assertIsNone(provider.thread)

    @patch("socket.socket")
    def test_run_no_response(self, mock_socket: MockSocket) -> None:
        """Test run with no response.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234)
        provider.start()

        mock_socket.sendall.assert_called_once_with(b"PROVIDER\r\n")
        provider.stop()

    @patch("socket.socket")
    def test_run_with_timeout_no_prompt(self, mock_socket: MockSocket) -> None:
        """Test run with timeout and no prompt

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        ."""
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None
        mock_socket.recv.side_effect = [END_OF_MESSAGE]

        provider = TCPProvider(
            "localhost", 1234, response="response", timeout=2
        )
        provider.start()
        provider.wait(2)

        mock_socket.sendall.assert_called_once_with(b"PROVIDER\r\n")

    @patch("socket.socket")
    def test_restart(self, mock_socket: MockSocket) -> None:
        """Test restart.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, response="response")
        provider.start()

        mock_socket.connect.assert_called_once_with(("localhost", 1234))
        provider.restart()
        no_close_calls = mock_socket.close.call_count
        self.assertGreaterEqual(no_close_calls, 1)
        mock_socket.connect.assert_called_with(("localhost", 1234))

        self.assertIsNotNone(provider.thread)
        provider.stop()
        self.assertIsNone(provider.thread)

    @patch("socket.socket")
    def test_is_running(self, mock_socket: MockSocket) -> None:
        """Test is_running.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, response="response")
        self.assertFalse(provider.is_running())
        provider.start()
        self.assertTrue(provider.is_running())
        self.assertEqual(provider.response, "response")  # from the thread
        provider.set_response("other")
        self.assertEqual(provider.response, "other")
        provider.stop()
        self.assertFalse(provider.is_running())

    @patch("socket.socket")
    def test_wait(self, mock_socket: MockSocket) -> None:
        """Test wait.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        provider = TCPProvider("localhost", 1234, response="response")
        self.assertFalse(provider.is_running())
        provider.start()
        self.assertTrue(provider.is_running())
        provider.wait(1)
        provider.stop()
        self.assertFalse(provider.is_running())

    @patch("socket.socket")
    def test_provider_context_manager(self, mock_socket: MockSocket) -> None:
        """Test provider context manager.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        with TCPProvider("localhost", 1234, response="response") as provider:
            self.assertTrue(provider.is_running())
        self.assertFalse(provider.is_running())
        mock_socket.close.assert_called_once()

    @patch("socket.socket")
    def test_provider_no_timeout(self, mock_socket: MockSocket) -> None:
        """Test provider with no timeout.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.side_effect = [
            b"PROVIDE:prompt",
            END_OF_MESSAGE,
        ]
        provider = TCPProvider(
            "localhost",
            1234,
            response="response",
            timeout=None,
        )
        provider.start()
        provider.wait(2)
        mock_socket.sendall.assert_called_with(b"USE:response\r\n")
        provider.stop()

    @patch("socket.socket")
    def test_provider_no_timeout_no_provide_message(
        self,
        mock_socket: MockSocket,
    ) -> None:
        """Test provider with no provide message.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.side_effect = [b"NOT:prompt", END_OF_MESSAGE]
        provider = TCPProvider("localhost", 1234, response=None, timeout=None)
        provider.start()
        provider.wait(2)
        provider.stop()

    @patch("socket.socket")
    def test_provider_no_timeout_no_response(
        self,
        mock_socket: MockSocket,
    ) -> None:
        """Test catching errors in the provider.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        provider = TCPProvider("localhost", 1234, response=None, timeout=None)
        # pylint: disable=protected-access
        provider._wrapper = None
        self.assertIsNone(provider.response)
        self.assertIsNone(provider.thread)
        self.assertFalse(provider.is_running())
        with pytest.raises(RuntimeError):
            provider.set_response("response")
        with pytest.raises(RuntimeError):
            provider.start()
