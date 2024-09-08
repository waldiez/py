"""Waldie flow data."""

from typing import Any, Dict, List

from pydantic import Field
from typing_extensions import Annotated

from ..agents import WaldieAgents
from ..chat import WaldieChat
from ..common import WaldieBase
from ..model import WaldieModel
from ..skill import WaldieSkill


class WaldieFlowData(WaldieBase):
    """Flow data class.

    Attributes
    ----------
    nodes : List[Dict[str, Any]]
        The nodes of the flow. We ignore this (UI-related)
    edges : List[Dict[str, Any]]
        The edges of the flow. We ignore this (UI-related)
    viewport : Dict[str, Any]
        The viewport of the flow. We ignore this (UI-related)
    agents : WaldieAgents
        The agents of the flow:
        users: List[WaldieUserProxy]
        assistants: List[WaldieAssistant]
        managers: List[WaldieGroupManager]
        rag_users : List[WaldieRagUser]
        See `WaldieAgents` for more info.
    models : List[WaldieModel]
        The models of the flow. See `WaldieModel`.
    skills : List[WaldieSkill]
        The skills of the flow. See `WaldieSkill`.
    chats : List[WaldieChat]
        The chats of the flow. See `WaldieChat`.
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
        WaldieAgents,
        Field(
            description="The agents of the flow",
            title="Agents",
            default_factory=list,
        ),
    ]
    models: Annotated[
        List[WaldieModel],
        Field(
            description="The models of the flow",
            title="Models",
            default_factory=list,
        ),
    ]
    skills: Annotated[
        List[WaldieSkill],
        Field(
            description="The skills of the flow",
            title="Skills",
            default_factory=list,
        ),
    ]
    chats: Annotated[
        List[WaldieChat],
        Field(
            description="The chats of the flow",
            title="Chats",
            default_factory=list,
        ),
    ]
