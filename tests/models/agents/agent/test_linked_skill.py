"""Test waldiez.models.agents.agent.linked_skill.*."""

from waldiez.models.agents.agent.linked_skill import WaldieAgentLinkedSkill


def test_waldie_agent_linked_skill() -> None:
    """Test WaldieAgentLinkedSkill."""
    linked_skill = WaldieAgentLinkedSkill(id="skill_id", executor_id="agent_id")
    assert linked_skill.id == "skill_id"
    assert linked_skill.executor_id == "agent_id"
