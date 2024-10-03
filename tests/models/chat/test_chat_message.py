"""Test waldiez.models.chat.chat_message.*."""

from typing import Any, Dict, Optional, Union

import pytest
from typing_extensions import Literal

from waldiez.models.chat.chat_message import (
    WaldieChatMessage,
    validate_message_dict,
)


def test_waldie_chat_message() -> None:
    """Test WaldieChatMessage."""
    # Given
    message = WaldieChatMessage(
        type="string",
        content="Hello there",
        context={},
    )
    # Then
    assert message.type == "string"
    assert message.content == "Hello there"

    # Given
    message = WaldieChatMessage(
        type="method",
        content="Hello there",
        context={},
    )
    # Then
    assert message.type == "method"
    assert message.content == "Hello there"

    # Given
    message = WaldieChatMessage(
        type="none",
        content=None,
        context={},
    )
    # Then
    assert message.type == "none"
    assert message.content is None


def test_validate_message_dict() -> None:
    """Test validate_message_dict."""
    # Given
    message_content = """
def nested_chat_message(recipient, messages, sender, config):
    return "Hello there"
"""
    message_dict: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ] = {
        "type": "string",
        "content": message_content,
    }
    # When
    message = validate_message_dict(message_dict, "nested_chat_message")
    # Then
    assert message.type == "string"
    assert message.content == message_content

    # Given
    message_content = "Hello there"
    message_dict = {
        "type": "method",
        "content": message_content,
    }
    # Then
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "nested_chat_message")

    # Given
    message_dict = {
        "type": "none",
        "content": None,
    }
    # When
    message = validate_message_dict(message_dict, "nested_chat_message")
    # Then
    assert message.type == "none"
    assert message.content is None

    # Given
    message_dict = {
        "type": "string",
        "content": None,
    }
    # Then
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "nested_chat_message")

    # Given
    message_dict = {
        "type": "method",
        "content": "",
    }
    # Then
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "nested_chat_message")

    # Given
    message_dict = {
        "type": "invalid",
        "content": "",
    }
    # Then
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "nested_chat_message")

    # Given
    message_dict = {
        "type": 4,  # type: ignore
        "content": "",
        "context": {},
    }
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "nested_chat_message")


def test_last_carryover_message() -> None:
    """Test last_carryover_message."""
    # Given
    message_dict: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ] = {
        "type": "last_carryover",
        "content": "",
        "context": {},
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "method"
    assert message.content is not None
    assert "def callable_message" in message.content
    assert "carryover" in message.content
    assert "final_message" not in message.content
    assert message.context == {}

    # Given
    message_dict = {
        "type": "last_carryover",
        "content": "Hello there",
        "context": {
            "text": "Hello there.\nUse the carryover to complete the task.\n"
        },
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "method"
    assert message.content is not None
    assert "def callable_message" in message.content
    assert "carryover" in message.content
    assert "final_message" in message.content

    # Given
    message_dict = {
        "type": "last_carryover",
        "content": "Hello there",
        "context": {
            "text": 42,
        },
    }
    # Then
    message = validate_message_dict(message_dict, "callable_message")
    assert message.type == "method"
    assert message.content is not None
    assert "def callable_message" in message.content
    assert "carryover" in message.content
    assert "final_message" not in message.content
