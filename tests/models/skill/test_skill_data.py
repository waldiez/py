"""Test waldiez.models.skill.skill_data.*."""

import pytest

from waldiez.models.skill import WaldieSkillData


def test_waldie_skill_data() -> None:
    """Test WaldieSkillData."""
    # Given
    content = "print('hello, world')"
    secrets = {"API_KEY": "api_key"}
    # When
    skill_data = WaldieSkillData(content=content, secrets=secrets)
    # Then
    assert skill_data.content == content
    assert skill_data.secrets == secrets

    # Given
    skill_data = WaldieSkillData(content=content)  # type: ignore
    # Then
    assert skill_data.content == content
    assert not skill_data.secrets

    with pytest.raises(ValueError):
        skill_data = WaldieSkillData()  # type: ignore
