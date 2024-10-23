"""Agent skills related string generation functions."""

from typing import Dict, List

from waldiez.models import WaldiezAgent, WaldiezSkill

from ..utils import get_escaped_string


def get_agent_skill_registrations(
    agent: WaldiezAgent,
    agent_names: Dict[str, str],
    all_skills: List[WaldiezSkill],
    skill_names: Dict[str, str],
) -> str:
    """Get the agent skill registrations.

    example output:

    ```python
    >>> register_function(
        {skill_name},
        caller={agent_name},
        executor={executor_agent_name},
        name="{skill_name}",
        description="{skill_description}",
    )
    ```

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    all_skills : List[WaldiezSkill]
        All the skills in the flow.
    skill_names : Dict[str, str]
        A mapping of skill id to skill name.

    Returns
    -------
    str
        The agent skill registrations.
    """
    if not agent.data.skills or not all_skills:
        return ""
    content = ""
    for linked_skill in agent.data.skills:
        skill_name = skill_names[linked_skill.id]
        waldiez_skill = next(
            skill for skill in all_skills if skill.id == linked_skill.id
        )
        skill_description = (
            waldiez_skill.description or f"Description of {skill_name}"
        )
        skill_description = get_escaped_string(skill_description)
        content += (
            f"register_function(\n"
            f"    {skill_name},\n"
            f"    caller={agent_names[agent.id]},\n"
            f"    executor={agent_names[linked_skill.executor_id]},\n"
            f'    name="{skill_name}",\n'
            f'    description="{skill_description}",\n'
            f")\n\n"
        )
    return content
