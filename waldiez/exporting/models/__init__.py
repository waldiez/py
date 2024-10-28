"""Model/LLM related string generation functions.

Functions
---------
export_models
    Get the string representations of the LLM configs.
"""

from pathlib import Path
from typing import Dict, List, Optional

from waldiez.models import WaldiezModel

from ..utils import get_comment, get_object_string


def export_models(
    all_models: List[WaldiezModel],
    model_names: Dict[str, str],
    notebook: bool,
    output_dir: Optional[Path] = None,
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
    output_dir : Optional[Path]
        The output directory to write the api keys.
    Returns
    -------
    str
        The string representation of the models.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezModel, WaldiezModelData
    >>> api_key = "1234567890"
    ... model = WaldiezModel(
    ...     id="wm-1",
    ...     name="llama3.1"  ,
    ...     description="A model for llamas :P.",
    ...     tags=["llama", "llama3.1"],
    ...     requirements=[],
    ...     data=WaldiezModelData(
    ...         base_url="https://example.com/v1",
    ...         api_key=api_key,
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
            "model": "llama3_1",
            "base_url": "https://example.com/v1",
            "api_key": get_model_api_key("llama3_1"),
            "api_type": "openai",
            "temperature": 0.5,
            "price": [0.0001, 0.0002],
        }]
    }
    ```
    """
    content = get_comment("models", notebook) + "\n"
    for model in all_models:
        model_name = model_names[model.id]
        llm_config = model.get_llm_config()
        llm_config["api_key"] = f'get_model_api_key("{model_name}")'
        model_dict_str = get_object_string(llm_config, tabs=2)
        model_dict_str = model_dict_str.replace(
            f'"get_model_api_key("{model_name}")"',
            f'get_model_api_key("{model_name}")',
        )
        content += f"{model_name}_llm_config = " + "{\n"
        content += '    "config_list": [\n'
        content += f"        {model_dict_str}\n"
        content += "    ]\n"
        content += "}\n"
    if output_dir:
        write_api_keys(all_models, model_names, output_dir)
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


def write_api_keys(
    all_models: List[WaldiezModel],
    model_names: Dict[str, str],
    output_dir: Path,
) -> None:
    """Write the api keys to a separate file.

    Parameters
    ----------
    all_models : List[WaldiezModel]
        All the models in the flow.
    model_names : Dict[str, str]
        A mapping of model ids to model names.
    output_dir : Path
        The output directory to write the api keys.
    """
    # example call: llama3_1_api_key = get_model_api_key("llama3_1")
    api_keys_content = '''
"""API keys for the models."""

__ALL_MODEL_API_KEYS__ = {
'''
    for model in all_models:
        model_name = model_names[model.id]
        api_keys_content += f'    "{model_name}": "{model.api_key}",\n'
    api_keys_content += "}\n"

    api_keys_content += '''

def get_model_api_key(model_name: str) -> str:
    """Get the api key for the model.

    Parameters
    ----------
    model_name : str
        The name of the model.

    Returns
    -------
    str
        The api key for the model.
    """
    return __ALL_MODEL_API_KEYS__.get(model_name, "")
'''

    with open(output_dir / "waldiez_api_keys.py", "w", encoding="utf-8") as f:
        f.write(api_keys_content)
