"""Waldie Message Model."""

from typing import Any, Dict, Optional, Union

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..common import WaldieBase, WaldieMethodName, check_function


class WaldieChatMessage(WaldieBase):
    """
    Waldie Message.

    A generic message with a type and content.

    If the type is not 'none',
    the content is a string.
    If the type is 'method', the content is the source code of a method.

    Attributes
    ----------
    type : Literal["string", "method", "none"]
        The type of the message: string, method, or none.
    content : Optional[str]
        The content of the message (string or method).
    context : Dict[str, Any]
        Extra context of the message.
    """

    type: Annotated[
        Literal["string", "method", "none"],
        Field(
            "none",
            title="Type",
            description="The type of the message: string, method, or none.",
        ),
    ]
    content: Annotated[
        Optional[str],
        Field(
            None,
            title="Content",
            description="The content of the message (string or method).",
        ),
    ]
    context: Annotated[
        Dict[str, Any],
        Field(
            default_factory=dict,
            title="Context",
            description="Extra context of the message.",
        ),
    ]


def validate_message_dict(
    value: Dict[
        Literal["type", "content", "context"],
        Union[Optional[str], Optional[Dict[str, Any]]],
    ],
    function_name: WaldieMethodName,
) -> WaldieChatMessage:
    """Validate a message dict.

    Check the provided message dict.
    Depending on the type, the content is validated.
    If the type is "method", the content is checked against the function name.

    Parameters
    ----------
    value : dict
        The message dict.
    function_name : str (WaldieMethodName)
        The function name.

    Returns
    -------
    WaldieChatMessage
        The validated message.

    Raises
    ------
    ValueError
        If the validation fails.
    """
    message_type = value.get("type")
    content = value.get("content", "")
    if not isinstance(content, str):
        content = ""
    context: Dict[str, Any] = {}
    context_value = value.get("context")
    if isinstance(context_value, dict):
        context = context_value
    if not isinstance(context, dict):  # pragma: no cover
        context = {}
    if message_type == "string":
        if not content:
            raise ValueError(
                "The message content is required for the string type"
            )
        return WaldieChatMessage(
            type="string", content=content, context=context
        )
    if message_type == "none":
        return WaldieChatMessage(type="none", content=None, context=context)
    if message_type == "method":
        if not content:
            raise ValueError(
                "The message content is required for the method type"
            )
        valid, error_or_content = check_function(content, function_name)
        if not valid:
            raise ValueError(error_or_content)
        return WaldieChatMessage(
            type="method", content=error_or_content, context=context
        )
    raise ValueError("Invalid message type")
