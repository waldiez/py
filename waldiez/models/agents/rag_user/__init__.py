"""RAG user agent.
# pylint: disable=line-too-long
It extends a user agent and has RAG related parameters.
"""

from .rag_user import WaldiezRagUser
from .rag_user_data import WaldiezRagUserData
from .retrieve_config import (
    WaldiezRagUserChunkMode,
    WaldiezRagUserModels,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserTask,
    WaldiezRagUserVectorDb,
)
from .vector_db_config import WaldiezRagUserVectorDbConfig

__all__ = [
    "WaldiezRagUser",
    "WaldiezRagUserData",
    "WaldiezRagUserModels",
    "WaldiezRagUserVectorDb",
    "WaldiezRagUserChunkMode",
    "WaldiezRagUserRetrieveConfig",
    "WaldiezRagUserTask",
    "WaldiezRagUserVectorDbConfig",
]
