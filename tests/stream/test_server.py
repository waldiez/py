# type: ignore
"""Test waldiez.io.stream.server.*."""

import socket

import pytest
from twisted.trial import unittest

from waldiez.io.stream import TCPConsumer, TCPProvider, TCPServer

# DeprecationWarning: reactor.stop cannot be used inside unit tests


class TestTCPServer(unittest.TestCase):
    """Test TCPServer."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.server = TCPServer(0)

    def test_start(self) -> None:
        """Test start."""
        self.server.start()
        self.assertTrue(self.server.is_running())

    def test_start_twice(self) -> None:
        """Test start twice."""
        self.server.start()
        self.assertTrue(self.server.is_running())
        self.server.start()
        self.assertTrue(self.server.is_running())

    def test_stop(self) -> None:
        """Test stop."""
        with pytest.warns(DeprecationWarning):
            self.server.start()
            self.server.stop()
        self.assertFalse(self.server.is_running())

    def test_stop_twice(self) -> None:
        """Test stop twice."""
        with pytest.warns(DeprecationWarning):
            self.server.start()
            self.server.stop()
            self.assertFalse(self.server.is_running())
            self.server.stop()
            self.assertFalse(self.server.is_running())

    def test_restart(self) -> None:
        """Test restart."""
        with pytest.warns(DeprecationWarning):
            self.server.start()
            self.server.restart()
            self.assertTrue(self.server.is_running())
            self.server.stop()
            self.assertFalse(self.server.is_running())


class TestTCPServerContextManager(unittest.TestCase):
    """Test TCPServer with context manager."""

    def test_context_manager(self) -> None:
        """Test context manager."""
        with pytest.warns(DeprecationWarning):
            with TCPServer(0) as server:
                self.assertTrue(server.is_running())
            self.assertFalse(server.is_running())


class TestTCPServerWithClients(unittest.TestCase):
    """Test TCPServer with clients."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.server = TCPServer(0, timeout=5)

    def test_connections(self) -> None:
        """Test start."""
        self.server.start()
        self.assertTrue(self.server.is_running())
        provider = TCPProvider(
            "localhost", self.server.port, response="response"
        )
        provider.start()
        provider.wait(timeout=2)
        self.assertTrue(provider.is_running())
        consumer = TCPConsumer("localhost", self.server.port, timeout=10)
        consumer.start()
        consumer.send_prompt("prompt")
        response = consumer.get_response()
        self.assertEqual(response, "response")
        provider.stop()
        consumer.stop()
        with pytest.warns(DeprecationWarning):
            self.server.stop()

    def test_no_consumer(self) -> None:
        """Test run without a consumer connection."""
        self.server.start()
        self.assertTrue(self.server.is_running())
        provider = TCPProvider(
            "localhost", self.server.port, response="response"
        )
        provider.start()
        provider.wait(timeout=2)
        self.assertTrue(provider.is_running())
        # send a "USE:" message to the server
        other_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        other_client.connect(("localhost", self.server.port))
        other_client.sendall(b"USE:response\r\n")
        other_client.close()
        provider.stop()
        with pytest.warns(DeprecationWarning):
            self.server.stop()

    def test_no_provider(self) -> None:
        """Test run without a provider connection."""
        self.server.start()
        self.assertTrue(self.server.is_running())
        consumer = TCPConsumer("localhost", self.server.port, timeout=2)
        consumer.start()
        consumer.send_prompt("prompt")
        response = consumer.get_response()
        consumer.stop()
        self.assertIsNone(response)
        consumer.stop()
        with pytest.warns(DeprecationWarning):
            self.server.stop()

    def test_unknown_message(self) -> None:
        """Test run with an unknown message."""
        self.server.start()
        self.assertTrue(self.server.is_running())
        # send an unknown message to the server
        other_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        other_client.connect(("localhost", self.server.port))
        other_client.sendall(b"UNKNOWN\r\n")
        other_client.close()
        with pytest.warns(DeprecationWarning):
            self.server.stop()
