"""Test waldiez.models.agents.user_proxy.user_proxy.*."""

from waldiez.models.agents.user_proxy.user_proxy import WaldiezUserProxy


def test_waldiez_user_proxy() -> None:
    """Test WaldiezUserProxy."""
    user_proxy = WaldiezUserProxy(id="wa-1", name="user")  # type: ignore
    assert user_proxy.data.human_input_mode == "ALWAYS"
    assert user_proxy.agent_type == "user"
