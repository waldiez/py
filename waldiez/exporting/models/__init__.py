"""Model/LLM related string generation functions.

Functions
---------
export_models
    Get the string representations of the LLM configs.
"""

from typing import Dict, List

from waldiez.models import WaldieModel

from ..utils import get_comment, get_object_string


def export_models(
    all_models: List[WaldieModel],
    model_names: Dict[str, str],
    notebook: bool,
) -> str:
    """Get the string representations of the LLM configs.

    Parameters
    ----------
    all_models : List[WaldieModel]
        The models.
    model_names : Dict[str, str]
        A mapping of model ids to model names.
    notebook : bool
        Whether to export the string for a jupyter notebook.

    Returns
    -------
    str
        The string representation of the LLM configs.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldieModel, WaldieModelData
    >>> model = WaldieModel(
    ...     id="wm-1",
    ...     name="llama3.1"  ,
    ...     description="A model for llamas :P.",
    ...     tags=["llama", "llama3.1"],
    ...     requirements=[],
    ...     data=WaldieModelData(
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
    llama3_1 = {
        "model": "llama3.1",
        "base_url": "https://example.com/v1",
        "api_key": "1234567890",
        "api_type": "openai",
        "temperature": 0.5,
        "price": [0.0001, 0.0002],
    }
    ```
    """
    content = get_comment("models", notebook) + "\n"
    if len(all_models) == 1:
        model_name = model_names[all_models[0].id]
        model_dict_str = get_object_string(all_models[0].llm_config, tabs=0)
        content += f"{model_name} = {model_dict_str}\n"
        return content
    for model in all_models:
        model_name = model_names[model.id]
        content += (
            f"{model_name} = {get_object_string(model.llm_config, tabs=0)}\n"
        )
    return content