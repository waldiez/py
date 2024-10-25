"""Waldiez flow data."""

from typing import Any, Dict, List

from pydantic import Field
from typing_extensions import Annotated

from ..agents import WaldiezAgents
from ..chat import WaldiezChat
from ..common import WaldiezBase
from ..model import WaldiezModel
from ..skill import WaldiezSkill


class WaldiezFlowData(WaldiezBase):
    """Flow data class.

    Attributes
    ----------
    nodes : List[Dict[str, Any]]
        The nodes of the flow. We ignore this (UI-related)
    edges : List[Dict[str, Any]]
        The edges of the flow. We ignore this (UI-related)
    viewport : Dict[str, Any]
        The viewport of the flow. We ignore this (UI-related)
    agents : WaldiezAgents
        The agents of the flow:
        users: List[WaldiezUserProxy]
        assistants: List[WaldiezAssistant]
        managers: List[WaldiezGroupManager]
        rag_users : List[WaldiezRagUser]
        See `WaldiezAgents` for more info.
    models : List[WaldiezModel]
        The models of the flow. See `WaldiezModel`.
    skills : List[WaldiezSkill]
        The skills of the flow. See `WaldiezSkill`.
    chats : List[WaldiezChat]
        The chats of the flow. See `WaldiezChat`.
    """

    # the ones below (nodes,edges, viewport) we ignore
    # (they for graph connections, positions, etc.)
    nodes: Annotated[
        List[Dict[str, Any]],
        Field(default_factory=list),
    ]
    edges: Annotated[
        List[Dict[str, Any]],
        Field(default_factory=list),
    ]
    viewport: Annotated[
        Dict[str, Any],
        Field(default_factory=dict),
    ]
    # these are the ones we use.
    agents: Annotated[
        WaldiezAgents,
        Field(
            description="The agents of the flow",
            title="Agents",
            default_factory=WaldiezAgents,
        ),
    ]
    models: Annotated[
        List[WaldiezModel],
        Field(
            description="The models of the flow",
            title="Models",
            default_factory=list,
        ),
    ]
    skills: Annotated[
        List[WaldiezSkill],
        Field(
            description="The skills of the flow",
            title="Skills",
            default_factory=list,
        ),
    ]
    chats: Annotated[
        List[WaldiezChat],
        Field(
            description="The chats of the flow",
            title="Chats",
            default_factory=list,
        ),
    ]
