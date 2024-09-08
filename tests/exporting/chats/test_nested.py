"""Test waldiez.exporting.chats.nested.*."""

# pylint: disable=line-too-long

from waldiez.exporting.chats.nested import (
    export_nested_chat,
    get_chat_nested_string,
)
from waldiez.models import (
    WaldieAgent,
    WaldieAgentNestedChat,
    WaldieAgentNestedChatMessage,
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
)


def test_get_chat_nested_string() -> None:
    """Test get_chat_nested_string()."""
    # Given
    chat = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="nested_chat",
            description="A nested chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=WaldieChatMessage(
                    type="string",
                    content="Hi",
                ),
            ),
        ),
    )
    chat_names = {
        "wc-1": "nested_chat",
    }
    # When
    result = get_chat_nested_string(
        chat=chat,
        is_reply=True,
        chat_names=chat_names,
    )
    # Then
    expected = ("Hi", None)
    assert result == expected
    # When
    result = get_chat_nested_string(
        chat=chat,
        is_reply=False,
        chat_names=chat_names,
    )
    # Then
    expected = ("None", None)
    assert result == expected


def test_export_nested_chat() -> None:
    """Test export_nested_chat()."""
    # Given
    agent1 = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
        data={  # type: ignore
            "nested_chats": [
                WaldieAgentNestedChat(
                    triggered_by=[
                        WaldieAgentNestedChatMessage(
                            id="wc-1",
                            is_reply=True,
                        ),
                    ],
                    messages=[
                        WaldieAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=False,
                        ),
                        WaldieAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=True,
                        ),
                    ],
                )
            ]
        },
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="nested_chat1",
            description="A nested chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message="Hello from agent1 to agent2!",  # type: ignore
                reply="Hello from agent2 to agent1!",  # type: ignore
            ),
        ),
    )
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="nested_chat2",
            description="Another nested chat.",
            source="wa-2",
            target="wa-3",
            position=2,
            clear_history=True,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message={  # type: ignore
                    "type": "string",
                    "content": "Hello from agent2 to agent3!",
                },
                reply={  # type: ignore
                    "type": "string",
                    "content": "Hello from agent3 to agent2!",
                },
            ),
        ),
    )
    agent_names = {
        "wa-1": "agent1",
        "wa-2": "agent2",
        "wa-3": "agent3",
    }
    chat_names = {
        "wc-1": "nested_chat1",
        "wc-2": "nested_chat2",
    }
    # When
    result = export_nested_chat(
        agent=agent1,
        all_chats=[chat1, chat2],
        agent_names=agent_names,
        chat_names=chat_names,
    )

    # Then
    expected = """
agent1_chat_queue = [
    {
        "clear_history": True,
        "silent": False,
        "recipient": agent3,
        "sender": agent2,
        "message": "Hello from agent2 to agent3!"
    },
    {
        "clear_history": True,
        "silent": False,
        "recipient": agent2,
        "sender": agent3,
        "message": "Hello from agent3 to agent2!"
    },
]


agent1.register_nested_chats(
    trigger=["agent2"],
    chat_queue=agent1_chat_queue,
)

"""
    assert result == expected

    # Given
    agent2 = WaldieAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="assistant",
        data={  # type: ignore
            "nested_chats": [
                WaldieAgentNestedChat(
                    triggered_by=[
                        WaldieAgentNestedChatMessage(
                            id="wc-1",
                            is_reply=False,
                        ),
                    ],
                    messages=[
                        WaldieAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=False,
                        ),
                        WaldieAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=True,
                        ),
                    ],
                )
            ]
        },
    )
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="nested_chat1",
            description="A nested chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="method",
                    content=(
                        "def nested_chat_message(recipient, messages, sender, config):\n"
                        '    return "Hello from agent1 to agent2!"'
                    ),
                ),
                reply=WaldieChatMessage(
                    type="method",
                    content=(
                        "def nested_chat_reply(recipient, messages, sender, config):\n"
                        '    return "Hello from agent2 to agent1!"'
                    ),
                ),
            ),
        ),
    )
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="nested_chat2",
            description="Another nested chat.",
            source="wa-2",
            target="wa-3",
            position=2,
            clear_history=True,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="method",
                    content=(
                        "def nested_chat_message(recipient, messages, sender, config):\n"
                        '    return "Hello from agent2 to agent3!"'
                    ),
                ),
                reply=WaldieChatMessage(
                    type="method",
                    content=(
                        "def nested_chat_reply(recipient, messages, sender, config):\n"
                        '    return "Hello from agent3 to agent2!"'
                    ),
                ),
            ),
        ),
    )
    agent_names = {
        "wa-1": "agent1",
        "wa-2": "agent2",
        "wa-3": "agent3",
    }
    chat_names = {
        "wc-1": "nested_chat1",
        "wc-2": "nested_chat2",
    }
    # When
    result = export_nested_chat(
        agent=agent2,
        all_chats=[chat1, chat2],
        agent_names=agent_names,
        chat_names=chat_names,
    )
    # Then
    expected = """
def nested_chat_message_nested_chat2(recipient, messages, sender, config):
    # type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]
    return "Hello from agent2 to agent3!"


def nested_chat_reply_nested_chat2(recipient, messages, sender, config):
    # type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]
    return "Hello from agent3 to agent2!"


agent2_chat_queue = [
    {
        "clear_history": True,
        "silent": False,
        "recipient": agent3,
        "message": nested_chat_message_nested_chat2
    },
    {
        "clear_history": True,
        "silent": False,
        "recipient": agent2,
        "sender": agent3,
        "message": nested_chat_reply_nested_chat2
    },
]


agent2.register_nested_chats(
    trigger=["agent1"],
    chat_queue=agent2_chat_queue,
)

"""
    assert result == expected

    # Given
    agent3 = WaldieAgent(  # type: ignore
        id="wa-3",
        name="agent3",
        agent_type="assistant",
        data={  # type: ignore
            "nested_chats": [
                WaldieAgentNestedChat(
                    triggered_by=[
                        WaldieAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=False,
                        ),
                    ],
                    messages=[],
                )
            ]
        },
    )
    # pylint: disable=line-too-long
    chat1 = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="nested_chat1",
            description="A nested chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            clear_history=False,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
        ),
    )
    chat2 = WaldieChat(
        id="wc-2",
        data=WaldieChatData(
            name="nested_chat2",
            description="Another nested chat.",
            source="wa-2",
            target="wa-3",
            position=2,
            clear_history=True,
            message=WaldieChatMessage(
                type="string",
                content="Hello, world!",
            ),
            message_context={},
            summary_method=None,
            llm_summary_method_options=None,
            silent=False,
            max_turns=None,
            nested_chat=WaldieChatNested(
                message=WaldieChatMessage(
                    type="none",
                    content=None,
                ),
                reply=None,
            ),
        ),
    )
    agent_names = {
        "wa-1": "agent1",
        "wa-2": "agent2",
        "wa-3": "agent3",
    }
    chat_names = {
        "wc-1": "nested_chat1",
        "wc-2": "nested_chat2",
    }
    # When
    result = export_nested_chat(
        agent=agent3,
        all_chats=[chat1, chat2],
        agent_names=agent_names,
        chat_names=chat_names,
    )
    # Then
    expected = """
agent3_chat_queue = []


agent3.register_nested_chats(
    trigger=["agent2"],
    chat_queue=agent3_chat_queue,
)
"""
    # Given
    agent4 = WaldieAgent(  # type: ignore
        id="wa-4",
        name="agent4",
        agent_type="assistant",
        data={  # type: ignore
            "nested_chats": [],
        },
    )
    # When
    result = export_nested_chat(
        agent=agent4,
        all_chats=[],
        agent_names={},
        chat_names={},
    )
    # Then
    expected = ""
    assert result == expected
