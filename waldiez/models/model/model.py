"""Waldiez model(llm) model."""

import os
from typing import Any, Dict, List, Optional

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..common import WaldiezBase, now
from .model_data import WaldiezModelData


class WaldiezModel(WaldiezBase):
    """Waldiez Model class.

    Attributes
    ----------
    id : str
        The ID of the model.
    name : str
        The name of the model.
    description : str
        The description of the model.
    tags : List[str]
        The tags of the model.
    requirements : List[str]
        The requirements of the model.
    created_at : str
        The date and time when the model was created.
    updated_at : str
        The date and time when the model was last updated.
    data : WaldiezModelData
        The data of the model.
        See `waldiez.models.model.WaldiezModelData` for more information.
    """

    id: Annotated[
        str, Field(..., title="ID", description="The ID of the model.")
    ]
    type: Annotated[
        Literal["model"],
        Field(
            default="model",
            title="Type",
            description="The type of the 'node' in a graph.",
        ),
    ]
    name: Annotated[
        str, Field(..., title="Name", description="The name of the model.")
    ]
    description: Annotated[
        str,
        Field(
            ...,
            title="Description",
            description="The description of the model.",
        ),
    ]
    tags: Annotated[
        List[str],
        Field(
            default_factory=list,
            title="Tags",
            description="The tags of the model.",
        ),
    ]
    requirements: Annotated[
        List[str],
        Field(
            default_factory=list,
            title="Requirements",
            description="The requirements of the model.",
        ),
    ]
    created_at: Annotated[
        str,
        Field(
            default_factory=now,
            title="Create At",
            description="The date and time when the model was created.",
        ),
    ]
    updated_at: Annotated[
        str,
        Field(
            default_factory=now,
            title="Updated At",
            description="The date and time when the model was last updated.",
        ),
    ]
    data: Annotated[
        WaldiezModelData,
        Field(..., title="Data", description="The data of the model."),
    ]

    @property
    def api_key(self) -> str:
        """Get the model's api key.

        Either from the model's data or from the environment variables:

            - openai: 'OPENAI_API_KEY',
            - azure: 'AZURE_API_KEY',
            - google: 'GOOGLE_GEMINI_API_KEY',
            - anthropic: 'ANTHROPIC_API_KEY',
            - mistral: 'MISTRAL_API_KEY',
            - groq: 'GROQ_API_KEY',
            - together: 'TOGETHER_API_KEY',
            - nim: 'NIM_API_KEY',
            - other: 'OPENAI_API_KEY'
        """
        if self.data.api_key:
            return self.data.api_key
        env_key = "OPENAI_API_KEY"
        if self.data.api_type == "google":
            env_key = "GOOGLE_GEMINI_API_KEY"
        elif self.data.api_type not in ["openai", "other"]:
            env_key = f"{self.data.api_type.upper()}_API_KEY"
        api_key = os.environ.get(env_key, "")
        return api_key

    @property
    def price(self) -> Optional[List[float]]:
        """Get the model's price."""
        if self.data.price is None:
            return None
        if isinstance(
            self.data.price.prompt_price_per_1k, float
        ) and isinstance(self.data.price.completion_token_price_per_1k, float):
            return [
                self.data.price.prompt_price_per_1k,
                self.data.price.completion_token_price_per_1k,
            ]
        return None

    def get_llm_config(self, skip_price: bool = False) -> Dict[str, Any]:
        """Get the model's llm config.

        Parameters
        ----------
        skip_price : bool, optional
            Whether to skip the price, by default False

        Returns
        -------
        Dict[str, Any]
            The model's llm config dictionary.
        """
        _llm_config: Dict[str, Any] = {}
        _llm_config["model"] = self.name
        for attr, atr_type in [
            ("base_url", str),
            ("max_tokens", int),
            ("temperature", float),
            ("top_p", float),
            ("api_version", str),
            ("default_headers", dict),
        ]:
            value = getattr(self.data, attr)
            if value and isinstance(value, atr_type):
                _llm_config[attr] = value
        if self.data.api_type not in ["nim", "other"]:
            _llm_config["api_type"] = self.data.api_type
        other_attrs = ["api_key"] if skip_price else ["api_key", "price"]
        for attr in other_attrs:
            value = getattr(self, attr)
            if value:
                _llm_config[attr] = value
        return _llm_config
