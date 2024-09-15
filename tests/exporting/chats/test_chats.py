"""Test waldiez.exporting.chats.chats.*."""

from waldiez.exporting.chats.chats import export_chats
from waldiez.models import (
    WaldieAgent,
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
)


def test_export_chats() -> None:
    """Test export_chats()."""
    # Given
    agent1 = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = WaldieAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="assistant",
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="chat1",
            description="A chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            order=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
        ),
    )
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="chat2",
            description="Another chat.",
            source="wa-2",
            target="wa-1",
            position=1,
            order=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Goodbye, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
        ),
    )
    all_agents = [agent1, agent2]
    agent_names = {agent.id: agent.name for agent in all_agents}
    # When
    all_chats = [chat1]
    chat_names = {chat.id: chat.name for chat in all_chats}
    # Then
    export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        main_chats=[(chat1, agent1, agent2)],
        tabs=1,
    )
    # When
    all_chats = [chat1, chat2]
    chat_names = {chat.id: chat.name for chat in all_chats}
    # Then
    export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        main_chats=[
            (chat1, agent1, agent2),
            (chat2, agent2, agent1),
        ],
        tabs=1,
    )
