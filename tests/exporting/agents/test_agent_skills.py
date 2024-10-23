"""Test waldiez.exporting.agents.agent_skills.*."""

from waldiez.exporting.agents.agent_skills import get_agent_skill_registrations
from waldiez.models import WaldiezAgent, WaldiezSkill


def test_get_agent_skill_registrations() -> None:
    """Test get_agent_skill_registrations()."""
    # Given
    agent = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent_name",
        agent_type="assistant",
        data={  # type: ignore
            "skills": [
                {
                    "id": "ws-1",
                    "executor_id": "wa-2",
                },
            ],
        },
    )
    skill = WaldiezSkill(  # type: ignore
        id="ws-1",
        name="skill_name",
        description="Skill description.",
        data={  # type: ignore
            "content": (
                "def skill_name():\n"
                '    """Skill description."""\n'
                "    return 42"
            ),
        },
    )
    agent_names = {"wa-1": "agent_name", "wa-2": "executor_agent_name"}
    all_skills = [skill]
    skill_names = {"ws-1": "skill_name"}
    expected_output = (
        "register_function(\n"
        "    skill_name,\n"
        "    caller=agent_name,\n"
        "    executor=executor_agent_name,\n"
        '    name="skill_name",\n'
        '    description="Skill description.",\n'
        ")\n\n"
    )
    # When
    output = get_agent_skill_registrations(
        agent=agent,
        agent_names=agent_names,
        all_skills=all_skills,
        skill_names=skill_names,
    )
    # Then
    assert output == expected_output
    # When
    output = get_agent_skill_registrations(
        agent=agent,
        agent_names=agent_names,
        all_skills=[],
        skill_names=skill_names,
    )
    # Then
    assert output == ""
