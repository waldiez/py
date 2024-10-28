"""Test waldiez.models.agents.agent.termination_message.*."""

# pylint: disable=line-too-long

import pytest

from waldiez.models.agents.agent.termination_message import (
    WaldiezAgentTerminationMessage,
)


def test_waldiez_agent_termination_message_keyword() -> None:
    """Test WaldiezAgentTerminationMessage with keyword."""
    termination_message = WaldiezAgentTerminationMessage(
        type="keyword",
        keywords=["keyword-1", "keyword-2"],
        criterion="found",
        method_content=None,
    )
    assert termination_message.type == "keyword"
    assert termination_message.keywords == ["keyword-1", "keyword-2"]
    assert termination_message.criterion == "found"
    assert termination_message.method_content is None
    assert termination_message.string == (
        'lambda x: any(x.get("content", "") and keyword in x.get("content", "") for keyword in ["keyword-1", "keyword-2"])'
    )

    termination_message = WaldiezAgentTerminationMessage(
        type="keyword",
        keywords=["keyword-1", "keyword-2"],
        criterion="ending",
        method_content=None,
    )
    assert termination_message.string == (
        'lambda x: any(x.get("content", "") and x.get("content", "").endswith(keyword) for keyword in ["keyword-1", "keyword-2"])'
    )

    termination_message = WaldiezAgentTerminationMessage(
        type="keyword",
        keywords=["keyword-1", "keyword-2"],
        criterion="exact",
        method_content=None,
    )
    assert termination_message.string == (
        'lambda x: any(x.get("content", "") == keyword for keyword in ["keyword-1", "keyword-2"])'
    )

    with pytest.raises(ValueError):
        WaldiezAgentTerminationMessage(
            type="keyword",
            keywords=["TERMINATE"],
            criterion=None,
            method_content=None,
        )

    with pytest.raises(ValueError):
        WaldiezAgentTerminationMessage(
            type="keyword",
            keywords=[],
            criterion="found",
            method_content=None,
        )


def test_waldiez_agent_termination_message_method() -> None:
    """Test WaldiezAgentTerminationMessage with method."""
    termination_message = WaldiezAgentTerminationMessage(
        type="method",
        keywords=[],
        criterion=None,
        method_content="def is_termination_message(message):\n    return False",
    )
    assert termination_message.type == "method"
    assert not termination_message.keywords
    assert termination_message.criterion is None
    assert (
        termination_message.method_content
        == "def is_termination_message(message):\n    return False"
    )
    assert (
        termination_message.string
        == "    # type: (dict) -> bool\n    return False"
    )

    with pytest.raises(ValueError):
        WaldiezAgentTerminationMessage(
            type="method",
            keywords=[],
            criterion=None,
            method_content=None,
        )

    with pytest.raises(ValueError):
        WaldiezAgentTerminationMessage(
            type="method",
            keywords=[],
            criterion=None,
            method_content="def is_termination_message():\n    return False",
        )
