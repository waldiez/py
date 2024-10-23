"""Get an agent's llm config argument."""

from typing import Dict, List, Tuple

from waldiez.models import WaldiezAgent, WaldiezModel

from ..models import export_agent_models


def get_agent_llm_config(
    agent: WaldiezAgent,
    agent_name: str,
    all_models: List[WaldiezModel],
    model_names: Dict[str, str],
) -> Tuple[str, str]:
    """Get the llm config argument string for one agent.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_name : str
        The name of the agent.
    all_models : List[WaldiezModel]
        All the models in the flow.
    model_names : Dict[str, str]
        A mapping of model id to model name.

    Returns
    -------
    Tuple[str, str]
        The llm config argument string and extra content
        to use before the argument (the variable definition if needed).
    """
    content_before = ""
    if not agent.data.model_ids:
        # no models
        return "False", content_before
    if len(agent.data.model_ids) == 1:
        # one model
        model_id = agent.data.model_ids[0]
        model_name = model_names[model_id]
        return f"{model_name}_llm_config", content_before
    arg = f"{agent_name}_llm_config"
    content_before = "\n" + (
        export_agent_models(
            agent_model_ids=agent.data.model_ids,
            all_models=all_models,
            agent_name=agent_name,
        )
        + "\n"
    )
    return arg, content_before
