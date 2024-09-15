"""Test waldiez.models.chat.chat_data.*."""

# import pytest

from waldiez.models.chat.chat_data import WaldieChatData
from waldiez.models.chat.chat_message import WaldieChatMessage


def test_waldie_chat_data() -> None:
    """Test WaldieChatData."""
    # Given
    chat_data = WaldieChatData(
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=-1,
        order=1,
        clear_history=False,
        message={  # type: ignore
            "type": "string",
            "content": "Hello there",
        },
        message_context={
            "problem": "Solve this task",
            "solution": "4.2",
            "alternative_solution": "42",
            "not_a_solution": "null",
        },
        nested_chat={  # type: ignore
            "message": {
                "type": "string",
                "content": "Hi",
            },
            "reply": {
                "type": "string",
                "content": "Hello",
            },
        },
        summary_method="reflectionWithLlm",
        llm_summary_method_options={  # type: ignore
            "prompt": "Summarize this chat",
            "args": {
                "summary_role": "system",
            },
        },
        max_turns=5,
        silent=False,
    )

    # Then
    assert chat_data.name == "chat_data"
    assert chat_data.description == "Chat data"
    assert chat_data.source == "wa-1"
    assert chat_data.target == "wa-2"
    assert chat_data.position == -1
    assert chat_data.order == 1
    assert not chat_data.clear_history
    assert isinstance(chat_data.message, WaldieChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"
    assert chat_data.message_context == {
        "problem": "Solve this task",
        "solution": "4.2",
        "alternative_solution": "42",
        "not_a_solution": "null",
    }
    assert isinstance(chat_data.nested_chat.message, WaldieChatMessage)
    assert chat_data.nested_chat.message.type == "string"
    assert chat_data.nested_chat.message.content == "Hi"
    assert isinstance(chat_data.nested_chat.reply, WaldieChatMessage)
    assert chat_data.nested_chat.reply.type == "string"
    assert chat_data.nested_chat.reply.content == "Hello"
    assert chat_data.summary_method == "reflection_with_llm"
    assert chat_data.llm_summary_method_options
    assert chat_data.llm_summary_method_options.prompt == "Summarize this chat"
    assert chat_data.llm_summary_method_options.args == {
        "summary_role": "system"
    }
    assert chat_data.max_turns == 5
    assert not chat_data.silent
    assert chat_data.summary_args == {
        "summary_prompt": "Summarize this chat",
        "summary_role": "system",
    }
    chat_args = chat_data.get_chat_args()
    assert chat_args["problem"] == "Solve this task"
    assert chat_args["solution"] == 4.2
    assert chat_args["alternative_solution"] == 42
    assert chat_args["not_a_solution"] is None

    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summaryMethod"] == "reflectionWithLlm"


def test_waldie_chat_data_message() -> None:
    """Test WaldieChatData message."""
    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
    )
    # Then
    assert isinstance(chat_data.message, WaldieChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"
    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="",
        summary_method=None,
    )
    # Then
    assert isinstance(chat_data.message, WaldieChatMessage)
    assert chat_data.message.type == "none"
    assert chat_data.message.content is None

    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message=42,  # type: ignore
        summary_method="lastMsg",
    )
    # Then
    assert isinstance(chat_data.message, WaldieChatMessage)
    assert chat_data.message.type == "none"
    assert chat_data.message.content is None

    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message=WaldieChatMessage(
            type="string",
            content="Hello there",
        ),
    )
    # Then
    assert isinstance(chat_data.message, WaldieChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"


def test_waldie_chat_summary() -> None:
    """Test WaldieChatData summary."""
    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
        summary_method="lastMsg",
    )
    # Then
    assert chat_data.summary_method == "last_msg"
    assert chat_data.summary_args is None
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summaryMethod"] == "lastMsg"
    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
        summary_method="reflectionWithLlm",
    )
    # Then
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summaryMethod"] == "reflectionWithLlm"
    # Given
    chat_data = WaldieChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
        summary_method="reflection_with_llm",
    )
    # Then
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summaryMethod"] == "reflectionWithLlm"
    model_dump = chat_data.model_dump(by_alias=False)
    assert model_dump["summary_method"] == "reflection_with_llm"
