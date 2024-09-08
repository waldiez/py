"""Get an agent's llm config argument."""

from typing import Dict

from waldiez.models import WaldieAgent


def get_agent_llm_config(
    agent: WaldieAgent,
    model_names: Dict[str, str],
) -> str:
    """Get the llm config argument string for one agent.

    Parameters
    ----------
    agent : WaldieAgent
        The agent.
    model_names : Dict[str, str]
        A mapping of model id to model name.

    Returns
    -------
    str
        The llm config argument string.
    """
    if not agent.data.model_ids:
        # no models
        return "False"
    if len(agent.data.model_ids) == 1:
        # one model
        model_id = agent.data.model_ids[0]
        model_name = model_names[model_id]
        return model_name
    output = '{\n    "config_list": [\n'
    for model_id in agent.data.model_ids:
        model_name = model_names[model_id]
        output += f"        {model_name},\n"
    output += "    ]\n" "}"
    return output
