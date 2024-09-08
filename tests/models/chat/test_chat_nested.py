"""Test waldiez.models.chat.chat_nested.*."""

import pytest

from waldiez.models.chat.chat_message import WaldieChatMessage
from waldiez.models.chat.chat_nested import WaldieChatNested


def test_waldie_chat_nested() -> None:
    """Test WaldieChatNested."""
    # Given
    reply = WaldieChatMessage(
        type="string",
        content="Hi",
    )
    # When
    chat_nested = WaldieChatNested(
        message="Hello there",  # type: ignore
        reply=reply,
    )
    # Then
    assert isinstance(chat_nested.message, WaldieChatMessage)
    assert chat_nested.message.content == "Hello there"
    assert isinstance(chat_nested.reply, WaldieChatMessage)
    assert chat_nested.reply.type == "string"
    assert chat_nested.reply.content == "Hi"

    # Given
    reply = None  # type: ignore
    message_content = """
def nested_chat_message(recipient, messages, sender, config):
    return "Hello there"
"""
    message = WaldieChatMessage(
        type="method",
        content=message_content,
    )
    # When
    chat_nested = WaldieChatNested(
        message=message,
        reply=reply,
    )
    # Then
    assert isinstance(chat_nested.message, WaldieChatMessage)
    assert chat_nested.message.type == "method"
    assert chat_nested.message.content == (
        "    # type: (ConversableAgent, list[dict], ConversableAgent, dict) ->"
        ' Union[dict, str]\n    return "Hello there"'
    )
    assert isinstance(chat_nested.reply, WaldieChatMessage)
    assert chat_nested.reply.type == "none"
    assert chat_nested.reply.content is None

    # Given
    message_content = "Hello there"
    reply_content = """
def nested_chat_reply(recipient, messages, sender, config):
    return "Hi"
"""
    # When
    chat_nested = WaldieChatNested(
        message={  # type: ignore
            "type": "string",
            "content": message_content,
        },
        reply={  # type: ignore
            "type": "method",
            "content": reply_content,
        },
    )
    # Then
    assert isinstance(chat_nested.message, WaldieChatMessage)
    assert chat_nested.message.type == "string"
    assert chat_nested.message.content == "Hello there"
    assert isinstance(chat_nested.reply, WaldieChatMessage)
    assert chat_nested.reply.type == "method"
    assert chat_nested.reply.content == (
        "    # type: (ConversableAgent, list[dict], ConversableAgent, dict) ->"
        ' Union[dict, str]\n    return "Hi"'
    )

    with pytest.raises(ValueError):
        chat_nested = WaldieChatNested(
            message=WaldieChatMessage(
                type="string",
                content="Hello there",
            ),
            reply=45,  # type: ignore
        )
