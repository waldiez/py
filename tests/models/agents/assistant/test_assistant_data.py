"""Test waldiez.models.agents.assistant.assistant_data.*."""

from waldiez.models.agents.assistant.assistant_data import WaldiezAssistantData


def test_waldiez_assistant_data() -> None:
    """Test WaldiezAssistantData."""
    assistant_data = WaldiezAssistantData()  # type: ignore
    assert assistant_data.human_input_mode == "NEVER"
