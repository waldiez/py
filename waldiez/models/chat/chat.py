"""Waldie chat model."""

from typing import Any, Dict, Optional

from pydantic import Field
from typing_extensions import Annotated

from ..agents import WaldieAgent, WaldieRagUser
from ..common import WaldieBase
from .chat_data import WaldieChatData
from .chat_message import WaldieChatMessage
from .chat_nested import WaldieChatNested


class WaldieChat(WaldieBase):
    """Chat class.

    Attributes
    ----------
    id : str
        The chat ID.
    data : WaldieChatData
        The chat data.
        See `waldiez.models.chat.WaldieChatData` for more information.
    name : str
        The chat name.
    source : str
        The chat source.
    target : str
        The chat target.
    nested_chat : WaldieChatNested
        The nested chat message/reply if any.
    message : WaldieChatMessage
        The chat message.
    message_content : Optional[str]
        The chat message content if any. If method, the method's body.

    Functions
    ---------
    get_chat_args()
        Get the chat arguments to use in autogen.
    """

    id: Annotated[
        str,
        Field(
            ...,
            title="ID",
            description="The chat ID.",
        ),
    ]
    data: Annotated[
        WaldieChatData,
        Field(
            ...,
            title="Data",
            description="The chat data.",
        ),
    ]

    @property
    def name(self) -> str:
        """Get the name."""
        return self.data.name

    @property
    def source(self) -> str:
        """Get the source."""
        if self.data.real_source:
            return self.data.real_source
        return self.data.source

    @property
    def target(self) -> str:
        """Get the target."""
        if self.data.real_target:
            return self.data.real_target
        return self.data.target

    @property
    def nested_chat(self) -> WaldieChatNested:
        """Get the nested chat."""
        return self.data.nested_chat

    @property
    def message(self) -> WaldieChatMessage:
        """Get the message."""
        if isinstance(
            self.data.message, str
        ):  # pragma: no cover (just for the lint)
            return WaldieChatMessage(
                type="string", content=self.data.message, context={}
            )
        return self.data.message

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self.data.message_content

    def get_chat_args(
        self,
        sender: Optional[WaldieAgent] = None,
    ) -> Dict[str, Any]:
        """Get the chat arguments to use in autogen.

        Parameters
        ----------
        sender : WaldieAgent
            The sender agent, to check if it's a RAG user.
        Returns
        -------
        dict
            The chat arguments.
        """
        args_dict = self.data.get_chat_args()
        if (
            isinstance(sender, WaldieRagUser)
            and sender.agent_type == "rag_user"
            and self.message.type == "rag_message_generator"
        ):
            # check for n_results in agent data, to add in context
            n_results = sender.data.retrieve_config.n_results
            if isinstance(n_results, int) and n_results > 0:
                args_dict["n_results"] = n_results
        return args_dict
