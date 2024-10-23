"""Nested chat model."""

from typing import Any, Optional

from pydantic import (
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Self

from ..common import WaldiezBase, WaldiezMethodName
from .chat_message import WaldiezChatMessage, validate_message_dict


class WaldiezChatNested(WaldiezBase):
    """Nested chat class.

    Attributes
    ----------
    message : WaldiezChatMessage
        The message in a nested chat (sender -> recipient).
    reply : WaldiezChatMessage
        The reply in a nested chat (recipient -> sender).
    """

    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        populate_by_name=True,
        frozen=False,
    )

    message: Annotated[
        Optional[WaldiezChatMessage],
        Field(
            None,
            title="Message",
            description="The message in a nested chat (sender -> recipient).",
        ),
    ]
    reply: Annotated[
        Optional[WaldiezChatMessage],
        Field(
            None,
            title="Reply",
            description="The reply in a nested chat (recipient -> sender).",
        ),
    ]

    _message_content: Optional[str] = None
    _reply_content: Optional[str] = None

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self._message_content

    @property
    def reply_content(self) -> Optional[str]:
        """Get the reply content."""
        return self._reply_content

    @field_validator("message", "reply", mode="before")
    @classmethod
    def validate_message(
        cls, value: Any, info: ValidationInfo
    ) -> WaldiezChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The value.
        info : ValidationInfo
            The validation info.

        Returns
        -------
        WaldiezChatMessage
            The validated message.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        function_name: WaldiezMethodName = (
            "nested_chat_message"
            if info.field_name == "message"
            else "nested_chat_reply"
        )
        if not value:
            return WaldiezChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        if isinstance(value, str):
            return WaldiezChatMessage(
                type="string", use_carryover=False, content=value, context={}
            )
        if isinstance(value, dict):
            return validate_message_dict(value, function_name=function_name)
        if isinstance(value, WaldiezChatMessage):
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

    @model_validator(mode="after")
    def validate_nested_chat(self) -> Self:
        """Validate the nested chat.

        Returns
        -------
        WaldiezChatNested
            The validated nested chat.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.message is not None:
            if self.message.type == "none":
                self._message_content = ""
            elif self.message.type == "string":
                self._message_content = self.message.content
            else:
                self._message_content = validate_message_dict(
                    value={
                        "type": "method",
                        "content": self.message.content,
                    },
                    function_name="nested_chat_message",
                    skip_definition=True,
                ).content
        if self.reply is not None:
            if self.reply.type == "none":
                self._reply_content = ""
            elif self.reply.type == "string":
                self._reply_content = self.reply.content
            else:
                self._reply_content = validate_message_dict(
                    value={
                        "type": "method",
                        "content": self.reply.content,
                    },
                    function_name="nested_chat_reply",
                    skip_definition=True,
                ).content
        return self
