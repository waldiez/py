"""Model/LLM related string generation functions.

Functions
---------
export_models
    Get the string representations of the LLM configs.
"""

from typing import Dict, List

from waldiez.models import WaldiezModel

from ..utils import get_comment, get_object_string


def export_models(
    all_models: List[WaldiezModel],
    model_names: Dict[str, str],
    notebook: bool,
) -> str:
    """Get the string representations of the LLM configs.

    Parameters
    ----------
    all_models : List[WaldiezModel]
        The models.
    model_names : Dict[str, str]
        A mapping of model ids to model names.
    notebook : bool
        Whether to export the string for a jupyter notebook.

    Returns
    -------
    str
        The string representation of the models.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezModel, WaldiezModelData
    >>> model = WaldiezModel(
    ...     id="wm-1",
    ...     name="llama3.1"  ,
    ...     description="A model for llamas :P.",
    ...     tags=["llama", "llama3.1"],
    ...     requirements=[],
    ...     data=WaldiezModelData(
    ...         base_url="https://example.com/v1",
    ...         api_key="1234567890",
    ...         api_type="openai",
    ...         temperature=0.5,
    ...         price={
    ...             "prompt_price_per_1k": 0.0001,
    ...             "completion_token_price_per_1k": 0.0002,
    ...         },
    ...     ),
    ... )
    >>> model_names = {"wm-1": "llama3_1"}
    >>> export_models([model], model_names, True)

    # # Models
    llama3_1_llm_config = {
        "config_list": [{
            "model": "llama3.1",
            "base_url": "https://example.com/v1",
            "api_key": "1234567890",
            "api_type": "openai",
            "temperature": 0.5,
            "price": [0.0001, 0.0002],
        }]
    }
    ```
    """
    content = get_comment("models", notebook) + "\n"
    if len(all_models) == 1:
        only_model = all_models[0]
        model_name = model_names[only_model.id]
        llm_config = only_model.get_llm_config()
        model_dict_str = get_object_string(llm_config, tabs=2)
        content += f"{model_name}_llm_config = " + "{\n"
        content += '    "config_list": [\n'
        content += f"        {model_dict_str}\n"
        content += "    ]\n"
        content += "}\n"
    else:
        for model in all_models:
            model_name = model_names[model.id]
            llm_config = model.get_llm_config()
            model_dict_str = get_object_string(llm_config, tabs=2)
            content += f"{model_name}_llm_config = " + "{\n"
            content += '    "config_list": [\n'
            content += f"        {model_dict_str}\n"
            content += "    ]\n"
            content += "}\n"
    return content


def export_agent_models(
    agent_model_ids: List[str],
    all_models: List[WaldiezModel],
    agent_name: str,
) -> str:
    """Get the string representations of the agent's registered models.

    Parameters
    ----------
    agent_model_ids : List[str]
        The model ids registered to the agent.
    all_models : List[WaldiezModel]
        All the models in the flow.
    agent_name : str
        The name of the agent.

    Returns
    -------
    str
        The agent's llm config string.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezModel, WaldiezModelData
    >>> model1 = WaldiezModel(
    ...     id="wm-1",
    ...     name="llama3.1"  ,
    ...     description="A model for llamas :P.",
    ...     tags=["llama", "llama3.1"],
    ...     requirements=[],
    ...     data=WaldiezModelData(
    ...         base_url="https://example.com/v1",
    ...         api_key="1234567890",
    ...         api_type="openai",
    ...         temperature=0.5,
    ...         price={
    ...             "prompt_price_per_1k": 0.0001,
    ...             "completion_token_price_per_1k": 0.0002,
    ...         },
    ...     ),
    ... )
    >>> model2 = WaldiezModel(
    ...     id="wm-2",
    ...     name="llama3.2"  ,
    ...     description="A model for llamas :P.",
    ...     tags=["llama", "llama3.2"],
    ...     requirements=[],
    ...     data=WaldiezModelData(
    ...         base_url="https://example.com/v1",
    ...        api_key="1234567890",
    ...         api_type="openai",
    ...         temperature=0.5,
    ...         price={
    ...             "prompt_price_per_1k": 0.0001,
    ...             "completion_token_price_per_1k": 0.0002,
    ...         },
    ...     ),
    ... )
    >>> all_models = [model1, model2]
    >>> agent_model_ids = ["wm-1", "wm-2"]
    >>> export_agent_models(agent_model_ids, all_models, "llama_agent")

    llama_agent_llm_config = {
        "config_list": [
            {
                "model": "llama3.1",
                "base_url": "https://example.com/v1",
                "api_key": "1234567890",
                "api_type": "openai",
                "temperature": 0.5,
                "price": [0.0001, 0.0002],
            },
            {
                "model": "llama3.2",
                "base_url": "https://example.com/v1",
                "api_key": "1234567890",
                "api_type": "openai",
                "temperature": 0.5,
                "price": [0.0001, 0.0002],
            },
        ]
    }
    ```
    """
    content = f"{agent_name}_llm_config = " + "{\n"
    content += '    "config_list": [\n'
    for model_id in agent_model_ids:
        model = next((m for m in all_models if m.id == model_id), None)
        if model is not None:
            llm_config = model.get_llm_config()
            model_dict_str = get_object_string(llm_config, tabs=2)
            content += f"        {model_dict_str},\n"
    content += "    ]\n"
    content += "}\n"
    return content
