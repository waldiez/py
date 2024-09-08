"""Test waldiez.models.flow.flow_data.*."""

import pytest

from waldiez.models.flow.flow_data import WaldieFlowData


def test_waldie_flow_data() -> None:
    """Test WaldieFlowData."""
    # Given
    assistant_1 = {
        "id": "wa-1",
        "name": "assistant1",
        "type": "agent",
        "agent_type": "assistant",
    }
    assistant_2 = {
        "id": "wa-2",
        "name": "assistant2",
        "type": "agent",
        "agent_type": "assistant",
    }
    flow_data = WaldieFlowData(
        nodes=[],
        edges=[],
        viewport={},
        agents={  # type: ignore
            "users": [],
            "assistants": [assistant_1, assistant_2],
            "managers": [],
            "rag_users": [],
        },
        models=[],
        skills=[],
        chats=[],
    )
    # Then
    assert not flow_data.nodes
    assert not flow_data.edges
    assert not flow_data.viewport
    assert not flow_data.agents.users
    assert len(flow_data.agents.assistants) == 2
    assert not flow_data.agents.managers
    assert not flow_data.agents.rag_users
    assert not flow_data.models
    assert not flow_data.skills
    assert not flow_data.chats

    with pytest.raises(ValueError):
        # at least 2 agents are required
        WaldieFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents={  # type: ignore
                "users": [],
                "assistants": [],
                "managers": [],
                "rag_users": [],
            },
            models=[],
            skills=[],
            chats=[],
        )
    with pytest.raises(ValueError):
        # not unique agent ids
        WaldieFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents={  # type: ignore
                "users": [],
                "assistants": [assistant_1, assistant_1],
                "managers": [],
                "rag_users": [],
            },
            models=[],
            skills=[],
            chats=[],
        )
