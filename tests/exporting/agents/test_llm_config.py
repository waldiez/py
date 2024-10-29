"""Test waldiez.exporting.agents.llm_config.*."""

from waldiez.exporting.agents.llm_config import get_agent_llm_config
from waldiez.models import WaldiezAgent, WaldiezModel, WaldiezModelData


def test_get_agent_llm_config() -> None:
    """Test get_agent_llm_config()."""
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "model_ids": ["wm-1"],
        },
    )
    model_names = {"wm-1": "model_name"}
    model = WaldiezModel(
        id="wm-1",
        name="model_name",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.1"],
        requirements=[],
        data=WaldiezModelData(
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

    expected_output = "model_name_llm_config"
    # When
    output = get_agent_llm_config(
        agent=agent,
        model_names=model_names,
        all_models=[model],
        agent_name="agent_name",
    )
    # Then
    assert output[0] == expected_output
    assert not output[1]
    # When
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "model_ids": ["wm-1", "wm-2"],
        },
    )
    model_names = {"wm-1": "model_name_1", "wm-2": "model_name_2"}
    model1 = WaldiezModel(
        id="wm-1",
        name="model_name_1",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.1"],
        requirements=[],
        data=WaldiezModelData(
            base_url="https://example.com/v8",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.3,
            top_p=0.9,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.001,
                "completion_token_price_per_1k": 0.002,
            },
        ),
    )
    model2 = WaldiezModel(
        id="wm-2",
        name="model_name_2",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.2"],
        requirements=[],
        data=WaldiezModelData(
            base_url="https://example.com/v9",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.4,
            top_p=0.8,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.003,
                "completion_token_price_per_1k": 0.004,
            },
        ),
    )
    expected_arg_output = "agent_name_llm_config"
    expected_content_output = """
agent_name_llm_config = {
    "config_list": [
        {
            "model": "model_name_1",
            "base_url": "https://example.com/v8",
            "temperature": 0.3,
            "top_p": 0.9,
            "api_type": "openai",
            "api_key": "1234567890",
            "price": [
                0.001,
                0.002
            ]
        },
        {
            "model": "model_name_2",
            "base_url": "https://example.com/v9",
            "temperature": 0.4,
            "top_p": 0.8,
            "api_type": "openai",
            "api_key": "1234567890",
            "price": [
                0.003,
                0.004
            ]
        },
    ]
}

"""
    # When
    output = get_agent_llm_config(
        agent=agent,
        model_names=model_names,
        all_models=[model1, model2],
        agent_name="agent_name",
    )
    # Then
    assert output[0] == expected_arg_output
    assert output[1] == expected_content_output
