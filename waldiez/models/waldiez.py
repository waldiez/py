"""Waldiez data class.

A Waldiez class contains all the information that is needed to generate
and run an autogen workflow. It has the model/LLM configurations, the agent
definitions and their optional additional skills to be used.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

#  let's be strict with autogen version
from autogen.version import __version__ as autogen_version  # type: ignore

from .agents import WaldiezAgent
from .chat import WaldiezChat
from .flow import WaldiezFlow
from .model import WaldiezModel
from .skill import WaldiezSkill


@dataclass(frozen=True, slots=True)
class Waldiez:
    """Waldiez data class.

    It contains all the information to generate and run an autogen workflow.
    """

    flow: WaldiezFlow

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        flow_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        requirements: Optional[List[str]] = None,
    ) -> "Waldiez":
        """Create a Waldiez from dict.

        Parameters
        ----------
        data : Dict[str, Any]
            The data.
        flow_id : Optional[str], optional
            The flow id, by default None (retrieved from data or generated).
        name : Optional[str], optional
            The name, by default None (retrieved from data).
        description : Optional[str], optional
            The description, by default None (retrieved from data).
        tags : Optional[List[str]], optional
            The tags, by default None (retrieved from data).
        requirements : Optional[List[str]], optional
            The requirements, by default None (retrieved from data).

        Returns
        -------
        Waldiez
            The Waldiez.
        """
        flow = _get_flow(
            data,
            flow_id=flow_id,
            name=name,
            description=description,
            tags=tags,
            requirements=requirements,
        )
        return cls(flow=WaldiezFlow.model_validate(flow))

    @classmethod
    def load(
        cls,
        waldiez_file: Union[str, Path],
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        requirements: Optional[List[str]] = None,
    ) -> "Waldiez":
        """Load a Waldiez from a file.

        Parameters
        ----------
        waldiez_file : Union[str, Path]
            The Waldiez file.
        name : Optional[str], optional
            The name, by default None.
        description : Optional[str], optional
            The description, by default None.
        tags : Optional[List[str]], optional
            The tags, by default None.
        requirements : Optional[List[str]], optional
            The requirements, by default None.

        Returns
        -------
        Waldiez
            The Waldiez.

        Raises
        ------
        ValueError
            If the file is not found or invalid JSON.
        """
        data: Dict[str, Any] = {}
        if not Path(waldiez_file).exists():
            raise ValueError(f"File not found: {waldiez_file}")
        with open(waldiez_file, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON: {waldiez_file}") from error
        return cls.from_dict(
            data,
            name=name,
            description=description,
            tags=tags,
            requirements=requirements,
        )

    def model_dump_json(
        self, by_alias: bool = True, indent: Optional[int] = None
    ) -> str:
        """Get the model dump json.

        We use `by_alias=True` by default to use the alias (toCamel).

        Parameters
        ----------
        by_alias : bool, optional
            Use alias (toCamel), by default True.
        indent : Optional[int], optional
            The indent, by default None.

        Returns
        -------
        str
            The model dump json.
        """
        return self.flow.model_dump_json(by_alias=by_alias, indent=indent)

    @property
    def has_rag_agents(self) -> bool:
        """Check if the flow has RAG agents."""
        return any(agent.agent_type == "rag_user" for agent in self.agents)

    @property
    def chats(self) -> List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]]:
        """Get the chats."""
        return self.flow.ordered_flow

    @property
    def agents(self) -> Iterator[WaldiezAgent]:
        """Get the agents.

        Yields
        -------
        WaldiezAgent
            The flow agents.
        """
        yield from self.flow.data.agents.members

    @property
    def skills(self) -> Iterator[WaldiezSkill]:
        """Get the flow skills.

        Yields
        -------
        WaldiezSkill
            The skills.
        """
        yield from self.flow.data.skills

    @property
    def models(self) -> Iterator[WaldiezModel]:
        """Get the models.

        Yields
        -------
        WaldiezModel
            The flow models.
        """
        yield from self.flow.data.models

    @property
    def name(self) -> str:
        """Get the flow name."""
        return self.flow.name or "Waldiez Flow"

    @property
    def description(self) -> str:
        """Get the flow description."""
        return self.flow.description or "Waldiez Flow description"

    @property
    def tags(self) -> List[str]:
        """Get the flow tags."""
        return self.flow.tags

    @property
    def requirements(self) -> List[str]:
        """Get the flow requirements."""
        requirements_list = filter(
            lambda requirement: not (
                requirement.startswith("pyautogen")
                or requirement.startswith("autogen-agentchat")
            ),
            self.flow.requirements,
        )
        requirements = set(requirements_list)
        if self.has_rag_agents:
            requirements.add(
                f"autogen-agentchat[retrievechat]=={autogen_version}"
            )
        else:
            requirements.add(f"autogen-agentchat=={autogen_version}")
        # ref: https://github.com/microsoft/autogen/blob/main/setup.py
        models_with_additional_requirements = [
            "together",
            "gemini",
            "mistral",
            "groq",
            "anthropic",
            "cohere",
            "bedrock",
        ]
        for model in self.models:
            if model.data.api_type in models_with_additional_requirements:
                requirements.add(
                    f"autogen-agentchat[{model.data.api_type}]=="
                    f"{autogen_version}"
                )
        return list(requirements)

    def get_flow_env_vars(self) -> List[Tuple[str, str]]:
        """Get the flow environment variables.

        Returns
        -------
        List[Tuple[str, str]]
            The environment variables for the flow.
        """
        env_vars: List[Tuple[str, str]] = []
        for skill in self.skills:
            for secret_key, secret_value in skill.secrets.items():
                env_vars.append((secret_key, secret_value))
        return env_vars

    def get_group_chat_members(self, agent: WaldiezAgent) -> List[WaldiezAgent]:
        """Get the chat members that connect to a group chat manger agent.

        Parameters
        ----------
        agent : WaldiezAgent
            The agent (group chat manager).

        Returns
        -------
        List[WaldiezAgent]
            The group chat members.
        """
        if agent.agent_type != "manager":
            return []
        return self.flow.get_group_chat_members(agent.id)


def _get_flow(
    data: Dict[str, Any],
    flow_id: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    requirements: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Get the flow."""
    item_type = data.get("type", "flow")
    if item_type != "flow":
        # empty flow (from exported model/skill ?)
        raise ValueError(f"Invalid flow type: {item_type}")
    from_args = {
        "id": flow_id,
        "name": name,
        "description": description,
        "tags": tags,
        "requirements": requirements,
    }
    for key, value in from_args.items():
        if value:
            data[key] = value
    if "name" not in data:
        data["name"] = "Waldiez Flow"
    if "description" not in data:
        data["description"] = "Waldiez Flow description"
    if "tags" not in data:
        data["tags"] = []
    if "requirements" not in data:
        data["requirements"] = []
    return data
