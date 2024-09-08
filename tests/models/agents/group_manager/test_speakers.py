"""Test waldiez.models.agents.group_manager.speakers.*."""

# pylint: disable=line-too-long

import pytest

from waldiez.models.agents.group_manager.speakers import (
    WaldieGroupManagerSpeakers,
)


def test_waldie_group_manager_speakers() -> None:
    """Test WaldieGroupManagerSpeakers."""
    # Given
    speakers_config = WaldieGroupManagerSpeakers(
        selection_method="auto",
        selection_custom_method=None,
        max_retries_for_selecting=None,
        selection_mode="repeat",
        allow_repeat=True,
        allowed_or_disallowed_transitions={},
        transitions_type="allowed",
    )
    # Then
    assert speakers_config.selection_method == "auto"
    assert speakers_config.custom_method_string is None

    # Given
    speakers_config = WaldieGroupManagerSpeakers(
        selection_method="custom",
        selection_custom_method=(
            "def custom_speaker_selection(last_speaker, groupchat):\n"
            "    return last_speaker"
        ),
        max_retries_for_selecting=None,
        selection_mode="repeat",
        allow_repeat=True,
        allowed_or_disallowed_transitions={},
        transitions_type="allowed",
    )

    # Then
    assert speakers_config.selection_method == "custom"
    assert speakers_config.custom_method_string == (
        "    # type: (ConversableAgent, GroupChat) -> Union[Agent, str, None]\n"
        "    return last_speaker"
    )

    with pytest.raises(ValueError):
        WaldieGroupManagerSpeakers(
            selection_method="custom",
            selection_custom_method="",
            max_retries_for_selecting=1,
            selection_mode="repeat",
            allow_repeat=True,
            allowed_or_disallowed_transitions={},
            transitions_type="allowed",
        )
    with pytest.raises(ValueError):
        WaldieGroupManagerSpeakers(
            selection_method="custom",
            selection_custom_method=(
                "def invalid_custom_speaker_selection(last_speaker, groupchat):\n"
                "    return last_speaker"
            ),
            max_retries_for_selecting=3,
            selection_mode="transition",
            allow_repeat=True,
            allowed_or_disallowed_transitions={},
            transitions_type="allowed",
        )
