"""Test waldiez.io_stream.*."""

from waldiez.io_stream import WaldieIOStream


def test_waldie_io_stream() -> None:
    """Test WaldieIOStream."""
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
        # `waldie_io_stream.forward_input(input_data)` with the input data.
        nonlocal input_prompt
        input_prompt = prompt

    waldie_io_stream = WaldieIOStream(
        print_function=print,
        on_prompt_input=on_prompt_input,
        input_timeout=2,
    )

    # when
    with WaldieIOStream.set_default(waldie_io_stream):
        # then
        waldie_io_stream.print("print")
        assert input_prompt == ""
        waldie_io_stream.forward_input("User's input")
        users_input = waldie_io_stream.input(">")
        assert users_input == "User's input"
        assert input_prompt == "Your input:"


def test_waldie_io_stream_no_input() -> None:
    """Test WaldieIOStream without an input value."""
    # Given
    waldie_io_stream = WaldieIOStream(print_function=print, input_timeout=1.1)

    # when
    with WaldieIOStream.set_default(waldie_io_stream):
        # then
        waldie_io_stream.print("print")
        users_input = waldie_io_stream.input("Enter something:")
        assert users_input == "\n"
