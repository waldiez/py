"""Test waldiez.waldiez.*."""

import os
import tempfile

import pytest
from autogen.version import __version__ as ag2_version  # type: ignore

from waldiez import Waldiez

from .exporting.flow_helpers import get_flow


def test_waldiez() -> None:
    """Test Waldiez with retrievechat requirement."""
    flow = get_flow()
    waldiez = Waldiez(flow=flow)
    assert waldiez.name == flow.name

    flow_dump = waldiez.model_dump_json(by_alias=True)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".waldiez", delete=False
    ) as file:
        file.write(flow_dump)
        file_path = file.name
        file.close()
    waldiez2 = Waldiez.load(file_path)
    os.remove(file_path)
    assert waldiez2.name == flow.name
    assert waldiez2.description == flow.description
    assert waldiez2.tags == flow.tags
    assert next(waldiez2.models)
    assert waldiez2.has_rag_agents
    skill = next(waldiez2.skills)
    assert f"pyautogen[retrievechat]=={ag2_version}" in waldiez2.requirements
    assert "SKILL_KEY" in skill.secrets
    assert "SKILL_KEY" == waldiez2.get_flow_env_vars()[0][0]
    for agent in waldiez2.agents:
        if agent.agent_type == "manager":
            assert waldiez2.get_group_chat_members(agent)
        else:
            assert not waldiez2.get_group_chat_members(agent)
    assert waldiez2.chats


def test_waldiez_without_rag() -> None:
    """Test Waldiez."""
    flow_dict = get_flow().model_dump(by_alias=True)
    # remove the rag user from the agents
    flow_dict["data"]["agents"]["ragUsers"] = []
    # also remove any chats that has source or target "wa-4" (the rag agent)
    flow_dict["data"]["chats"] = [
        chat
        for chat in flow_dict["data"]["chats"]
        if (
            chat["data"]["source"] != "wa-4"
            and chat["data"]["target"] != "wa-4"
        )
    ]
    waldiez = Waldiez.from_dict(data=flow_dict)
    assert waldiez.name == flow_dict["name"]
    assert waldiez.description == flow_dict["description"]
    assert waldiez.tags == flow_dict["tags"]
    assert next(waldiez.models)
    assert not waldiez.has_rag_agents
    assert f"pyautogen[retrievechat]=={ag2_version}" not in waldiez.requirements
    assert f"pyautogen=={ag2_version}" in waldiez.requirements


def test_waldiez_errors() -> None:
    """Test Waldiez errors."""
    with pytest.raises(ValueError):
        Waldiez.load("non_existent_file")

    with pytest.raises(ValueError):
        Waldiez.from_dict(
            name="flow",
            description="flow description",
            tags=["tag"],
            requirements=["requirement"],
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Waldiez.from_dict(
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Waldiez.from_dict(
            data={"type": "other", "data": {}},
        )

    with tempfile.NamedTemporaryFile(
        "w", suffix=".waldiez", delete=False
    ) as file:
        file.write("invalid json")
        file_path = file.name
        file.close()
    with pytest.raises(ValueError):
        Waldiez.load(file_path)
    os.remove(file_path)
