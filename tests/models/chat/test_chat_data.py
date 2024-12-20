"""Test waldiez.models.chat.chat_data.*."""

# import pytest

from waldiez.models.chat.chat_data import WaldiezChatData
from waldiez.models.chat.chat_message import WaldiezChatMessage


def test_waldiez_chat_data() -> None:
    """Test WaldiezChatData."""
    # Given
    chat_data = WaldiezChatData(
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
            "context": {
                "problem": "Solve this task",
                "solution": "4.2",
                "alternative_solution": "42",
                "not_a_solution": "null",
            },
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
        summary={  # type: ignore
            "method": "reflectionWithLlm",
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
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"
    assert chat_data.message.context == {
        "problem": "Solve this task",
        "solution": "4.2",
        "alternative_solution": "42",
        "not_a_solution": "null",
    }
    assert isinstance(chat_data.nested_chat.message, WaldiezChatMessage)
    assert chat_data.nested_chat.message.type == "string"
    assert chat_data.nested_chat.message.content == "Hi"
    assert isinstance(chat_data.nested_chat.reply, WaldiezChatMessage)
    assert chat_data.nested_chat.reply.type == "string"
    assert chat_data.nested_chat.reply.content == "Hello"
    assert chat_data.summary.method == "reflection_with_llm"
    assert chat_data.summary.prompt == "Summarize this chat"
    assert chat_data.summary.args == {"summary_role": "system"}
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
    assert model_dump["summary"]["method"] == "reflectionWithLlm"


def test_waldiez_chat_data_message() -> None:
    """Test WaldiezChatData message."""
    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
    )
    # Then
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"
    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message=None,  # type: ignore
    )
    # Then
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "none"
    assert chat_data.message.content is None

    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message=42,  # type: ignore
    )
    # Then
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "none"
    assert chat_data.message.content is None

    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message=WaldiezChatMessage(
            type="string",
            use_carryover=False,
            content="Hello there",
            context={},
        ),
    )
    # Then
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == "Hello there"

    # Given
    chat_data_dict = {
        "name": "chat_data",
        "description": "Chat data",
        "source": "wa-1",
        "target": "wa-2",
        "position": 0,
        "clear_history": False,
        "message": {
            "type": "string",
            "content": 4,
            "context": 5,
            "use_carryover": 6,
        },
    }
    # Then
    chat_data = WaldiezChatData(**chat_data_dict)  # type: ignore
    assert isinstance(chat_data.message, WaldiezChatMessage)
    assert chat_data.message.type == "string"
    assert chat_data.message.content == ""
    assert chat_data.message.context == {}
    assert chat_data.message.use_carryover is False


def test_waldiez_chat_summary() -> None:
    """Test WaldiezChatData summary."""
    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
    )
    # Then
    assert chat_data.summary.method == "last_msg"
    assert chat_data.summary_args is None
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summary"]["method"] == "lastMsg"
    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
        summary={  # type: ignore
            "method": "reflectionWithLlm",
        },
    )
    # Then
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summary"]["method"] == "reflectionWithLlm"
    # Given
    chat_data = WaldiezChatData(  # type: ignore
        name="chat_data",
        description="Chat data",
        source="wa-1",
        target="wa-2",
        position=0,
        clear_history=False,
        message="Hello there",
        summary={  # type: ignore
            "method": "reflectionWithLlm",
            "args": {
                "summary_role": "system",
            },
        },
    )
    # Then
    model_dump = chat_data.model_dump(by_alias=True)
    assert model_dump["summary"]["method"] == "reflectionWithLlm"
    model_dump = chat_data.model_dump(by_alias=False)
    assert model_dump["summary"]["method"] == "reflection_with_llm"
