"""Test waldiez.models.agents.rag_user.rag_user.*."""

from waldiez.models.agents.rag_user.rag_user import WaldieRagUser


def test_waldie_rag_user() -> None:
    """Test WaldieRagUser."""
    rag_user = WaldieRagUser(id="wa-1", name="rag_user")  # type: ignore
    assert rag_user.agent_type == "rag_user"
    assert rag_user.data.human_input_mode == "ALWAYS"
    assert rag_user.retrieve_config
