"""Test waldiez.models.agents.agent.agent.*."""

import pytest

from waldiez.models.agents.agent import (
    WaldieAgent,
    WaldieAgentCodeExecutionConfig,
    WaldieAgentData,
    WaldieAgentLinkedSkill,
    WaldieAgentNestedChat,
    WaldieAgentTeachability,
    WaldieAgentTerminationMessage,
)


def test_waldie_agent() -> None:
    """Test WaldieAgent."""
    agent = WaldieAgent(
        id="wa-1",
        name="agent-1",
        type="agent",
        description="description",
        agent_type="assistant",
        tags=["tag-1", "tag-2"],
        requirements=["req-1", "req-2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieAgentData(
            system_message="system_message",
            human_input_mode="NEVER",
            max_tokens=100,
            agent_default_auto_reply="auto_reply",
            max_consecutive_auto_reply=5,
            termination=WaldieAgentTerminationMessage(
                type="none",
                keywords=[],
                criterion=None,
                method_content=None,
            ),
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            code_execution_config=WaldieAgentCodeExecutionConfig(
                work_dir="work_dir",
                use_docker=True,
                timeout=60,
                last_n_messages=5,
                functions=["ws-1"],
            ),
            model_ids=["wm-1"],
            skills=[
                WaldieAgentLinkedSkill(
                    id="ws-1",
                    executor_id="wa-1",
                )
            ],
            nested_chats=[
                WaldieAgentNestedChat(
                    triggered_by=[],
                    messages=[],
                )
            ],
        ),
    )
    assert agent.id == "wa-1"
    agent.validate_linked_models(["wm-1"])
    agent.validate_linked_skills(skill_ids=["ws-1"], agent_ids=["wa-1"])
    agent.validate_code_execution(
        skill_ids=["ws-1"],
    )
    with pytest.raises(ValueError):
        agent.validate_code_execution(
            skill_ids=["ws-2"],
        )
    with pytest.raises(ValueError):
        agent.validate_linked_models(["wm-2"])
    with pytest.raises(ValueError):
        agent.validate_linked_skills(skill_ids=["ws-2"], agent_ids=["wa-1"])
    with pytest.raises(ValueError):
        agent.validate_linked_skills(skill_ids=["ws-1"], agent_ids=["wa-2"])
