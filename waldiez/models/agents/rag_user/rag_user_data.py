"""Waldie RAG user agent data."""

from pydantic import Field
from typing_extensions import Annotated

from ..user_proxy import WaldieUserProxyData
from .retrieve_config import WaldieRagUserRetrieveConfig


class WaldieRagUserData(WaldieUserProxyData):
    """RAG user agent data.

    The data for a RAG user agent.

    Attributes
    ----------
    use_message_generator: bool
        Whether to use the message generator in user's chats. Defaults to False.
    retrieve_config : WaldieRagUserRetrieveConfig
        The RAG user agent's retrieve config.

    """

    use_message_generator: Annotated[
        bool,
        Field(
            title="Use Message Generator",
            description="Whether to use the message generator in user's chats.",
            default=False,
            alias="useMessageGenerator",
        ),
    ]
    retrieve_config: Annotated[
        WaldieRagUserRetrieveConfig,
        Field(
            title="Retrieve Config",
            description="The RAG user agent's retrieve config",
            default_factory=WaldieRagUserRetrieveConfig,
            alias="retrieveConfig",
        ),
    ]
