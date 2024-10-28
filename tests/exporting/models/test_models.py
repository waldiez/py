"""Test waldiez.exporting.models*."""

import uuid
from pathlib import Path

from waldiez.exporting.models import export_models
from waldiez.models import WaldiezModel, WaldiezModelData


def test_export_models(tmp_path: Path) -> None:
    """Test export_models().

    Parameters
    ----------
    tmp_path : Path
        A pytest fixture to provide a temporary directory.
    """
    # Given
    model1 = WaldiezModel(
        id="wm-1",
        name="llama3.1",
        type="model",
        description="A model for llamas :P.",
        tags=["llama3.1 8b"],
        requirements=[],
        data=WaldiezModelData(
            base_url="https://example.com/v1",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.6,
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

llama3_1_llm_config = {
    "config_list": [
        {
            "model": "llama3.1",
            "base_url": "https://example.com/v1",
            "temperature": 0.6,
            "api_type": "openai",
            "api_key": get_model_api_key("llama3_1"),
            "price": [
                0.0001,
                0.0002
            ]
        }
    ]
}
"""

    assert result == expected

    # Given
    model2 = WaldiezModel(
        id="wm-1",
        name="anthropic_model",
        type="model",
        description="An anthropic model.",
        tags=[],
        requirements=[],
        data=WaldiezModelData(
            base_url="https://example.com/v2",
            api_key="1234567890",
            api_type="anthropic",
            api_version=None,
            temperature=0.7,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0001,
                "completion_token_price_per_1k": 0.0002,
            },
        ),
    )
    model_names = {"wm-1": "anthropic_model"}
    output_dir = tmp_path / uuid.uuid4().hex
    output_dir.mkdir(exist_ok=True)
    # When
    result = export_models([model2], model_names, True, output_dir)
    # Then
    expected_str = """
# ## Models

anthropic_model_llm_config = {
    "config_list": [
        {
            "model": "anthropic_model",
            "base_url": "https://example.com/v2",
            "temperature": 0.7,
            "api_type": "anthropic",
            "api_key": get_model_api_key("anthropic_model"),
            "price": [
                0.0001,
                0.0002
            ]
        }
    ]
}
"""
    assert result == expected_str

    # Given
    model3 = WaldiezModel(
        id="wm-2",
        name="groq_model",
        type="model",
        description="A groq model.",
        tags=["groq"],
        requirements=[],
        data=WaldiezModelData(
            base_url="https://example.com/v4",
            api_key="1234567890",
            api_type="groq",
            api_version=None,
            temperature=0.8,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0002,
                "completion_token_price_per_1k": 0.0003,
            },
        ),
    )
    model_names = {"wm-1": "llama3_1", "wm-2": "groq_model"}
    # When
    result = export_models([model1, model3], model_names, True)
    # Then
    expected = """
# ## Models

llama3_1_llm_config = {
    "config_list": [
        {
            "model": "llama3.1",
            "base_url": "https://example.com/v1",
            "temperature": 0.6,
            "api_type": "openai",
            "api_key": get_model_api_key("llama3_1"),
            "price": [
                0.0001,
                0.0002
            ]
        }
    ]
}
groq_model_llm_config = {
    "config_list": [
        {
            "model": "groq_model",
            "base_url": "https://example.com/v4",
            "temperature": 0.8,
            "api_type": "groq",
            "api_key": get_model_api_key("groq_model"),
            "price": [
                0.0002,
                0.0003
            ]
        }
    ]
}
"""
    assert result == expected
    assert (output_dir / "waldiez_api_keys.py").exists()
