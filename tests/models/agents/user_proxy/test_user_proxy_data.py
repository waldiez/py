"""Test waldiez.models.agents.user_proxy.user_proxy_data.*."""

from waldiez.models.agents.user_proxy.user_proxy_data import WaldieUserProxyData


def test_waldie_user_proxy_data() -> None:
    """Test WaldieUserProxyData."""
    user_proxy_data = WaldieUserProxyData()  # type: ignore
    assert user_proxy_data.human_input_mode == "ALWAYS"
