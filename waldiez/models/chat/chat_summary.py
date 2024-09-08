"""Waldie chat summary options."""

from typing import Dict

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..common import WaldieBase

WaldieChatSummaryMethod = Literal[
    "reflectionWithLlm",
    "lastMsg",
    "reflection_with_llm",
    "last_msg",
]


class WaldieChatSummary(WaldieBase):
    """Llm summary method options.

    Attributes
    ----------
    prompt : str
        The prompt for the LLM summary method.
    args : Optional[Dict[str, Any]]
        The additional arguments for the LLM summary method, by default None.
    """

    prompt: str
    args: Annotated[
        Dict[str, str],
        Field(
            title="Arguments",
            description="The additional arguments for the LLM summary method.",
            default_factory=dict,
        ),
    ]
