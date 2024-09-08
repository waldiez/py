"""Test waldiez.models.agents."""

from waldiez.models.agents import WaldieAgents, WaldieAssistant, WaldieUserProxy
from waldiez.models.model import WaldieModel
from waldiez.models.skill import WaldieSkill


def test_waldie_agents() -> None:
    """Test WaldieAgents."""
    model = WaldieModel(
        id="wa-1",
        name="model",
        type="model",
        description="Model",
        tags=[],
        requirements=[],
        data={},  # type: ignore
    )
    skill = WaldieSkill(
        id="wa-2",
        name="skill",
        type="skill",
        description="Skill",
        tags=[],
        requirements=[],
        data={  # type: ignore
            "content": "def skill():\n    return 'skill'",
        },
    )
    assistant = WaldieAssistant(
        id="wa-1",
        name="assistant",
        type="agent",
        agent_type="assistant",
        description="Assistant",
        tags=[],
        requirements=[],
        data={  # type: ignore
            "model_ids": [model.id],
            "skills": [
                {"id": skill.id, "executor_id": "wa-1"},
            ],
        },
    )
    user = WaldieUserProxy(
        id="wa-2",
        name="user",
        type="agent",
        agent_type="user",
        description="User",
        tags=[],
        requirements=[],
        data={},  # type: ignore
    )
    agents = WaldieAgents(
        assistants=[assistant],
        users=[user],
        managers=[],
        rag_users=[],
    )
    assert agents.assistants == [assistant]
    assert next(agents.members) == user
    agents.validate_flow(model_ids=[model.id], skill_ids=[skill.id])
