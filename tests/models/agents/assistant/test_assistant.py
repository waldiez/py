"""Test waldiez.models.agents.assistant.assistant.*."""

from waldiez.models.agents.assistant.assistant import WaldiezAssistant


def test_waldiez_assistant() -> None:
    """Test WaldiezAssistant."""
    assistant = WaldiezAssistant(id="wa-1", name="assistant")  # type: ignore
    assert assistant.data.human_input_mode == "NEVER"
    assert assistant.agent_type == "assistant"
