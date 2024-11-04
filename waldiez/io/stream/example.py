"""Example usage of the server the provider and the consumer."""

import logging
import sys
from pathlib import Path

# pyright: reportMissingImports=false

try:
    from . import TCPConsumer, TCPProvider, TCPServer  # noqa
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent))
    from stream import (  # type: ignore # noqa
        TCPConsumer,
        TCPProvider,
        TCPServer,
    )


LOG_LEVEL = "ERROR"
if "--debug" in sys.argv:
    LOG_LEVEL = "DEBUG"
PORT = 8000
if "--port" in sys.argv:
    PORT = int(sys.argv[sys.argv.index("--port") + 1])


def _log(message: str) -> None:
    """Log the message."""
    logging.info(message)
    if LOG_LEVEL != "DEBUG":
        print(message)


def main() -> None:
    """Start the server and the two clients."""
    server = TCPServer(PORT)
    provider = TCPProvider("localhost", PORT)
    consumer = TCPConsumer("localhost", PORT)
    server.start()
    prompt = "Enter something. Enter exit or quit to stop: "
    user_input = input(prompt)
    while user_input not in ("exit", "quit"):
        provider.start()
        provider.wait(10)
        _log("Setting the provider's response to: " + user_input)
        consumer.start()
        provider.set_response(user_input)
        consumer.send_prompt(prompt)
        _log(f"Sent prompt: {prompt}")
        response = consumer.get_response()
        _log(f"Received: {response}")
        provider.stop()
        consumer.stop()
        user_input = input(prompt)
    provider.stop()
    server.stop()


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, stream=sys.stdout)
    main()
