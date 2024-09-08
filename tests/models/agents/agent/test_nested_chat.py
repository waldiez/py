"""Test waldiez.models.agents.agent.nested_chat.*."""

from waldiez.models.agents.agent.nested_chat import (
    WaldieAgentNestedChat,
    WaldieAgentNestedChatMessage,
)


def test_waldie_agent_nested_chat_message() -> None:
    """Test WaldieAgentNestedChatMessage."""
    message = WaldieAgentNestedChatMessage(
        id="message_id",
        is_reply=False,
    )
    assert message.id == "message_id"
    assert not message.is_reply


def test_waldie_agent_nested_chat() -> None:
    """Test WaldieAgentNestedChat."""
    nested_chat = WaldieAgentNestedChat(
        triggered_by=[WaldieAgentNestedChatMessage(id="wc-1", is_reply=False)],
        messages=[WaldieAgentNestedChatMessage(id="wc-2", is_reply=True)],
    )
    assert nested_chat.triggered_by[0].id == "wc-1"
    assert not nested_chat.triggered_by[0].is_reply
    assert nested_chat.messages[0].id == "wc-2"
    assert nested_chat.messages[0].is_reply
