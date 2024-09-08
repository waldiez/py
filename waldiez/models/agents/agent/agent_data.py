"""Common data structures for agents."""

from typing import List, Optional, Union

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Literal

from ...common import WaldieBase
from .code_execution import WaldieAgentCodeExecutionConfig
from .linked_skill import WaldieAgentLinkedSkill
from .nested_chat import WaldieAgentNestedChat
from .teachability import WaldieAgentTeachability
from .termination_message import WaldieAgentTerminationMessage


class WaldieAgentData(WaldieBase):
    """Waldie Agent Data.

    Attributes
    ----------
    system_message : Optional[str]
        The agent's system message. Default: None (depends on the agent's type)
    human_input_mode : Literal["ALWAYS", "NEVER", "TERMINATE"]
        The human input mode to use for the agent.
    code_execution_config : Union[WaldieAgentCodeExecutionConfig, False]
        The code execution config. Either False (no execution) or a dict
    max_tokens : Optional[int]
        The maximum tokens to use. Default: None (no limit).
    agent_default_auto_reply : Optional[str]
        The agent's default auto reply when no input is received.
    max_consecutive_auto_reply : Optional[int]
        The maximum number or consecutive auto replies to use
        before ending the chat. Default: None (no limit).
    termination : WaldieAgentTerminationMessage
        The message termination check to use (keyword, method, none)
    teachability : WaldieAgentTeachability
        The agent teachability configuration.
    model_ids: List[str]
        A list of models (their ids) to link with the agent.
    skills : List[WaldieAgentLinkedSkill]
        A list of skills (id and executor) to register.
    nested_chats : List[WaldieAgentNestedChat]
        A list of nested chats (triggered_by, messages), to register.
    """

    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        populate_by_name=True,
        # we have a field starting with "model_" (model_ids)
        # this is protected by default
        protected_namespaces=(),
    )

    system_message: Annotated[
        Optional[str],
        Field(
            None,
            title="System message",
            description="The agent's system message.",
            alias="systemMessage",
        ),
    ]
    human_input_mode: Annotated[
        Literal["ALWAYS", "NEVER", "TERMINATE"],
        Field(
            "NEVER",
            title="Human input mode",
            description="The human input mode to use for the agent.",
            alias="humanInputMode",
        ),
    ]
    max_tokens: Annotated[
        Optional[int],
        Field(
            None,
            title="Max tokens",
            description="The maximum tokens to use. Default: None (no limit).",
            alias="maxTokens",
        ),
    ]
    code_execution_config: Annotated[
        Union[WaldieAgentCodeExecutionConfig, Literal[False]],
        Field(
            False,
            title="Code execution config",
            description=(
                "The code execution config. Either False (no execution) "
                "or a `WaldieAgentCodeExecutionConfig` with details"
            ),
            alias="codeExecutionConfig",
        ),
    ]
    agent_default_auto_reply: Annotated[
        Optional[str],
        Field(
            None,
            title="Agent's default auto reply",
            description=(
                "The agent's default auto reply when no input is received."
            ),
            alias="agentDefaultAutoReply",
        ),
    ]
    max_consecutive_auto_reply: Annotated[
        Optional[int],
        Field(
            None,
            title="Max consecutive auto reply",
            description=(
                "The maximum number or consecutive auto replies to use "
                "before ending the chat"
            ),
            alias="maxConsecutiveAutoReply",
        ),
    ]
    termination: Annotated[
        WaldieAgentTerminationMessage,
        Field(
            title="Termination",
            description=(
                "The message termination check to use (keyword, method, none)"
            ),
            default_factory=WaldieAgentTerminationMessage,
        ),
    ]
    teachability: Annotated[
        WaldieAgentTeachability,
        Field(
            title="Teachability",
            description="The agent teachability configuration.",
            default_factory=WaldieAgentTeachability,
        ),
    ]
    model_ids: Annotated[
        List[str],
        Field(
            default_factory=list,
            title="Model IDs",
            description="A list of models (their ids) to link with the agent.",
            alias="modelIds",
        ),
    ]
    skills: Annotated[
        List[WaldieAgentLinkedSkill],
        Field(
            default_factory=list,
            title="Skills",
            description=("A list of skills (id and executor) to register."),
        ),
    ]
    nested_chats: Annotated[
        List[WaldieAgentNestedChat],
        Field(
            default_factory=list,
            description=(
                "A list of nested chats (triggered_by, messages), to register."
            ),
            alias="nestedChats",
        ),
    ]
