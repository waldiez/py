"""Test waldiez.exporting.skills.skills*."""

import os
import tempfile

from waldiez.exporting.skills import export_skills, get_agent_skill_registration
from waldiez.models import WaldiezSkill, WaldiezSkillData


def test_get_agent_skill_registration() -> None:
    """Test get_agent_skill_registration()."""
    # Given
    caller_name = "agent1"
    executor_name = "agent2"
    skill_name = "skill1"
    skill_description = "A skill that does something."
    # When
    result = get_agent_skill_registration(
        caller_name=caller_name,
        executor_name=executor_name,
        skill_name=skill_name,
        skill_description=skill_description,
    )
    # Then
    expected = """register_function(
    skill1,
    caller=agent1,
    executor=agent2,
    name="skill1",
    description="A skill that does something.",
)"""
    assert result == expected


def test_export_skills() -> None:
    """Test export_skills()."""
    # Given
    skill1 = WaldiezSkill(
        id="ws-1",
        name="skill1",
        type="skill",
        tags=[],
        requirements=[],
        description="A skill that does something.",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezSkillData(
            content="def skill1():\n    print('skill1')",
            secrets={},
        ),
    )
    skill2 = WaldiezSkill(
        id="ws-2",
        name="skill2",
        type="skill",
        tags=[],
        requirements=[],
        description="A skill that does something else.",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezSkillData(
            content="def skill2():\n    print('skill2')",
            secrets={"SKILL_2_KEY": "123456"},
        ),
    )
    skill_names = {"ws-1": "skill1", "ws-2": "skill2"}
    # When
    result = export_skills(
        skills=[skill1, skill2],
        skill_names=skill_names,
    )
    # Then
    expected_imports = {
        "from skill1 import skill1",
        "from skill2 import skill2",
    }
    expected_secrets = {("SKILL_2_KEY", "123456")}
    assert result[0] == expected_imports
    assert result[1] == expected_secrets

    # Given
    with tempfile.TemporaryDirectory() as temp_output_dir:
        # When
        export_skills(
            skills=[skill1, skill2],
            skill_names=skill_names,
            output_dir=temp_output_dir,
        )
        # Then
        expected_file = os.path.join(temp_output_dir, "skill1.py")
        assert os.path.exists(expected_file)
        os.remove(expected_file)
