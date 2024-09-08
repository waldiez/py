"""Test waldiez.exporting.models*."""

from waldiez.exporting.models import export_models
from waldiez.models import WaldieModel, WaldieModelData


def test_export_models() -> None:
    """Test export_models()."""
    # Given
    model1 = WaldieModel(
        id="wm-1",
        name="llama3.1",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.1"],
        requirements=[],
        data=WaldieModelData(
            base_url="https://example.com/v1",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.5,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0001,
                "completion_token_price_per_1k": 0.0002,
            },
        ),
    )
    model_names = {"wm-1": "llama3_1"}
    # When
    result = export_models([model1], model_names, True)
    # Then
    expected = """
# ## Models

llama3_1 = {
    "model": "llama3.1",
    "base_url": "https://example.com/v1",
    "temperature": 0.5,
    "api_type": "openai",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}
"""

    assert result == expected

    # Given
    model2 = WaldieModel(
        id="wm-2",
        name="llama3.2",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.2"],
        requirements=[],
        data=WaldieModelData(
            base_url="https://example.com/v2",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.5,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0001,
                "completion_token_price_per_1k": 0.0002,
            },
        ),
    )
    model_names = {"wm-1": "llama3_1", "wm-2": "llama3_2"}
    # When
    result = export_models([model1, model2], model_names, True)
    # Then
    expected = """
# ## Models

llama3_1 = {
    "model": "llama3.1",
    "base_url": "https://example.com/v1",
    "temperature": 0.5,
    "api_type": "openai",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}

llama3_2 = {
    "model": "llama3.2",
    "base_url": "https://example.com/v2",
    "temperature": 0.5,
    "api_type": "openai",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}
"""
