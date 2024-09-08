"""Test waldiez.exporting.agents.llm_config.*."""

from waldiez.exporting.agents.llm_config import get_agent_llm_config
from waldiez.models import WaldieAgent


def test_get_agent_llm_config() -> None:
    """Test get_agent_llm_config()."""
    # Given
    agent = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "model_ids": ["wm-1"],
        },
    )
    model_names = {"wm-1": "model_name"}
    expected_output = "model_name"
    # When
    output = get_agent_llm_config(
        agent=agent,
        model_names=model_names,
    )
    # Then
    assert output == expected_output
    # When
    agent = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "model_ids": ["wm-1", "wm-2"],
        },
    )
    model_names = {"wm-1": "model_name_1", "wm-2": "model_name_2"}
    expected_output = (
        "{\n"
        '    "config_list": [\n'
        "        model_name_1,\n"
        "        model_name_2,\n"
        "    ]\n"
        "}"
    )
    # When
    output = get_agent_llm_config(
        agent=agent,
        model_names=model_names,
    )
    # Then
    assert output == expected_output
    # When
    agent = WaldieAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "model_ids": [],
        },
    )
    model_names = {}
    expected_output = "False"
    # When
    output = get_agent_llm_config(
        agent=agent,
        model_names=model_names,
    )
    # Then
    assert output == expected_output
