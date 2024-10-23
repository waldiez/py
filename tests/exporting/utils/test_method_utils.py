"""Test waldiez.exporting.utils.method_utils.*."""

# pylint: disable=line-too-long
from waldiez.exporting.utils.method_utils import get_method_string
from waldiez.models import WaldiezMethodName


def test_get_method_string() -> None:
    """Test get_method_string."""
    # Given
    method_name: WaldiezMethodName = "callable_message"
    renamed_method_name = "callable_message_agent1"
    # When
    result = get_method_string(
        method_name=method_name,
        renamed_method_name=renamed_method_name,
        method_body="    return 'callable_message'",
    )
    # Then
    assert result == (
        "def callable_message_agent1(\n"
        "    sender,\n"
        "    recipient,\n"
        "    context,\n"
        "):\n"
        "    return 'callable_message'"
    )
    # Given
    method_name = "custom_embedding_function"
    renamed_method_name = "custom_embedding_function_agent1"
    # When
    result = get_method_string(
        method_name=method_name,
        renamed_method_name=renamed_method_name,
        method_body="    return lambda x: x",
    )
    # Then
    assert result == (
        "def custom_embedding_function_agent1():\n" "    return lambda x: x"
    )
