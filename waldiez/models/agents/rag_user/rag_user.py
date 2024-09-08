# pylint: disable=line-too-long
"""RAG user agent.
It extends a user agent and has RAG related parameters (`retrieve_config`).
"""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import WaldieAgent
from .rag_user_data import WaldieRagUserData
from .retrieve_config import WaldieRagUserRetrieveConfig


class WaldieRagUser(WaldieAgent):
    """RAG user agent.

    It extends a user agent and has RAG related parameters.

    Attributes
    ----------
    agent_type : Literal["rag_user"]
        The agent type: 'rag_user' for a RAG user agent.
    data : WaldieRagUserData
        The RAG user agent's data.
        See `WaldieRagUserData` for more info.
    retrieve_config : WaldieRagUserRetrieveConfig
        The RAG user agent's retrieve config.
    """

    agent_type: Annotated[
        Literal["rag_user"],
        Field(
            "rag_user",
            title="Agent type",
            description="The agent type: 'rag_user' for a RAG user agent",
            alias="agentType",
        ),
    ]

    data: Annotated[
        WaldieRagUserData,
        Field(
            title="Data",
            description="The RAG user agent's data",
            default_factory=WaldieRagUserData,
        ),
    ]

    @property
    def retrieve_config(self) -> WaldieRagUserRetrieveConfig:
        """Get the retrieve config.

        Returns
        -------
        WaldieRagUserRetrieveConfig
            The RAG user agent's retrieve config.
        """
        return self.data.retrieve_config
