"""Test waldiez.models.chat.chat_message.*."""

from typing import Any, Dict, Optional, Union

import pytest
from typing_extensions import Literal

from waldiez.models.chat import (
    WaldiezChat,
    WaldiezChatData,
    WaldiezChatMessage,
    WaldiezChatNested,
    WaldiezChatSummary,
    validate_message_dict,
)
from waldiez.models.chat.chat_message import RAG_METHOD_WITH_CARRYOVER


def test_waldiez_chat_message() -> None:
    """Test WaldiezChatMessage."""
    # Given
    message = WaldiezChatMessage(
        type="string",
        use_carryover=False,
        content="Hello there",
        context={},
    )
    # Then
    assert message.type == "string"
    assert message.content == "Hello there"

    # Given
    message = WaldiezChatMessage(
        type="method",
        use_carryover=False,
        content="Hello there",
        context={},
    )
    # Then
    assert message.type == "method"
    assert message.content == "Hello there"

    # Given
    message = WaldiezChatMessage(
        type="none",
        use_carryover=False,
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
        Literal["type", "use_carryover", "content", "context"],
        Union[Optional[str], Optional[bool], Optional[Dict[str, Any]]],
    ] = {
        "type": "string",
        "use_carryover": False,
        "content": message_content,
    }
    # When
    message = validate_message_dict(message_dict, "nested_chat_message")
    # Then
    assert message.type == "string"
    assert message.content == message_content

    # Given
    message_dict = {
        "type": "string",
        "content": "Hello there",
        "use_carryover": True,
    }
    # Then
    message = validate_message_dict(message_dict, "callable_message")
    assert message.type == "method"
    assert (
        message.content
        == '''
def callable_message(sender, recipient, context):
    # type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]
    """Get the message to send using the last carryover.

    Parameters
    ----------
    sender : ConversableAgent
        The source agent.
    recipient : ConversableAgent
        The target agent.
    context : dict
        The context.

    Returns
    -------
    Union[dict, str]
        The message to send using the last carryover.
    """
    carryover = context.get("carryover", "")
    if isinstance(carryover, list):
        carryover = carryover[-1]
    if not isinstance(carryover, str):
        carryover = ""
    final_message = "Hello there" + carryover
    return final_message
'''
    )

    # Given
    message_dict = {
        "type": "string",
        "content": "",
        "use_carryover": True,
    }
    # Then
    message = validate_message_dict(message_dict, "callable_message")
    assert message.type == "method"
    assert (
        message.content
        == '''
def callable_message(sender, recipient, context):
    # type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]
    """Get the message to send using the last carryover.

    Parameters
    ----------
    sender : ConversableAgent
        The source agent.
    recipient : ConversableAgent
        The target agent.
    context : dict
        The context.

    Returns
    -------
    Union[dict, str]
        The message to send using the last carryover.
    """
    carryover = context.get("carryover", "")
    if isinstance(carryover, list):
        carryover = carryover[-1]
    if not isinstance(carryover, str):
        carryover = ""
    return carryover
'''
    )
    # Given
    message_dict = {
        "type": "rag_message_generator",
        "content": "Hello there",
        "use_carryover": True,
    }
    # Then
    message = validate_message_dict(message_dict, "callable_message")
    assert message.type == "method"
    assert message.content == RAG_METHOD_WITH_CARRYOVER

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


def test_rag_message_generator_message() -> None:
    """Test rag_message_generator_message."""
    # Given
    message_dict: Dict[
        Literal["type", "use_carryover", "content", "context"],
        Union[Optional[str], Optional[bool], Optional[Dict[str, Any]]],
    ] = {
        "type": "rag_message_generator",
        "use_carryover": False,
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
    chat = WaldiezChat(
        id="chat_id",
        data=WaldiezChatData(
            name="chat_name",
            description="Chat description",
            source="source",
            target="target",
            message=WaldiezChatMessage(
                type="rag_message_generator",
                use_carryover=False,
                content=None,
                context={
                    "n_results": "5",
                    "problem": "Solve this task",
                },
            ),
            position=0,
            order=0,
            clear_history=False,
            nested_chat=WaldiezChatNested(
                message=None,
                reply=None,
            ),
            max_turns=1,
            silent=False,
            real_source=None,
            real_target=None,
            summary=WaldiezChatSummary(
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
