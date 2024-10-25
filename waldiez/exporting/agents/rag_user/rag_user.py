"""RAG User related exporting utils."""

from typing import Dict, List, Set, Tuple, Union

from waldiez.models import (
    WaldiezAgent,
    WaldiezRagUser,
    WaldiezRagUserModels,
    WaldiezRagUserRetrieveConfig,
)

from ...utils import get_object_string, get_path_string
from .vector_db import get_rag_user_vector_db_string


def get_rag_user_retrieve_config_str(
    agent: WaldiezRagUser,
    agent_name: str,
    model_names: Dict[str, str],
) -> Tuple[str, str, Set[str]]:
    """Get the RAG user retrieve config string.

    Parameters
    ----------
    agent : WaldiezRagUser
        The agent.
    agent_name : str
        The agent's name.
    model_names : Dict[str, str]
        A mapping from model id to model name.
    Returns
    -------
    Tuple[str, str, Set[str]]
        The content before the args, the args and the imports.
    """
    # e.g. user_agent = RetrieveUserProxyAgent(
    # ...other common/agent args,
    #  retrieve_config={what_this_returns})
    imports: Set[str] = set()
    retrieve_config = agent.retrieve_config
    before_the_args, vector_db_arg, db_imports = get_rag_user_vector_db_string(
        agent=agent,
        agent_name=agent_name,
    )
    imports.update(db_imports)
    args_dict = _get_args_dict(agent, retrieve_config, model_names)
    if retrieve_config.use_custom_token_count:
        token_count_arg_name = f"custom_token_count_function_{agent_name}"
        before_the_args += (
            f"\ndef {token_count_arg_name}():\n"
            f"{retrieve_config.token_count_function_string}"
            "\n\n"
        )
        args_dict["custom_token_count_function"] = token_count_arg_name
    if retrieve_config.use_custom_text_split:
        text_split_arg_name = f"custom_text_split_function_{agent_name}"
        before_the_args += (
            f"\ndef {text_split_arg_name}():\n"
            f"{retrieve_config.text_split_function_string}"
            "\n\n"
        )
        args_dict["custom_text_split_function"] = text_split_arg_name
    # docs_path = args_dict.pop("docs_path", [])
    args_content = get_object_string(args_dict)
    # get the last line (where the dict ends)
    args_parts = args_content.split("\n")
    before_vector_db = args_parts[:-1]
    closing_arg = args_parts[-1]
    args_content = "\n".join(before_vector_db)
    # add the vector_db arg
    args_content += f',\n        "vector_db": {vector_db_arg},\n'
    args_content += closing_arg
    return before_the_args, args_content, imports


def get_rag_user_extras(
    agent: WaldiezAgent,
    agent_name: str,
    model_names: Dict[str, str],
) -> Tuple[str, str, Set[str]]:
    """Get the RAG user extra argument, imports and content before the agent.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_name : str
        The agent's name.
    model_names : Dict[str, str]
        A mapping from model id to model name.

    Returns
    -------
    Tuple[str, str, Set[str]]
        The content before the agent, the retrieve arg and the db imports.
    """
    before_agent_string = ""
    retrieve_arg = ""
    db_imports: Set[str] = set()
    if agent.agent_type == "rag_user" and isinstance(agent, WaldiezRagUser):
        rag_content_before_agent, retrieve_arg, db_imports = (
            get_rag_user_retrieve_config_str(
                agent=agent, agent_name=agent_name, model_names=model_names
            )
        )
        if retrieve_arg:
            retrieve_arg = f"\n    retrieve_config={retrieve_arg},"
        if rag_content_before_agent:
            before_agent_string += rag_content_before_agent
    return before_agent_string, retrieve_arg, db_imports


def _get_model_arg(
    agent: WaldiezRagUser,
    retrieve_config: WaldiezRagUserRetrieveConfig,
    model_names: Dict[str, str],
) -> str:  # pragma: no cover
    agent_models = agent.data.model_ids
    if agent_models:
        first_model = agent_models[0]
        first_model_name = model_names[first_model]
        new_model_name = f"{first_model_name}"
        return f"{new_model_name}"
    if retrieve_config.model in model_names:
        selected_model = model_names[retrieve_config.model]
        new_model_name = f"{selected_model}"
        return f"{new_model_name}"
    return WaldiezRagUserModels[retrieve_config.vector_db]


def _get_args_dict(
    agent: WaldiezRagUser,
    retrieve_config: WaldiezRagUserRetrieveConfig,
    model_names: Dict[str, str],
) -> Dict[str, Union[str, List[str]]]:
    model_arg = _get_model_arg(agent, retrieve_config, model_names)
    args_dict: Dict[str, Union[str, List[str]]] = {
        "task": retrieve_config.task,
        "model": model_arg,
    }
    optional_args = [
        "chunk_token_size",
        "context_max_tokens",
        "customized_prompt",
        "customized_answer_prefix",
    ]
    for arg in optional_args:
        arg_value = getattr(retrieve_config, arg)
        if arg_value is not None:
            args_dict[arg] = arg_value
            args_dict[arg] = getattr(retrieve_config, arg)
    docs_path: Union[str, List[str]] = []
    if retrieve_config.docs_path:
        docs_path = (
            retrieve_config.docs_path
            if isinstance(retrieve_config.docs_path, list)
            else [retrieve_config.docs_path]
        )
        docs_path = [get_path_string(path) for path in docs_path]
        args_dict["docs_path"] = docs_path
    if docs_path:
        args_dict["docs_path"] = docs_path
    non_optional_args = [
        "new_docs",
        "update_context",
        "get_or_create",
        "overwrite",
        "recursive",
        "chunk_mode",
        "must_break_at_empty_line",
        "collection_name",
        "distance_threshold",
    ]
    for arg in non_optional_args:
        args_dict[arg] = getattr(retrieve_config, arg)
    return args_dict
