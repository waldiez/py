"""Waldie Model Data."""

from typing import Dict, Optional

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..common import WaldieBase

WaldieModelAPIType = Literal[
    "openai",
    "azure",
    "google",
    "anthropic",
    "mistral",
    "grog",
    "together",
    "other",
]


class WaldieModelPrice(WaldieBase):
    """Model Price.

    Attributes
    ----------
    prompt_price_per_1k : float
        The prompt price per 1k tokens.
    completion_token_price_per_1k : float
        The completion token price per 1k tokens.
    """

    prompt_price_per_1k: Annotated[
        Optional[float], Field(None, alias="promptPricePer1k")
    ]
    completion_token_price_per_1k: Annotated[
        Optional[float], Field(None, alias="completionTokenPricePer1k")
    ]


# pylint: disable=line-too-long
class WaldieModelData(WaldieBase):
    """Waldie Model Data.

    Attributes
    ----------
    base_url : Optional[str]
        The base url of the model, by default None.
    api_key : Optional[str]
        The api key to use with the model, by default None.
    api_type : Literal["openai","azure","google","anthropic","mistral","grog","together","other"]
        The api type of the model.
    api_version : Optional[str]
        The api version of the model, by default None.
    temperature : Optional[float]
        The temperature of the model, by default None.
    top_p : Optional[float]
        The top p of the model, by default None.
    max_tokens : Optional[int]
        The max tokens of the model, by default None.
    default_headers : Dict[str, str]
        The default headers of the model.
    price : Optional[WaldieModelPrice]
        The price of the model, by default None.
    """

    base_url: Annotated[
        Optional[str],
        Field(
            None,
            title="Base URL",
            description="The base url of the model",
            alias="baseUrl",
        ),
    ]
    api_key: Annotated[Optional[str], Field(None, alias="apiKey")]
    api_type: Annotated[WaldieModelAPIType, Field("other", alias="apiType")]
    api_version: Annotated[Optional[str], Field(None, alias="apiVersion")]
    temperature: Annotated[Optional[float], Field(None, alias="temperature")]
    top_p: Annotated[Optional[float], Field(None, alias="topP")]
    max_tokens: Annotated[Optional[int], Field(None, alias="maxTokens")]
    default_headers: Annotated[
        Dict[str, str], Field(alias="defaultHeaders", default_factory=dict)
    ]
    price: Annotated[Optional[WaldieModelPrice], Field(None)]
