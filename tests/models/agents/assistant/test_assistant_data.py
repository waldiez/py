"""Test waldiez.models.agents.assistant.assistant_data.*."""

from waldiez.models.agents.assistant.assistant_data import WaldieAssistantData


def test_waldie_assistant_data() -> None:
    """Test WaldieAssistantData."""
    assistant_data = WaldieAssistantData()  # type: ignore
    assert assistant_data.human_input_mode == "NEVER"
