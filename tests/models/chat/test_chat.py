"""Test waldiez.models.chat.chat.*."""

from waldiez.models.agents.rag_user import WaldiezRagUser
from waldiez.models.chat.chat import WaldiezChat
from waldiez.models.chat.chat_data import WaldiezChatData
from waldiez.models.chat.chat_nested import WaldiezChatNested


def test_waldiez_chat() -> None:
    """Test WaldiezChat."""
    # Given
    chat = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(  # type: ignore
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
    assert isinstance(chat.nested_chat, WaldiezChatNested)
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
    chat = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(  # type: ignore
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
    chat = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(  # type: ignore
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


def test_waldiez_chat_with_rag_user() -> None:
    """Test WaldiezChat with RAG user as a source."""
    agent = WaldiezRagUser(
        id="wa-1",
        type="agent",
        agent_type="rag_user",
        name="rag_user",
        description="RAG user",
        tags=["rag_user"],
        requirements=[],
        created_at="2021-01-01T00:00:00Z",
        updated_at="2021-01-01T00:00:00Z",
        data={  # type: ignore
            "retrieve_config": {
                "n_results": 5,
            }
        },
    )
    # Given
    chat = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(  # type: ignore
            name="chat_data",
            description="Chat data",
            source="wa-1",
            target="wa-2",
            message={  # type: ignore
                "type": "rag_message_generator",
                "content": None,
                "context": {
                    "problem": "Solve this task",
                },
            },
        ),
    )
    # When
    chat_args = chat.get_chat_args(sender=agent)
    # Then
    assert chat_args["n_results"] == 5
    assert chat_args["problem"] == "Solve this task"
