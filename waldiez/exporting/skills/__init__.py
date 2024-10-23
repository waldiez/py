"""Skills/tools related string generation functions.

Functions
---------
get_agent_skill_registration
    Get an agent's skill registration string.
export_skills
    Get the skills content and secrets.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from waldiez.models import WaldiezSkill

from ..utils import get_escaped_string


def get_agent_skill_registration(
    caller_name: str,
    executor_name: str,
    skill_name: str,
    skill_description: str,
) -> str:
    """Get the agent skill string and secrets.

    Parameters
    ----------
    caller_name : str
        The name of the caller (agent).
    executor_name : str
        The name of the executor (agent).
    skill_name : str
        The name of the skill.
    skill_description : str
        The skill description.

    Returns
    -------
    str
        The agent skill string.

    Example
    -------
    ```python
    >>> get_agent_skill_registration(
    ...     caller_name="agent1",
    ...     executor_name="agent2",
    ...     skill_name="skill1",
    ...     skill_description="A skill that does something.",
    ... )
    register_function(
        skill1,
        caller=agent1,
        executor=agent2,
        name="skill1",
        description="A skill that does something.",
    )
    ```
    """
    skill_description = get_escaped_string(skill_description)
    content = f"""register_function(
    {skill_name},
    caller={caller_name},
    executor={executor_name},
    name="{skill_name}",
    description="{skill_description}",
)"""
    return content


def export_skills(
    skills: List[WaldiezSkill],
    skill_names: Dict[str, str],
    output_dir: Optional[Union[str, Path]] = None,
) -> Tuple[Set[str], Set[Tuple[str, str]]]:
    """Get the skills' contents and secrets.

    If `output_dir` is provided, the contents are saved to that directory.

    Parameters
    ----------
    skills : List[WaldiezSkill]
        The skills.
    skill_names : Dict[str, str]
        The skill names.
    output_dir : Optional[Union[str, Path]]
        The output directory to save the skills to.

    Returns
    -------
    Tuple[Set[str], Set[Tuple[str, str]]]
        - The skill imports to use in the main file.
        - The skill secrets to set as environment variables.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezSkill, WaldiezSkillData
    >>> skill1 = WaldiezSkill(
    ...     id="ws-1",
    ...     name="skill1",
    ...     description="A skill that does something.",
    ...     tags=["skill", "skill1"],
    ...     requirements=[],
    ...     data=WaldiezSkillData(
    ...         content="def skill1():\\n    pass",
    ...         secrets={"API_KEY": "1234567890"},
    ... )
    >>> skill_names = {"ws-1": "skill1"}
    >>> export_skills([skill1], skill_names, None)
    ({'from skill1 import skill1'}, {('API_KEY', '1234567890')})
    ```
    """
    skill_imports: Set[str] = set()
    skill_secrets: Set[Tuple[str, str]] = set()
    for skill in skills:
        skill_name = skill_names[skill.id]
        skill_imports.add(f"from {skill_name} import {skill_name}")
        skill_secrets.update(skill.secrets.items())
        if not output_dir:
            continue
        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
        skill_file = output_dir / f"{skill_name}.py"
        with skill_file.open("w", encoding="utf-8") as f:
            f.write(skill.content)
    return skill_imports, skill_secrets
