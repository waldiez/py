"""Test waldiez.models.chat.chat.*."""

from waldiez.models.chat.chat import WaldieChat
from waldiez.models.chat.chat_data import WaldieChatData
from waldiez.models.chat.chat_nested import WaldieChatNested


def test_waldie_chat() -> None:
    """Test WaldieChat."""
    # Given
    chat = WaldieChat(
        id="wc-1",
        data=WaldieChatData(  # type: ignore
            name="chat_data",
            description="Chat data",
            source="wa-1",
            target="wa-2",
            position=0,
            clear_history=False,
            max_turns=1,
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
        ),
    )
    # Then
    assert chat.id == "wc-1"
    assert chat.name == "chat_data"
    assert chat.source == "wa-1"
    assert chat.target == "wa-2"
    assert chat.message.type == "string"
    assert chat.message.content == "Hello there"
    assert isinstance(chat.nested_chat, WaldieChatNested)
    assert chat.nested_chat.message is None
    assert chat.nested_chat.reply is None
    chat_args = chat.get_chat_args()
    assert chat_args == {
        "clear_history": False,
        "max_turns": 1,
        "summary_method": "last_msg",
        "problem": "Solve this task",
        "solution": 4.2,
        "alternative_solution": 42,
        "not_a_solution": None,
    }

    # Given
    chat = WaldieChat(
        id="wc-1",
        data=WaldieChatData(  # type: ignore
            name="chat_data",
            description="Chat data",
            source="wa-1",
            target="wa-2",
            real_source="wa-3",
            real_target=None,
        ),
    )
    # Then
    assert chat.id == "wc-1"
    assert chat.data.source == "wa-1"
    assert chat.source == "wa-3"
    assert chat.target == "wa-2"

    # Given
    chat = WaldieChat(
        id="wc-1",
        data=WaldieChatData(  # type: ignore
            name="chat_data",
            description="Chat data",
            source="wa-1",
            target="wa-2",
            real_source=None,
            real_target="wa-4",
        ),
    )
    # Then
    assert chat.id == "wc-1"
    assert chat.data.source == "wa-1"
    assert chat.source == "wa-1"
    assert chat.target == "wa-4"
    assert chat.data.target == "wa-2"
    assert chat.data.real_target == "wa-4"
