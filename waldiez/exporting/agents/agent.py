"""Agent strings generation.."""

from typing import Dict, List, Set, Tuple

from waldiez.models import WaldiezAgent, WaldiezModel, WaldiezSkill

from ..utils import get_escaped_string
from .agent_skills import get_agent_skill_registrations
from .code_execution import get_agent_code_execution_config
from .group_manager import get_group_manager_extras
from .llm_config import get_agent_llm_config
from .rag_user import get_rag_user_extras
from .termination_message import get_is_termination_message


def get_agent_class_name(agent: WaldiezAgent) -> str:
    """Get the agent class name.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.

    Returns
    -------
    str
        The agent class name.
    """
    if agent.agent_type == "assistant":
        return "AssistantAgent"
    if agent.agent_type == "user":
        return "UserProxyAgent"
    if agent.agent_type == "manager":
        return "GroupChatManager"
    if agent.agent_type == "rag_user":
        return "RetrieveUserProxyAgent"
    return "ConversableAgent"  # pragma: no cover


def get_agent_imports(agent_class: str) -> Set[str]:
    """Get the imports needed for the agent.

    Parameters
    ----------
    agent_class : str
        The agent class name.

    Returns
    -------
    Set[str]
        The imports needed for the agent.
    """
    imports = set()
    if agent_class == "AssistantAgent":
        imports.add("from autogen import AssistantAgent")
    elif agent_class == "UserProxyAgent":
        imports.add("from autogen import UserProxyAgent")
    elif agent_class == "GroupChatManager":
        imports.add("from autogen import GroupChatManager")
        imports.add("from autogen import GroupChat")
    elif agent_class == "RetrieveUserProxyAgent":
        imports.add(
            "from autogen.agentchat.contrib.retrieve_user_proxy_agent "
            "import RetrieveUserProxyAgent"
        )
    return imports


def get_system_message_arg(agent: WaldiezAgent) -> str:
    """Get the system message argument.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.

    Returns
    -------
    str
        The system message argument.
    """
    if not agent.data.system_message:
        return ""
    return (
        "\n    "
        f'system_message="{get_escaped_string(agent.data.system_message)}",'
    )


# pylint: disable=too-many-locals, unused-argument
def export_agent(
    agent: WaldiezAgent,
    agent_names: Dict[str, str],
    model_names: Dict[str, str],
    skill_names: Dict[str, str],
    all_models: List[WaldiezModel],
    all_skills: List[WaldiezSkill],
    group_chat_members: List[WaldiezAgent],
) -> Tuple[str, str, Set[str]]:
    """Export the agent to a string.

    If the agent's `is_termination_msg` is a method,
    the function definition and content will be included in the string.
    So it could be like:
    ```python
    ...
    def is_termination_message_{agent_name}(message):
        return ....
    ...
    agent_name = AssistantAgent(
        ...
        is_termination_msg=is_termination_message_{agent_name},
        ...
    )
    ```
    The same goes for any additional `before the agent` contents in the cases
    of a group chat manager (define the `GroupChat` first),
    a retrieve user proxy agent (define the retrieve/db config first),
    or the agent's `code_execution`: define the
    `DockerCommandLineCodeExecutor`/`LocalCommandLineCodeExecutor` first.

    The agent's `skill_registrations` and/or nested chats if any,
    should be added to the final string after all the agents are defined.
    definition. Example:
    ```python
        ...
        agent_name = AssistantAgent(
            ...
        )
        ...
        register_function(
            {skill_name},
            caller={caller_name},
            executor={executor_name},
        )
        ...
    ```

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    model_names : Dict[str, str]
        A mapping of model id to model name.
    skill_names : Dict[str, str]
        A mapping of skill id to skill name.
    all_models : List[WaldiezModel]
        All the models in the flow.
    all_skills : List[WaldiezSkill]
        All the skills in the flow.
    group_chat_members : List[WaldiezAgent]
        The group chat members.

    Returns
    -------
    Tuple[str, str, Set[str], Set[str]]
        A tuple containing:
        - The string representation of the agent (w additional content before),
        - Extra content to be added after the agents are defined.
        - Needed imports (autogen.x, db/RAG or code execution related) if any.
    """
    imports: Set[str] = set()
    agent_name = agent_names[agent.id]
    before_agent_string = ""
    after_agent_string = ""
    before_manager, group_chat_arg = get_group_manager_extras(
        agent, group_chat_members, agent_names
    )
    if before_manager:
        before_agent_string += before_manager
    before_rag, retrieve_arg, rag_imports = get_rag_user_extras(
        agent, agent_name, model_names
    )
    if before_rag:
        before_agent_string += before_rag
    imports.update(rag_imports)
    is_termination_message, termination_function = get_is_termination_message(
        agent, agent_name
    )
    if termination_function:
        before_agent_string += termination_function
    executor, config_arg, coding_import = get_agent_code_execution_config(
        agent=agent, agent_name=agent_name, skill_names=skill_names
    )
    if executor:
        before_agent_string += executor
    if coding_import:
        imports.add(f"from autogen.coding import {coding_import}")
    agent_class = get_agent_class_name(agent)
    imports.update(get_agent_imports(agent_class))
    if agent.data.skills:
        imports.add("from autogen import register_function")
    default_auto_reply: str = "None"
    if agent.data.agent_default_auto_reply:
        default_auto_reply = (
            f'"{get_escaped_string(agent.data.agent_default_auto_reply)}"'
        )
    agent_llm_config_arg, llm_config_string = get_agent_llm_config(
        agent=agent,
        agent_name=agent_name,
        all_models=all_models,
        model_names=model_names,
    )
    before_agent_string += llm_config_string
    agent_str = f"""{agent_name} = {agent_class}(
    name="{agent_name}",
    description="{agent.description}",
    llm_config={agent_llm_config_arg},{(get_system_message_arg(agent))}
    human_input_mode="{agent.data.human_input_mode}",
    max_consecutive_auto_reply={agent.data.max_consecutive_auto_reply},
    default_auto_reply={default_auto_reply},
    code_execution_config={config_arg},
    is_termination_msg={is_termination_message},{group_chat_arg}{retrieve_arg}
)
"""
    agent_skill_registrations = get_agent_skill_registrations(
        agent, agent_names, all_skills, skill_names
    )
    if before_agent_string:
        agent_str = before_agent_string + "\n" + agent_str
    if agent_skill_registrations:
        after_agent_string = "\n" + agent_skill_registrations + "\n"
    return (
        agent_str,
        after_agent_string,
        imports,
    )
