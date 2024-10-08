"""Test waldiez.models.chat.chat_message.*."""

from typing import Any, Dict, Optional, Union

import pytest
from typing_extensions import Literal

from waldiez.models.chat import (
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
    WaldieChatSummary,
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


def test_rag_message_generator_message() -> None:
    """Test rag_message_generator_message."""
    # Given
    message_dict: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ] = {
        "type": "rag_message_generator",
        "content": None,
        "context": {},
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "rag_message_generator"
    assert message.content is None
    assert message.context == {}

    # Given
    message_dict = {
        "type": "rag_message_generator",
        "content": "Hello there",
        "context": {},
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "rag_message_generator"
    assert message.content is None
    assert message.context == {}

    # Given
    message_dict = {
        "type": "rag_message_generator",
        "content": None,
        "context": {
            "n_results": 5,
        },
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "rag_message_generator"
    assert message.content is None
    assert message.context == {"n_results": 5}

    # Given
    message_dict = {
        "type": "rag_message_generator",
        "content": None,
        "context": {
            "n_results": "5",
        },
    }
    # When
    message = validate_message_dict(message_dict, "callable_message")
    # Then
    assert message.type == "rag_message_generator"
    assert message.content is None
    assert message.context == {"n_results": "5"}

    # Given
    chat = WaldieChat(
        id="chat_id",
        data=WaldieChatData(
            name="chat_name",
            description="Chat description",
            source="source",
            target="target",
            message=WaldieChatMessage(
                type="rag_message_generator",
                content=None,
                context={
                    "n_results": "5",
                    "problem": "Solve this task",
                },
            ),
            position=0,
            order=0,
            clear_history=False,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
            max_turns=1,
            silent=False,
            real_source=None,
            real_target=None,
            summary=WaldieChatSummary(
                method="last_msg",
                prompt="Return the last message",
                args={},
            ),
        ),
    )
    # When
    chat_args = chat.get_chat_args()
    # Then
    assert chat_args == {
        "clear_history": False,
        "max_turns": 1,
        "summary_method": "last_msg",
        "problem": "Solve this task",
        "silent": False,
        "n_results": 5,
    }

    # Given
    message_dict = {
        "type": "invalid",
        "content": None,
        "context": {
            "n_results": 3,
        },
    }
    # Then
    with pytest.raises(ValueError):
        validate_message_dict(message_dict, "callable_message")

    # Given
    message_dict = {
        "type": "rag_message_generator",
        "content": None,
        "context": {
            "problem": "Solve this task",
            "n_results": 5,
        },
    }
    # Then
    message = validate_message_dict(message_dict, "callable_message")
    assert message.type == "rag_message_generator"
    assert message.content is None
