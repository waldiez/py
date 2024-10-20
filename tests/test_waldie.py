"""Test waldiez.waldie.*."""

import os
import tempfile

import pytest
from autogen.version import __version__ as autogen_version  # type: ignore

from waldiez import Waldie

from .exporting.flow_helpers import get_flow


def test_waldie() -> None:
    """Test Waldie with retrievechat requirement."""
    flow = get_flow()
    waldie = Waldie(flow=flow)
    assert waldie.name == flow.name

    flow_dump = waldie.model_dump_json(by_alias=True)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".waldiez", delete=False
    ) as file:
        file.write(flow_dump)
        file_path = file.name
        file.close()
    waldie2 = Waldie.load(file_path)
    os.remove(file_path)
    assert waldie2.name == flow.name
    assert waldie2.description == flow.description
    assert waldie2.tags == flow.tags
    assert next(waldie2.models)
    assert waldie2.has_rag_agents
    skill = next(waldie2.skills)
    assert (
        f"autogen-agentchat[retrievechat]=={autogen_version}"
        in waldie2.requirements
    )
    assert "SKILL_KEY" in skill.secrets
    assert "SKILL_KEY" == waldie2.get_flow_env_vars()[0][0]
    for agent in waldie2.agents:
        if agent.agent_type == "manager":
            assert waldie2.get_group_chat_members(agent)
        else:
            assert not waldie2.get_group_chat_members(agent)
    assert waldie2.chats


def test_waldie_without_rag() -> None:
    """Test Waldie."""
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
    waldie = Waldie.from_dict(data=flow_dict)
    assert waldie.name == flow_dict["name"]
    assert waldie.description == flow_dict["description"]
    assert waldie.tags == flow_dict["tags"]
    assert next(waldie.models)
    assert not waldie.has_rag_agents
    assert (
        f"autogen-agentchat[retrievechat]=={autogen_version}"
        not in waldie.requirements
    )
    assert f"autogen-agentchat=={autogen_version}" in waldie.requirements


def test_waldie_errors() -> None:
    """Test Waldie errors."""
    with pytest.raises(ValueError):
        Waldie.load("non_existent_file")

    with pytest.raises(ValueError):
        Waldie.from_dict(
            name="flow",
            description="flow description",
            tags=["tag"],
            requirements=["requirement"],
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Waldie.from_dict(
            data={"type": "flow", "data": {}},
        )

    with pytest.raises(ValueError):
        Waldie.from_dict(
            data={"type": "other", "data": {}},
        )

    with tempfile.NamedTemporaryFile(
        "w", suffix=".waldiez", delete=False
    ) as file:
        file.write("invalid json")
        file_path = file.name
        file.close()
    with pytest.raises(ValueError):
        Waldie.load(file_path)
    os.remove(file_path)
