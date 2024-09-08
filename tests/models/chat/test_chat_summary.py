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

    with pytest.raises(ValueError):
        chat_summary = WaldieChatSummary()  # type: ignore
