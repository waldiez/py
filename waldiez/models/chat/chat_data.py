"""Chat data model."""

from typing import Any, Dict, Optional, Union

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Self

from ..common import WaldiezBase
from .chat_message import WaldiezChatMessage, validate_message_dict
from .chat_nested import WaldiezChatNested
from .chat_summary import WaldiezChatSummary


class WaldiezChatData(WaldiezBase):
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
    message : Union[str, WaldiezChatMessage]
        The message of the chat.
    nested_chat : WaldiezChatNested
        The nested chat config.
    summary : WaldiezChatSummary
        The summary method and options for the chat.
    max_turns : Optional[int]
        The maximum number of turns for the chat, by default None (no limit).
    silent : Optional[bool], optional
        Whether to run the chat silently, by default None (ignored).
    summary_args : Optional[Dict[str, Any]]
        The summary args to use in autogen.
    real_source : Optional[str]
        The real source of the chat (overrides the source).
    real_target : Optional[str]
        The real target of the chat (overrides the target).

    Functions
    ---------
    validate_message(value: Any)
        Validate the message.
    validate_summary_method(value: Optional[WaldiezChatSummaryMethod])
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
        Union[str, WaldiezChatMessage],
        Field(
            title="Message",
            description="The message of the chat.",
            default_factory=WaldiezChatMessage,
        ),
    ]
    nested_chat: Annotated[
        WaldiezChatNested,
        Field(
            title="Nested Chat",
            description="The nested chat.",
            alias="nestedChat",
            default_factory=WaldiezChatNested,
        ),
    ]
    summary: Annotated[
        WaldiezChatSummary,
        Field(
            default_factory=WaldiezChatSummary,
            title="Summary",
            description="The summary method options for the chat.",
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
    real_source: Annotated[
        Optional[str],
        Field(
            None,
            alias="realSource",
            title="Real Source",
            description="The real source of the chat (overrides the source).",
        ),
    ]
    real_target: Annotated[
        Optional[str],
        Field(
            None,
            alias="realTarget",
            title="Real Target",
            description="The real target of the chat (overrides the target).",
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
        WaldiezChatData
            The validated chat data.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if isinstance(self.message, WaldiezChatMessage):
            if self.message.type == "none":
                self._message_content = None
            elif self.message.type == "string":
                self._message_content = self.message.content
            else:
                self._message_content = validate_message_dict(
                    value={
                        "type": self.message.type,
                        "content": self.message.content,
                        "use_carryover": self.message.use_carryover,
                    },
                    function_name="callable_message",
                    skip_definition=True,
                ).content
        return self

    @field_validator("message", mode="before")
    @classmethod
    def validate_message(cls, value: Any) -> WaldiezChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The message value.

        Returns
        -------
        WaldiezChatMessage
            The validated message value.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if value is None:
            return WaldiezChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        if isinstance(value, str):
            return WaldiezChatMessage(
                type="string", use_carryover=False, content=value, context={}
            )
        if isinstance(value, dict):
            return validate_message_dict(
                value, function_name="callable_message"
            )
        if isinstance(value, WaldiezChatMessage):
            return validate_message_dict(
                value={
                    "type": value.type,
                    "use_carryover": value.use_carryover,
                    "content": value.content,
                    "context": value.context,
                },
                function_name="callable_message",
            )
        return WaldiezChatMessage(
            type="none", use_carryover=False, content=None, context={}
        )

    @property
    def summary_args(self) -> Optional[Dict[str, Any]]:
        """Get the summary args."""
        if self.summary.method not in (
            "reflection_with_llm",
            "reflectionWithLlm",
        ):
            return None
        args: Dict[str, Any] = {}
        if self.summary.prompt:
            args["summary_prompt"] = self.summary.prompt
        if self.summary.args:
            args.update(self.summary.args)
        return args

    def _get_context_args(self) -> Dict[str, Any]:
        """Get the context arguments to use in autogen.

        Returns
        -------
        Dict[str, Any]
            The dictionary to use for generating the kwargs.
        """
        extra_args: Dict[str, Any] = {}
        if isinstance(self.message, WaldiezChatMessage):
            for key, value in self.message.context.items():
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
        if self.summary.method:
            args["summary_method"] = self.summary.method
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
