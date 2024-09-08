"""Test waldiez.models.agents.group_manager.group_manager_data.*."""

from waldiez.models.agents.group_manager.group_manager_data import (
    WaldieGroupManagerData,
)


def test_waldie_group_manager_data() -> None:
    """Test WaldieGroupManagerData."""
    group_manager_data = WaldieGroupManagerData()  # type: ignore
    assert group_manager_data.human_input_mode == "NEVER"
    # assert defaults
    assert group_manager_data.speakers.selection_method == "auto"
    assert group_manager_data.speakers.selection_custom_method is None
    assert group_manager_data.speakers.max_retries_for_selecting is None
    assert group_manager_data.speakers.selection_mode == "repeat"
    assert group_manager_data.speakers.allow_repeat is True
    assert not group_manager_data.speakers.allowed_or_disallowed_transitions
    assert group_manager_data.speakers.transitions_type == "allowed"
    assert group_manager_data.speakers.custom_method_string is None
