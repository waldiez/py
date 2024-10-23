"""Export the entire flow to string."""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from waldiez.models import (
    Waldiez,
    WaldiezAgent,
    WaldiezChat,
    WaldiezModel,
    WaldiezSkill,
)

from ..agents import export_agent
from ..chats import export_chats, export_nested_chat
from ..models import export_models
from ..skills import export_skills
from ..utils import (
    get_comment,
    get_imports_string,
    get_logging_start_string,
    get_logging_stop_string,
    get_pylint_ignore_comment,
    get_sqlite_to_csv_call_string,
    get_sqlite_to_csv_string,
)
from .def_main import get_def_main


# pylint: disable=too-many-locals
def export_flow(
    waldiez: Waldiez,
    agents: Tuple[List[WaldiezAgent], Dict[str, str]],
    chats: Tuple[List[WaldiezChat], Dict[str, str]],
    models: Tuple[List[WaldiezModel], Dict[str, str]],
    skills: Tuple[List[WaldiezSkill], Dict[str, str]],
    output_dir: Optional[Path],
    notebook: bool,
) -> str:
    """Export the entire flow to a string.

    It contains the required imports, the model and skill definitions,
    the agent definitions, the links between agents, models and skills,
    the agents' nested chats, the chat definitions, and the actual call
    to start the chat(s).

    Parameters
    ----------
    waldiez : Waldiez
        The Waldiez instance.
    agents : Tuple[List[WaldiezAgent], Dict[str, str]]
        The agents and their names.
    chats : Tuple[List[WaldiezChat], Dict[str, str]]
        The chats and their names.
    models : Tuple[List[WaldiezModel], Dict[str, str]]
        The models and their names.
    skills : Tuple[List[WaldiezSkill], Dict[str, str]]
        The skills and their names.
    output_dir : Optional[Path]
        The output directory.
    notebook : bool
        Whether the export is for a jupyter notebook or a python script.

    Returns
    -------
    str
        The flow string.
    """
    all_agents, agent_names = agents
    all_models, model_names = models
    all_skills, skill_names = skills
    all_chats, chat_names = chats
    agent_strings = ""
    # we need to add `skipped_agent_strings` after the other agents are defined
    # for example, a group_manager needs the group members to have been defined
    skipped_agent_strings = ""
    nested_chats_strings = ""
    builtin_imports: Set[str] = {
        "import csv",
        "import os",
        "import sqlite3",
    }
    other_imports: Set[str] = {
        "from autogen import Agent",
        "from autogen import ConversableAgent",
        "from autogen import ChatResult",
        "from autogen import runtime_logging",
    }
    skill_imports, _ = export_skills(
        skills=all_skills,
        skill_names=skill_names,
        output_dir=output_dir,
    )
    if len(waldiez.chats) > 1:
        other_imports.add("from autogen import initiate_chats")
    for agent in all_agents:
        agent_string, after_agent, agent_imports = export_agent(
            agent=agent,
            agent_names=agent_names,
            model_names=model_names,
            skill_names=skill_names,
            all_models=all_models,
            all_skills=all_skills,
            group_chat_members=waldiez.flow.get_group_chat_members(agent.id),
        )
        other_imports.update(agent_imports)
        if after_agent:
            skipped_agent_strings += after_agent
        if agent.agent_type == "manager":
            skipped_agent_strings += agent_string
        else:
            agent_strings += agent_string
        agent_nested_chats_string = export_nested_chat(
            agent=agent,
            agent_names=agent_names,
            all_chats=all_chats,
            chat_names=chat_names,
        )
        if agent_nested_chats_string:
            nested_chats_strings += "\n" + agent_nested_chats_string
    agent_strings += skipped_agent_strings
    models_string = export_models(
        all_models=all_models,
        model_names=model_names,
        notebook=notebook,
    )
    all_imports_string = get_imports_string(
        imports=other_imports,
        builtin_imports=builtin_imports,
        skill_imports=skill_imports,
    )
    return _combine_strings(
        waldiez=waldiez,
        imports_string=all_imports_string,
        agents_string=agent_strings,
        nested_chats_string=nested_chats_strings,
        models_string=models_string,
        agent_names=agent_names,
        chat_names=chat_names,
        notebook=notebook,
    )


# pylint: disable=too-many-arguments
def _combine_strings(
    waldiez: Waldiez,
    imports_string: str,
    agents_string: str,
    nested_chats_string: str,
    models_string: str,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    notebook: bool,
) -> str:
    content = get_pylint_ignore_comment(notebook)
    content += imports_string
    # content += get_comment("logging", notebook) + "\n"
    # content += get_logging_start_string(tabs=0) + "\n\n"
    content += models_string
    content += get_comment("agents", notebook) + "\n"
    content += agents_string
    if nested_chats_string:
        content += get_comment("nested", notebook) + "\n"
    content += nested_chats_string
    chats_content, additional_methods = export_chats(
        main_chats=waldiez.chats,
        agent_names=agent_names,
        chat_names=chat_names,
        tabs=0 if notebook else 1,
    )
    if additional_methods:
        while not content.endswith("\n\n"):  # pragma: no cover
            content += "\n"
        content += "\n" + additional_methods + "\n"
    content += get_sqlite_to_csv_string()
    content += get_comment("run", notebook) + "\n"
    if not notebook:
        content += get_def_main(chats_content)
    else:
        content += get_logging_start_string(tabs=0)
        content += "\n" + chats_content + "\n"
        content += get_logging_stop_string(tabs=0) + "\n"
        content += get_sqlite_to_csv_call_string(tabs=0) + "\n"
    content = content.replace("\n\n\n\n", "\n\n\n")
    return content
