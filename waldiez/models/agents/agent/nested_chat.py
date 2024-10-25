"""Waldiez Agent Nested Chat."""

from typing import List

from pydantic import Field
from typing_extensions import Annotated

from ...common import WaldiezBase


class WaldiezAgentNestedChatMessage(WaldiezBase):
    """Waldiez Agent nested chat message.

    A reference to a chat's message or reply in a nested chat

    Attributes
    ----------
    id : str
        The id of the chat.
    is_reply : bool
        Whether to use the reply in the chat or not.
    """

    id: Annotated[
        str, Field(..., title="ID", description="The id of the chat.")
    ]
    is_reply: Annotated[
        bool,
        Field(
            False,
            title="Is reply",
            description="Whether to use the reply in the chat or not.",
            alias="isReply",
        ),
    ]


class WaldiezAgentNestedChat(WaldiezBase):
    """Waldiez Agent Nested Chat.

    Attributes
    ----------
    triggered_by : List[WaldiezAgentNestedChatMessage]
        A list of chats (id and is_reply) to determine
        the triggering of the nested chat.
    messages : List[WaldiezAgentNestedChatMessage]
        The list of messages (chat ids and 'is_reply'z)
        to include the in the nested chat registration.
    """

    triggered_by: Annotated[
        List[WaldiezAgentNestedChatMessage],
        Field(
            title="Triggered By",
            description=(
                "A list of chats (id and is_reply) to determine"
                "the triggering of the nested chat."
            ),
            alias="triggeredBy",
            default_factory=list,
        ),
    ]
    messages: Annotated[
        List[WaldiezAgentNestedChatMessage],
        Field(
            title="Messages",
            description=(
                "The list of messages (chat ids and 'is_reply'z)"
                "to include the in the nested chat registration."
            ),
            default_factory=list,
        ),
    ]
