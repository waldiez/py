"""Chat data model."""

from typing import Any, Dict, Optional, Union

from pydantic import (
    ConfigDict,
    Field,
    FieldSerializationInfo,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Self

from ..common import WaldieBase
from .chat_message import WaldieChatMessage, validate_message_dict
from .chat_nested import WaldieChatNested
from .chat_summary import WaldieChatSummary, WaldieChatSummaryMethod


class WaldieChatData(WaldieBase):
    """Chat data class.

    Attributes
    ----------
    name : str
        The name of the chat.
    source : str
        The source of the chat (sender).
    target : str
        The target of the chat (recipient).
    description : str
        The description of the chat.
    position : int
        The position of the chat. Ignored (UI related).
    order : int
        The of the chat. If negative, ignored.
    clear_history : Optional[bool], optional
        Whether to clear the chat history, by default None.
    message : Union[str, WaldieChatMessage]
        The message of the chat.
    message_context: Dict[str, str]
        Additional context to be sent with the message.
    nested_chat : WaldieChatNested
        The nested chat config.
    summary_method : Optional[WaldieChatSummaryMethod], optional
        The summary method for the chat, by default None.
    llm_summary_method_options : Optional[WaldieChatSummary]
        The LLM summary method options for the chat.
        Only used if the summary method is `reflection_with_llm`
    max_turns : Optional[int]
        The maximum number of turns for the chat, by default None (no limit).
    silent : Optional[bool], optional
        Whether to run the chat silently, by default None (ignored).
    summary_args : Optional[Dict[str, Any]]
        The summary args to use in autogen.

    Functions
    ---------
    validate_message(value: Any)
        Validate the message.
    validate_summary_method(value: Optional[WaldieChatSummaryMethod])
        Validate the summary method.
    serialize_summary_method(value: Any, info: FieldSerializationInfo)
        Serialize summary method.
    get_chat_args()
        Get the chat arguments to use in autogen.
    """

    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        populate_by_name=True,
        frozen=False,
    )

    name: Annotated[
        str, Field(..., title="Name", description="The name of the chat.")
    ]
    source: Annotated[
        str,
        Field(
            ...,
            title="Source",
            description="The source of the chat (sender).",
        ),
    ]
    target: Annotated[
        str,
        Field(
            ...,
            title="Target",
            description="The target of the chat (recipient).",
        ),
    ]
    description: Annotated[
        str,
        Field(
            ...,
            title="Description",
            description="The description of the chat.",
        ),
    ]
    position: Annotated[
        int,
        Field(
            -1,
            title="Position",
            description="The position of the chat in the flow (Ignored).",
        ),
    ]
    order: Annotated[
        int,
        Field(
            -1,
            title="Order",
            description="The order of the chat in the flow.",
        ),
    ]
    clear_history: Annotated[
        Optional[bool],
        Field(
            None,
            alias="clearHistory",
            title="Clear History",
            description="Whether to clear the chat history.",
        ),
    ]
    message: Annotated[
        Union[str, WaldieChatMessage],
        Field(
            title="Message",
            description="The message of the chat.",
            default_factory=WaldieChatMessage,
        ),
    ]
    message_context: Annotated[
        Dict[str, Any],
        Field(
            alias="messageContext",
            title="Message context",
            description="Additional context to be sent with the message.",
            default_factory=dict,
        ),
    ]
    nested_chat: Annotated[
        WaldieChatNested,
        Field(
            title="Nested Chat",
            description="The nested chat.",
            alias="nestedChat",
            default_factory=WaldieChatNested,
        ),
    ]
    summary_method: Annotated[
        Optional[WaldieChatSummaryMethod],
        Field(
            None,
            alias="summaryMethod",
            title="Summary Method",
            description="The summary method for the chat.",
        ),
    ]
    llm_summary_method_options: Annotated[
        Optional[WaldieChatSummary],
        Field(
            None,
            alias="llmSummaryMethodOptions",
            title="LLM Summary Method Options",
            description="The LLM summary method options for the chat.",
        ),
    ]
    max_turns: Annotated[
        Optional[int],
        Field(
            None,
            alias="maxTurns",
            title="Max Turns",
            description="The maximum number of turns for the chat.",
        ),
    ]
    silent: Annotated[
        Optional[bool],
        Field(
            None,
            title="Silent",
            description="Whether to run the chat silently.",
        ),
    ]

    _message_content: Optional[str] = None

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self._message_content

    @model_validator(mode="after")
    def validate_chat_data(self) -> Self:
        """Validate the chat data.

        Returns
        -------
        WaldieChatData
            The validated chat data.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if isinstance(self.message, WaldieChatMessage):
            if self.message.type == "none":
                self._message_content = None
            elif self.message.type == "string":
                self._message_content = self.message.content
            else:
                self._message_content = validate_message_dict(
                    value={
                        "type": self.message.type,
                        "content": self.message.content,
                    },
                    function_name="callable_message",
                ).content
        return self

    @field_validator("message", mode="before")
    @classmethod
    def validate_message(cls, value: Any) -> WaldieChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The message value.

        Returns
        -------
        WaldieChatMessage
            The validated message value.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if not value:
            return WaldieChatMessage(type="none", content=None)
        if isinstance(value, str):
            return WaldieChatMessage(type="string", content=value)
        if isinstance(value, dict):
            message = validate_message_dict(
                value, function_name="callable_message"
            )
            return WaldieChatMessage(
                type=message.type, content=value.get("content")
            )
        if isinstance(value, WaldieChatMessage):
            message = validate_message_dict(
                value={
                    "type": value.type,
                    "content": value.content,
                },
                function_name="callable_message",
            )
            return WaldieChatMessage(type=message.type, content=value.content)
        return WaldieChatMessage(type="none", content=None)

    @field_validator("summary_method", mode="before")
    @classmethod
    def validate_summary_method(
        cls, value: Optional[WaldieChatSummaryMethod]
    ) -> Optional[WaldieChatSummaryMethod]:
        """Validate the summary method.

        Parameters
        ----------
        value : Optional[WaldieChatSummaryMethod]
            The passed WaldieChatSummaryMethod

        Returns
        -------
        Optional[WaldieChatSummaryMethod]
            The validated message summary method
        """
        if str(value).lower() == "none":
            return None
        if value == "lastMsg":
            return "last_msg"
        if value == "reflectionWithLlm":
            return "reflection_with_llm"
        return value

    @field_serializer("summary_method")
    @classmethod
    def serialize_summary_method(
        cls, value: Any, info: FieldSerializationInfo
    ) -> Any:
        """Serialize summary method.

        Parameters
        ----------
        value : Any
            The value to serialize.
        info : FieldSerializationInfo
            The serialization info.

        Returns
        -------
        Any
            The serialized value.
        """
        if info.by_alias is True:
            if value == "reflection_with_llm":
                return "reflectionWithLlm"
            if value == "last_msg":
                return "lastMsg"
        return value

    @property
    def summary_args(self) -> Optional[Dict[str, Any]]:
        """Get the summary args."""
        if self.summary_method not in (
            "reflection_with_llm",
            "reflectionWithLlm",
        ):
            return None
        args: Dict[str, Any] = {}
        if self.llm_summary_method_options:
            summary_prompt = self.llm_summary_method_options.prompt
            if summary_prompt:
                args["summary_prompt"] = summary_prompt
            other_args = self.llm_summary_method_options.args
            if other_args:
                args.update(other_args)
        return args

    def _get_context_args(self) -> Dict[str, Any]:
        """Get the context arguments to use in autogen.

        Returns
        -------
        Dict[str, Any]
            The dictionary to use for generating the kwargs.
        """
        extra_args: Dict[str, Any] = {}
        for key, value in self.message_context.items():
            if str(value).lower() in ("none", "null"):
                extra_args[key] = None
            elif str(value).isdigit():
                extra_args[key] = int(value)
            elif str(value).replace(".", "").isdigit():
                try:
                    extra_args[key] = float(value)
                except ValueError:  # pragma: no cover
                    extra_args[key] = value
            else:
                extra_args[key] = value
        return extra_args

    def get_chat_args(self) -> Dict[str, Any]:
        """Get the chat arguments to use in autogen.

        Returns
        -------
        Dict[str, Any]
            The dictionary to pass as kwargs.
        """
        args: Dict[str, Any] = {}
        if self.summary_method:
            args["summary_method"] = self.summary_method
        if self.summary_args:
            args["summary_args"] = self.summary_args
        if isinstance(self.max_turns, int) and self.max_turns > 0:
            args["max_turns"] = self.max_turns
        if isinstance(self.clear_history, bool):
            args["clear_history"] = self.clear_history
        if isinstance(self.silent, bool):
            args["silent"] = self.silent
        args.update(self._get_context_args())
        return args
