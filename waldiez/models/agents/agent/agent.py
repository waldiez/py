"""Base agent class to be inherited by all agents."""

from typing import List

from pydantic import Field
from typing_extensions import Annotated, Literal

from ...common import WaldiezBase, now
from .agent_data import WaldiezAgentData
from .code_execution import WaldiezAgentCodeExecutionConfig

WaldiezAgentType = Literal["user", "assistant", "manager", "rag_user"]


class WaldiezAgent(WaldiezBase):
    """Waldiez Agent.

    Attributes
    ----------
    id : str
        The ID of the agent.
    type : Literal["agent"]
        The type of the "node" in a graph: "agent"
    agent_type : Literal["user", "assistant", "manager", "rag_user"]
        The type of the agent
    name: str
        The name of the agent.
    description : str
        The description of the agent.
    tags : List[str]
        Tags for this agent.
    requirements : List[str]
        Python requirements for the agent.
    created_at : str
        The date and time when the agent was created.
    updated_at : str
        The date and time when the agent was last updated.
    data: WaldiezAgentData
        The data (properties) of this agent.
        See `waldiez.models.agents.WaldiezAgentData` for more info.

    Functions
    ---------
    validate_linked_skills(skill_ids: List[str], agent_ids: List[str])
        Validate the skills linked to the agent.
    validate_linked_models(model_ids: List[str])
        Validate the models linked to the agent.
    """

    id: Annotated[
        str, Field(..., title="ID", description="The agents unique id")
    ]
    type: Annotated[
        Literal["agent"],
        Field(
            "agent",
            title="Type",
            description="The type of the 'node' in a graph.",
        ),
    ]
    agent_type: Annotated[
        Literal["user", "assistant", "manager", "rag_user"],
        Field(
            ...,
            title="Agent type",
            description="The type of the agent: user, assistant, group manager",
        ),
    ]
    name: Annotated[
        str, Field(..., title="Name", description="The name of the agent")
    ]
    description: Annotated[
        str,
        Field(
            "Agent's description",
            title="Description",
            description="The description of the agent",
        ),
    ]
    tags: Annotated[
        List[str],
        Field(
            title="Tags",
            description="Tags of the agent",
            default_factory=list,
        ),
    ]
    requirements: Annotated[
        List[str],
        Field(
            title="Requirements",
            description="Python requirements for the agent",
            default_factory=list,
        ),
    ]
    created_at: Annotated[
        str,
        Field(
            title="Created at",
            description="The date and time when the agent was created",
            default_factory=now,
        ),
    ]
    updated_at: Annotated[
        str,
        Field(
            title="Updated at",
            description="The date and time when the agent was last updated",
            default_factory=now,
        ),
    ]
    data: Annotated[
        WaldiezAgentData,
        Field(
            title="Data",
            description="The data (properties) of the agent",
            default_factory=WaldiezAgentData,
        ),
    ]

    def validate_linked_skills(
        self, skill_ids: List[str], agent_ids: List[str]
    ) -> None:
        """Validate the skills.

        Parameters
        ----------
        skill_ids : List[str]
            The list of skill IDs.
        agent_ids : List[str]
            The list of agent IDs.

        Raises
        ------
        ValueError
            If a skill or agent is not found
        """
        # if the config dict has skills, make sure they can be found
        for skill in self.data.skills:
            if skill.id not in skill_ids:
                raise ValueError(
                    f"Skill '{skill.id}' not found in agent's {self.id} skills"
                )
            if skill.executor_id not in agent_ids:
                raise ValueError(
                    f"Agent '{skill.executor_id}' not found in agents"
                )

    def validate_linked_models(self, model_ids: List[str]) -> None:
        """Validate the models.

        Parameters
        ----------
        model_ids : List[str]
            The list of model IDs.

        Raises
        ------
        ValueError
            If a model is not found
        """
        # if the config dict has models, make sure they can be found
        for model in self.data.model_ids:
            if model not in model_ids:
                raise ValueError(
                    f"Model '{model}' not found in agent's {self.id} models"
                )

    def validate_code_execution(self, skill_ids: List[str]) -> None:
        """Validate the code execution config.

        Parameters
        ----------
        skill_ids : List[str]
            The list of skill IDs.

        Raises
        ------
        ValueError
            If a function is not found
        """
        # if the config dict has functions, make sure they can be found
        if isinstance(
            self.data.code_execution_config, WaldiezAgentCodeExecutionConfig
        ):
            for function in self.data.code_execution_config.functions:
                if function not in skill_ids:
                    raise ValueError(
                        f"Function '{function}' not found in skills"
                    )
