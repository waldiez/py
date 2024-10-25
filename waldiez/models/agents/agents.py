"""Waldiez agents model."""

from typing import Iterator, List

from pydantic import Field, model_validator
from typing_extensions import Annotated, Self

from ..common import WaldiezBase
from .agent import WaldiezAgent
from .assistant import WaldiezAssistant
from .group_manager.group_manager import WaldiezGroupManager
from .rag_user import WaldiezRagUser
from .user_proxy import WaldiezUserProxy


class WaldiezAgents(WaldiezBase):
    """Waldiez agents model.

    Attributes
    ----------
    users : List[WaldiezUserProxy]
        User proxy agents.
    assistants : List[WaldiezAssistant]
        Assistant agents.
    managers : List[WaldiezGroupManager]
        Group chat mangers.
    rag_users : List[WaldiezRagUser]
        RAG user agents.
    """

    users: Annotated[
        List[WaldiezUserProxy],
        Field(
            title="Users.",
            description="User proxy agents",
            default_factory=list,
        ),
    ]
    assistants: Annotated[
        List[WaldiezAssistant],
        Field(
            title="Assistants.",
            description="Assistant agents",
            default_factory=list,
        ),
    ]
    managers: Annotated[
        List[WaldiezGroupManager],
        Field(
            title="Managers.",
            description="Group chat mangers",
            default_factory=list,
        ),
    ]
    rag_users: Annotated[
        List[WaldiezRagUser],
        Field(
            title="RAG Users.",
            description="RAG user agents",
            default_factory=list,
        ),
    ]

    @property
    def members(self) -> Iterator[WaldiezAgent]:
        """Get all agents.

        Yields
        ------
        WaldiezAgent
            The agents.
        """
        yield from self.users
        yield from self.assistants
        yield from self.managers
        yield from self.rag_users

    @model_validator(mode="after")
    def validate_agents(self) -> Self:
        """Validate the agents.

        - At least two agents are required.
        - All the agent IDs must be unique.

        Returns
        -------
        WaldiezAgents
            The agents.

        Raises
        ------
        ValueError
            If the agents are invalid.
        """
        all_agent_ids = [agent.id for agent in self.members]
        if len(all_agent_ids) < 2:
            raise ValueError("At least two agents are required.")
        if len(all_agent_ids) != len(set(all_agent_ids)):
            raise ValueError("Agent IDs must be unique.")
        return self

    def validate_flow(self, model_ids: List[str], skill_ids: List[str]) -> None:
        """Validate the flow of the agents.

        - Validate the linked models (the referenced model ids must exist).
        - Validate the linked skills (the referenced skill ids must exist).
        - Validate the code execution (the referenced functions must exist).

        Parameters
        ----------
        model_ids : List[str]
            The list of model IDs.
        skill_ids : List[str]
            The list of skill IDs.

        Raises
        ------
        ValueError
            If the flow is invalid.
        """
        all_agent_ids = [agent.id for agent in self.members]
        for agent in self.members:
            agent.validate_linked_models(model_ids)
            agent.validate_linked_skills(skill_ids, agent_ids=all_agent_ids)
            agent.validate_code_execution(skill_ids=skill_ids)
            if agent.agent_type == "manager" and isinstance(
                agent, WaldiezGroupManager
            ):
                agent.validate_transitions(agent_ids=all_agent_ids)
