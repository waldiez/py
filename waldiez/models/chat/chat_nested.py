"""Nested chat model."""

from typing import Any, Optional

from pydantic import Field, ValidationInfo, field_validator
from typing_extensions import Annotated

from ..common import WaldieBase, WaldieMethodName
from .chat_message import WaldieChatMessage, validate_message_dict


class WaldieChatNested(WaldieBase):
    """Nested chat class.

    Attributes
    ----------
    message : WaldieChatMessage
        The message in a nested chat (sender -> recipient).
    reply : WaldieChatMessage
        The reply in a nested chat (recipient -> sender).
    """

    message: Annotated[
        Optional[WaldieChatMessage],
        Field(
            None,
            title="Message",
            description="The message in a nested chat (sender -> recipient).",
        ),
    ]
    reply: Annotated[
        Optional[WaldieChatMessage],
        Field(
            None,
            title="Reply",
            description="The reply in a nested chat (recipient -> sender).",
        ),
    ]

    @field_validator("message", "reply", mode="before")
    @classmethod
    def validate_message(
        cls, value: Any, info: ValidationInfo
    ) -> WaldieChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The value.
        info : ValidationInfo
            The validation info.

        Returns
        -------
        WaldieChatMessage
            The validated message.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        function_name: WaldieMethodName = (
            "nested_chat_message"
            if info.field_name == "message"
            else "nested_chat_reply"
        )
        if not value:
            return WaldieChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        if isinstance(value, str):
            return WaldieChatMessage(
                type="string", use_carryover=False, content=value, context={}
            )
        if isinstance(value, dict):
            return validate_message_dict(value, function_name=function_name)
        if isinstance(value, WaldieChatMessage):
            return validate_message_dict(
                {
                    "type": value.type,
                    "use_carryover": False,
                    "content": value.content,
                    "context": value.context,
                },
                function_name=function_name,
            )
        raise ValueError(f"Invalid message type: {type(value)}")
