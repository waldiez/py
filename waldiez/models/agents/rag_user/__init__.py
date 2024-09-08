"""RAG user agent.
# pylint: disable=line-too-long
It extends a user agent and has RAG related parameters.
"""

from .rag_user import WaldieRagUser
from .rag_user_data import WaldieRagUserData
from .retrieve_config import (
    WaldieRagUserChunkMode,
    WaldieRagUserModels,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserTask,
    WaldieRagUserVectorDb,
)
from .vector_db_config import WaldieRagUserVectorDbConfig

__all__ = [
    "WaldieRagUser",
    "WaldieRagUserData",
    "WaldieRagUserModels",
    "WaldieRagUserVectorDb",
    "WaldieRagUserChunkMode",
    "WaldieRagUserRetrieveConfig",
    "WaldieRagUserTask",
    "WaldieRagUserVectorDbConfig",
]
