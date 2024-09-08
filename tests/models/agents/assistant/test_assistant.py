"""Test waldiez.models.agents.assistant.assistant.*."""

from waldiez.models.agents.assistant.assistant import WaldieAssistant


def test_waldie_assistant() -> None:
    """Test WaldieAssistant."""
    assistant = WaldieAssistant(id="wa-1", name="assistant")  # type: ignore
    assert assistant.data.human_input_mode == "NEVER"
    assert assistant.agent_type == "assistant"
