"""Test waldiez.io_stream.*."""

from waldiez.io import WaldiezIOStream


def test_waldiez_io_stream() -> None:
    """Test WaldiezIOStream."""
    # Given

    input_prompt = ""

    def on_prompt_input(prompt: str) -> None:
        """On prompt input.

        Parameters
        ----------
        prompt : str
            The prompt.
        """
        # A more realistic example would be to send the prompt to a websocket
        # and when the user sends the input, we would call
        # `waldiez_io_stream.forward_input(input_data)` with the input data.
        nonlocal input_prompt
        input_prompt = prompt

    waldiez_io_stream = WaldiezIOStream(
        print_function=print,
        on_prompt_input=on_prompt_input,
        input_timeout=2,
    )

    # when
    with WaldiezIOStream.set_default(waldiez_io_stream):
        # then
        waldiez_io_stream.print("print")
        assert input_prompt == ""
        waldiez_io_stream.forward_input("User's input")
        users_input = waldiez_io_stream.input(">")
        assert users_input == "User's input"
        assert input_prompt == "Your input:"

    waldiez_io_stream.close()


def test_reuse_waldiez_io_stream() -> None:
    """Test reusing WaldiezIOStream."""
    # Given
    waldiez_io_stream = WaldiezIOStream(print_function=print, input_timeout=1.1)

    # when
    with WaldiezIOStream.set_default(waldiez_io_stream):
        # then
        waldiez_io_stream.print("print")
        users_input = waldiez_io_stream.input(">")
        assert users_input == "\n"
    waldiez_io_stream.close()
    # re open
    waldiez_io_stream.open()
    with WaldiezIOStream.set_default(waldiez_io_stream):
        waldiez_io_stream.print("print")
        users_input = waldiez_io_stream.input(">")
        assert users_input == "\n"
    waldiez_io_stream.close()


def test_waldiez_io_stream_no_input() -> None:
    """Test WaldiezIOStream without an input value."""
    # Given
    waldiez_io_stream = WaldiezIOStream(print_function=print, input_timeout=1.1)

    # when
    with WaldiezIOStream.set_default(waldiez_io_stream):
        # then
        waldiez_io_stream.print("print")
        users_input = waldiez_io_stream.input("Enter something:")
        assert users_input == "\n"
