"""Test waldiez.exporting.agents.termination_message.*."""

import pytest

from waldiez.exporting.agents.termination_message import (
    get_is_termination_message,
)
from waldiez.models import WaldiezAgent


def test_get_is_termination_message() -> None:
    """Test get_is_termination_message()."""
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "termination": {
                "type": "none",
            },
        },
    )
    agent_name = "agent_name"
    expected_output = ("None", "")
    # When
    output = get_is_termination_message(
        agent=agent,
        agent_name=agent_name,
    )
    # Then
    assert output == expected_output
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "termination": {
                "type": "keyword",
                "criterion": "exact",
                "keywords": ["stop", "terminate"],
            },
        },
    )
    # pylint: disable=line-too-long
    agent_name = "agent_name"
    expected_output = (
        'lambda x: any(x.get("content", "") == keyword for keyword in ["stop", "terminate"])',
        "",
    )
    # When
    output = get_is_termination_message(
        agent=agent,
        agent_name=agent_name,
    )
    # Then
    assert output == expected_output
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "termination": {
                "type": "keyword",
                "criterion": "found",
                "keywords": ["terminate"],
            },
        },
    )
    agent_name = "agent_name"
    expected_output = (
        'lambda x: any(x.get("content", "") and keyword in x.get("content", "") for keyword in ["terminate"])',
        "",
    )
    # When
    output = get_is_termination_message(
        agent=agent,
        agent_name=agent_name,
    )
    # Then
    assert output == expected_output
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "termination": {
                "type": "keyword",
                "criterion": "ending",
                "keywords": ["stop", "terminate"],
            },
        },
    )
    agent_name = "agent_name"
    expected_output = (
        'lambda x: any(x.get("content", "") and x.get("content", "").endswith(keyword) for keyword in ["stop", "terminate"])',
        "",
    )
    # When
    output = get_is_termination_message(
        agent=agent,
        agent_name=agent_name,
    )
    # Then
    assert output == expected_output
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "termination": {
                "type": "method",
                "method_content": (
                    "def is_termination_message(message):\n" "    return True"
                ),
            },
        },
    )
    agent_name = "agent_name"
    expected_output = (
        "is_termination_message_agent_name",
        (
            "\n\n"
            "def is_termination_message_agent_name(message):\n"
            "    # type: (dict) -> bool\n"
            "    return True\n\n"
        ),
    )
    # When
    output = get_is_termination_message(
        agent=agent,
        agent_name=agent_name,
    )
    # Then
    assert output == expected_output
    #
    with pytest.raises(ValueError):
        agent.data.termination.type = "invalid"  # type: ignore
        get_is_termination_message(
            agent=agent,
            agent_name=agent_name,
        )
