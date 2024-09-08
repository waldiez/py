"""Test waldiez.exporting.chats.helpers.*."""

from waldiez.exporting.chats.helpers import (
    export_multiple_chats_string,
    export_single_chat_string,
)
from waldiez.models import (
    WaldieAgent,
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
    WaldieChatSummary,
)


def test_export_empty_single_chat_string() -> None:
    """Test export_single_chat_string() with empty chat."""
    # Given
    agent1 = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = WaldieAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="user",
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="chat1",
            description="A chat that does something.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=None,
            silent=None,
            max_turns=None,
            message=WaldieChatMessage(
                type="none",
                content=None,
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    chat_names = {"wc-1": "chat1"}
    agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    # When
    result = export_single_chat_string(
        flow=(chat1, agent1, agent2),
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=0,
    )
    # Then
    expected = """agent1.initiate_chat(
    agent2,
)"""
    assert not result[1]
    assert result[0] == expected


def test_export_single_chat_string() -> None:
    """Test export_single_chat_string()."""
    # Given
    agent1 = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = WaldieAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="user",
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="chat1",
            description="A chat that does something.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=False,
            silent=False,
            max_turns=5,
            message=WaldieChatMessage(
                type="string",
                content="Hello, wa-2!",
            ),
            message_context={
                "problem": "Solve this problem.",
            },
            summary_method="reflection_with_llm",
            llm_summary_method_options=WaldieChatSummary(
                prompt="Summarize the chat.",
                args={"temperature": "0.5", "max_tokens": "100"},
            ),
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    chat_names = {"wc-1": "chat1"}
    agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    # When
    result = export_single_chat_string(
        flow=(chat1, agent1, agent2),
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=0,
    )
    # Then
    expected = """agent1.initiate_chat(
    agent2,
    summary_method="reflection_with_llm",
    summary_args={
        "summary_prompt": "Summarize the chat.",
        "temperature": "0.5",
        "max_tokens": "100"
    },
    max_turns=5,
    clear_history=False,
    silent=False,
    problem="Solve this problem.",
    message="Hello, wa-2!",
)"""
    assert not result[1]
    assert result[0] == expected
    # Given
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="chat2",
            description="A chat that does something else.",
            source="wa-2",
            target="wa-1",
            position=2,
            clear_history=True,
            silent=True,
            max_turns=10,
            message=WaldieChatMessage(
                type="none",
                content=None,
            ),
            message_context={"temperature": "0.5", "max_tokens": "100"},
            summary_method="last_msg",
            llm_summary_method_options=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
        ),
    )
    chat_names = {"wc-2": "chat2"}
    agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    # When
    result = export_single_chat_string(
        flow=(chat2, agent2, agent1),
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=1,
    )
    # Then
    expected = """agent2.initiate_chat(
        agent1,
        summary_method="last_msg",
        max_turns=10,
        clear_history=True,
        silent=True,
        temperature=0.5,
        max_tokens=100,
        message=None,
    )"""
    assert not result[1]
    assert result[0] == expected
    # Given
    chat3 = WaldieChat(
        id="wc-3",
        data=WaldieChatData(
            name="chat3",
            description="A chat that does something else.",
            source="wa-2",
            target="wa-1",
            position=2,
            clear_history=True,
            silent=True,
            max_turns=10,
            message=WaldieChatMessage(
                type="method",
                content=(
                    "def callable_message(sender, recipient, context):\n"
                    "    return 'Hello, wa-1!'"
                ),
            ),
            message_context={"temperature": "0.5", "max_tokens": "100"},
            summary_method="last_msg",
            llm_summary_method_options=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
        ),
    )
    chat_names = {"wc-3": "chat3"}
    agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    # When
    result = export_single_chat_string(
        flow=(chat3, agent2, agent1),
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=1,
    )
    # Then
    # pylint: disable=line-too-long
    expected_callable_message = """def callable_message_chat3(sender, recipient, context):
    # type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]
    return 'Hello, wa-1!'
"""
    expected_chat = """agent2.initiate_chat(
        agent1,
        summary_method="last_msg",
        max_turns=10,
        clear_history=True,
        silent=True,
        temperature=0.5,
        max_tokens=100,
        message=callable_message_chat3,
    )"""
    assert result[1] == expected_callable_message
    assert result[0] == expected_chat


def test_export_multiple_chats_string() -> None:
    """Test export_multiple_chats_string()."""
    # Given
    agent1 = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = WaldieAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="user",
    )
    agent3 = WaldieAgent(  # type: ignore
        id="wa-3",
        name="agent3",
        agent_type="assistant",
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="chat1",
            description="A chat that does something.",
            source="wa-1",
            target="wa-2",
            position=0,
            clear_history=False,
            silent=False,
            max_turns=5,
            message=WaldieChatMessage(
                type="method",
                content=(
                    "def callable_message(sender, recipient, context):\n"
                    "    return 'Hello, wa-2!'"
                ),
            ),
            message_context={
                "problem": "Solve this problem.",
            },
            summary_method="reflection_with_llm",
            llm_summary_method_options=WaldieChatSummary(
                prompt="Summarize the chat.",
                args={"temperature": "0.5", "max_tokens": "100"},
            ),
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="chat2",
            description="A chat that does something else.",
            source="wa-2",
            target="wa-3",
            position=1,
            clear_history=False,
            silent=False,
            max_turns=5,
            message=WaldieChatMessage(
                type="none",
                content=None,
            ),
            message_context={"temperature": "0.5", "max_tokens": "100"},
            summary_method="last_msg",
            llm_summary_method_options=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    chat3 = WaldieChat(
        id="wc-3",
        data=WaldieChatData(
            name="chat3",
            description="A chat that does something else.",
            source="wa-2",
            target="wa-3",
            position=2,
            clear_history=False,
            silent=False,
            max_turns=5,
            message=WaldieChatMessage(
                type="string",
                content="Hello, wa-3!",
            ),
            message_context={},
            summary_method="last_msg",
            llm_summary_method_options=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    chat_names = {"wc-1": "chat1", "wc-2": "chat2", "wc-3": "chat3"}
    agent_names = {"wa-1": "agent1", "wa-2": "agent2", "wa-3": "agent3"}
    # When
    result = export_multiple_chats_string(
        main_chats=[
            (chat1, agent1, agent2),
            (chat2, agent2, agent3),
            (chat3, agent2, agent3),
        ],
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=1,
    )
    # Then
    expected_chats = """initiate_chats([
        {
            "sender": agent1,
            "recipient": agent2,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Summarize the chat.",
                "temperature": "0.5",
                "max_tokens": "100"
            },
            "max_turns": 5,
            "clear_history": False,
            "silent": False,
            "problem": "Solve this problem.",
            "message": callable_message_chat1,
        },
        {
            "sender": agent2,
            "recipient": agent3,
            "summary_method": "last_msg",
            "max_turns": 5,
            "clear_history": False,
            "silent": False,
            "temperature": 0.5,
            "max_tokens": 100,
            "message": None,
        },
        {
            "sender": agent2,
            "recipient": agent3,
            "summary_method": "last_msg",
            "max_turns": 5,
            "clear_history": False,
            "silent": False,
            "message": "Hello, wa-3!",
        },
    ])"""
    expected_callable_message = """
def callable_message_chat1(sender, recipient, context):
    # type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]
    return 'Hello, wa-2!'
"""
    assert result[1] == expected_callable_message
    assert result[0] == expected_chats
