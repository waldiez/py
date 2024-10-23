"""Test waldiez.models.common.method_utils.*."""

import ast

from waldiez.models.common.method_utils import (
    WaldiezMethodName,
    check_function,
    parse_code_string,
)


def test_parse_code_string() -> None:
    """Test parse_code_string."""
    # Given
    code_string = "def test():\n    return 42"
    # When
    error, tree = parse_code_string(code_string)
    # Then
    assert error is None
    assert tree is not None
    assert isinstance(tree, ast.Module)

    # Given
    code_string = "def test():\n   4x = 2\n"
    # When
    error, tree = parse_code_string(code_string)
    assert error is not None
    assert tree is None
    assert "SyntaxError" in error


def test_check_function() -> None:
    """Test check_function."""
    # Given
    code_string = """
def callable_message(sender, recipient, context):
    return "Hello"
    """
    function_name: WaldiezMethodName = "callable_message"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert valid
    assert body == (
        "    # type: (ConversableAgent, ConversableAgent, dict) -> "
        'Union[dict, str]\n    return "Hello"'
    )

    # Given
    code_string = """
def callable_message(sender, recipient, context):
    return "Hello"
    """
    function_name = "invalid_function"  # type: ignore[assignment]
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert not valid
    assert "Invalid function name" in body

    # Given
    code_string = """
def callable_message(other, context):
    return "Hello"
    """
    function_name = "callable_message"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert not valid
    assert "Invalid number of arguments" in body
    # Given
    code_string = """
def is_termination_message(x):
    return True
    """
    function_name = "is_termination_message"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert not valid
    assert "Invalid argument name" in body

    # Given
    code_string = """
def is_termination_message(4):
    return True
    """
    function_name = "is_termination_message"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert not valid
    assert "SyntaxError" in body

    # Given
    code_string = """
def some_other_function(sender, recipient, context):
    return "Hello"

def nested_chat_reply(recipient, messages, sender, config):
    return "Hello"
    """
    function_name = "nested_chat_reply"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert valid
    assert body == (
        "    # type: (ConversableAgent, list[dict], ConversableAgent, dict) -> "
        'Union[dict, str]\n    return "Hello"'
    )

    # Given
    code_string = """
def nested_chat_reply_(recipient, messages, sender, config):
    return "Hello"
    """
    function_name = "nested_chat_reply"
    # When
    valid, body = check_function(code_string, function_name)
    # Then
    assert not valid
    assert "No function with name" in body
