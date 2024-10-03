"""Test waldiez.models.chat.chat_summary.*."""

import pytest

from waldiez.models.chat.chat_summary import WaldieChatSummary


def test_waldie_chat_summary() -> None:
    """Test WaldieChatSummary."""
    # Given
    chat_summary = WaldieChatSummary(  # type: ignore
        prompt="prompt",
    )
    assert chat_summary.prompt == "prompt"
    assert not chat_summary.args

    # Given
    chat_summary = WaldieChatSummary(
        method="lastMsg",
        prompt="prompt",
        args={"key": "value"},
    )
    assert chat_summary.method == "last_msg"
    summary_dump = chat_summary.model_dump(by_alias=True)
    assert summary_dump["method"] == "lastMsg"
    assert summary_dump["prompt"] == "prompt"
    assert summary_dump["args"] == {"key": "value"}
    summary_dump = chat_summary.model_dump(by_alias=False)
    assert summary_dump["method"] == "last_msg"

    # Given
    chat_summary = WaldieChatSummary(
        method="reflectionWithLlm",
        prompt="prompt",
        args={"key": "value"},
    )
    assert chat_summary.method == "reflection_with_llm"
    summary_dump = chat_summary.model_dump(by_alias=True)
    assert summary_dump["method"] == "reflectionWithLlm"
    summary_dump = chat_summary.model_dump(by_alias=False)
    assert summary_dump["method"] == "reflection_with_llm"

    with pytest.raises(ValueError):
        chat_summary = WaldieChatSummary(prompt=1)  # type: ignore
