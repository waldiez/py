"""Test waldiez.io.stream.consumer.*."""

import socket
import unittest
from typing import Any
from unittest.mock import Mock, patch

from waldiez.io.stream.consumer import END_OF_MESSAGE, TCPConsumer


class MockSocket(Mock):
    """Mock socket."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a new mock socket object."""
        super().__init__(*args, **kwargs)
        self.recv = Mock(return_value=b"")
        self.sendall = Mock(return_value=None)
        self.connect = Mock(return_value=None)
        self.close = Mock(return_value=None)
        self.settimeout = Mock(return_value=None)


# pylint: disable=no-self-use
class TestTCPConsumer(unittest.TestCase):
    """Test TCPConsumer."""

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
        mock_socket.settimeout.return_value = None

        consumer = TCPConsumer("localhost", 1234)
        consumer.start()

        mock_socket.assert_called_once_with(
            socket.AF_INET, socket.SOCK_STREAM, 0
        )
        mock_socket.connect.assert_called_once_with(("localhost", 1234))
        mock_socket.sendall.assert_called_once_with(
            "CONSUMER\r\n".encode("utf-8")
        )

    @patch("socket.socket")
    def test_get_response(self, mock_socket: MockSocket) -> None:
        """Test get_response.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.settimeout.return_value = None
        # avoid StopIteration error
        mock_socket.recv.side_effect = [b"INPUT:response\r\n", b""]
        # mock_socket.recv.return_value = b"response\r\nINPUT:response"
        # safe to have a high timeout (we do get a response)
        consumer = TCPConsumer("localhost", 1234, timeout=30)
        consumer.start()
        response = consumer.get_response()
        self.assertEqual(response, "response")
        mock_socket.recv.assert_called_with(1024)

    # the ones below give timeout errors
    @patch("socket.socket")
    def test_get_response_no_data(self, mock_socket: MockSocket) -> None:
        """Test get_response with no data.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.return_value = b""

        consumer = TCPConsumer("localhost", 1234, timeout=1.1)

        response = consumer.get_response()

        self.assertIsNone(response)

    @patch("socket.socket")
    def test_get_response_no_input(self, mock_socket: MockSocket) -> None:
        """Test get_response with no input.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.return_value = b""

        consumer = TCPConsumer("localhost", 1234, timeout=1.1)

        response = consumer.get_response()

        self.assertIsNone(response)

    @patch("socket.socket")
    def test_get_response_invalid_input(self, mock_socket: MockSocket) -> None:
        """Test get_response with invalid input.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.return_value = b"INVALID:response\r\n"

        consumer = TCPConsumer("localhost", 1234, timeout=1.1)

        response = consumer.get_response()

        self.assertIsNone(response)

    @patch("socket.socket")
    def test_get_response_no_end_of_message(
        self, mock_socket: MockSocket
    ) -> None:
        """Test get_response with no end of message.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.side_effect = [
            b"INPUT:response",
            b"\r\n",
            b"END_OF_MESSAGE",
        ]

        consumer = TCPConsumer("localhost", 1234)

        response = consumer.get_response()

        self.assertEqual(response, "response")

        mock_socket.recv.assert_called_with(1024)

    @patch("socket.socket")
    def test_send_prompt(self, mock_socket: MockSocket) -> None:
        """Test send_prompt.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.sendall.return_value = None

        consumer = TCPConsumer("localhost", 1234)

        consumer.send_prompt("prompt")

        mock_socket.sendall.assert_called_with(
            "REQUEST:prompt\r\n".encode("utf-8")
        )
        # Calls: [call(b'CONSUMER\r\n'), call(b'REQUEST:prompt\r\n')]
        assert mock_socket.sendall.call_count == 2

    @patch("socket.socket")
    def test_stop(self, mock_socket: MockSocket) -> None:
        """Test stopping the consumer.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.close.return_value = None

        consumer = TCPConsumer("localhost", 1234)

        consumer.stop()

        mock_socket.close.assert_called_once_with()

    @patch("socket.socket")
    def test_consumer_context_manager(self, mock_socket: MockSocket) -> None:
        """Test consumer context manager.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.close.return_value = None

        with TCPConsumer("localhost", 1234) as consumer:
            self.assertTrue(consumer.is_running())

        mock_socket.close.assert_called_once_with()

    @patch("socket.socket")
    def test_consumer_call_start_twice(self, mock_socket: MockSocket) -> None:
        """Test calling start twice.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.connect.return_value = None
        mock_socket.sendall.return_value = None

        consumer = TCPConsumer("localhost", 1234)
        consumer.start()
        consumer.start()

    @patch("socket.socket")
    def test_consumer_no_response(self, mock_socket: MockSocket) -> None:
        """Test consumer with no response.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.return_value = END_OF_MESSAGE

        consumer = TCPConsumer("localhost", 1234, timeout=None)
        consumer.start()
        response = consumer.get_response()

        self.assertIsNone(response)

    @patch("socket.socket")
    def test_consumer_no_input_in_response(
        self, mock_socket: MockSocket
    ) -> None:
        """Test consumer with no input in response.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.recv.return_value = b"INVALID:response" + END_OF_MESSAGE

        consumer = TCPConsumer("localhost", 1234, timeout=None)
        consumer.start()
        response = consumer.get_response()
        consumer.stop()
        self.assertIsNone(response)

    @patch("socket.socket")
    def test_consumer_os_error(self, mock_socket: MockSocket) -> None:
        """Test consumer with OSError.

        Parameters
        ----------
        mock_socket : MockSocket
            The mock socket.
        """
        mock_socket.return_value = mock_socket
        mock_socket.close.side_effect = OSError

        consumer = TCPConsumer("localhost", 1234)
        consumer.stop()
