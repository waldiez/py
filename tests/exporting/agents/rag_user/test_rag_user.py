"""Test waldiez.exporting.agents.rag_user.rag_user.*."""

import os
from typing import Optional

from waldiez.exporting.agents.rag_user.rag_user import (
    get_rag_user_extras,
    get_rag_user_retrieve_config_str,
)
from waldiez.models import (
    WaldieRagUser,
    WaldieRagUserData,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserVectorDbConfig,
)

# pylint: disable=line-too-long


def _get_rag_user(
    local_path: Optional[str] = None,
    custom_embedding: Optional[str] = None,
    custom_token_count: Optional[str] = None,
    custom_text_split: Optional[str] = None,
) -> WaldieRagUser:
    """Get a RAG user agent."""
    return WaldieRagUser(
        id="wa-1",
        name="rag_user",
        description="A RAG user agent.",
        type="agent",
        agent_type="rag_user",
        tags=[],
        requirements=[],
        data=WaldieRagUserData(  # type: ignore
            model_ids=["wm-1"],
            retrieve_config=WaldieRagUserRetrieveConfig(  # type: ignore
                vector_db="chroma",
                db_config=WaldieRagUserVectorDbConfig(  # type: ignore
                    use_local_storage=local_path is not None,
                    local_storage_path=local_path,
                ),
                use_custom_text_split=custom_text_split is not None,
                custom_text_split_function=custom_text_split,
                use_custom_token_count=custom_token_count is not None,
                custom_token_count_function=custom_token_count,
                use_custom_embedding=custom_embedding is not None,
                embedding_function=custom_embedding,
            ),
        ),
    )


def test_get_rag_user_extras() -> None:
    """Test get_rag_user_extras()."""
    rag_user = _get_rag_user()
    agent_name = "rag_user"
    model_names = {"wm-1": "model_1"}
    before_agent_string, retrieve_arg, db_imports = get_rag_user_extras(
        agent=rag_user, agent_name=agent_name, model_names=model_names
    )
    assert before_agent_string == (
        "\nrag_user_client = chromadb.Client()\n"
        "try:\n"
        '    rag_user_client.get_collection("autogen-docs")\n'
        "except ValueError:\n"
        '    rag_user_client.create_collection("autogen-docs")\n'
    )
    assert (
        retrieve_arg
        == """
    retrieve_config={
        "task": "default",
        "model": "model_1",
        "customized_answer_prefix": "",
        "new_docs": True,
        "update_context": True,
        "get_or_create": False,
        "overwrite": False,
        "recursive": True,
        "chunk_mode": "multi_lines",
        "must_break_at_empty_line": True,
        "collection_name": "autogen-docs",
        "distance_threshold": -1,
        "vector_db": ChromaVectorDB(
            client=chromadb.Client(),
            embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2"),
        ),
    },"""
    )
    assert db_imports == {
        "from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction",
        "chromadb",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
    }


def test_get_rag_user_extras_with_custom_embedding_function() -> None:
    """Test get_rag_user_extras() with custom embedding function."""
    custom_embedding_function = """
def custom_embedding_function():
    return text.split
"""
    rag_user = _get_rag_user(custom_embedding=custom_embedding_function)
    agent_name = "rag_user"
    model_names = {"wm-1": "model_1"}
    before_agent_string, retrieve_arg, db_imports = get_rag_user_extras(
        agent=rag_user, agent_name=agent_name, model_names=model_names
    )
    assert (
        before_agent_string
        == """
rag_user_client = chromadb.Client()
try:
    rag_user_client.get_collection("autogen-docs")
except ValueError:
    rag_user_client.create_collection("autogen-docs")


def custom_embedding_function_rag_user():
    # type: () -> Callable[..., Any]
    return text.split

"""
    )
    assert (
        retrieve_arg
        == """
    retrieve_config={
        "task": "default",
        "model": "model_1",
        "customized_answer_prefix": "",
        "new_docs": True,
        "update_context": True,
        "get_or_create": False,
        "overwrite": False,
        "recursive": True,
        "chunk_mode": "multi_lines",
        "must_break_at_empty_line": True,
        "collection_name": "autogen-docs",
        "distance_threshold": -1,
        "vector_db": ChromaVectorDB(
            client=chromadb.Client(),
            embedding_function=custom_embedding_function_rag_user,
        ),
    },"""
    )
    assert db_imports == {
        "chromadb",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
    }


def test_get_rag_user_retrieve_config_str() -> None:
    """Test get_rag_user_retrieve_config_str()."""
    custom_token_count_function = """
def custom_token_count_function(text, model):
    return len(text.split())
"""  # nosemgrep  # nosec
    custom_text_split_function = """
def custom_text_split_function(text, max_tokens, chunk_mode, must_break_at_empty_line, overlap):
    return text.split()
"""
    custom_embedding_function = """
def custom_embedding_function():
    return text.split
"""
    rag_user = _get_rag_user(
        local_path="data",
        custom_embedding=custom_embedding_function,
        custom_token_count=custom_token_count_function,
        custom_text_split=custom_text_split_function,
    )
    agent_name = "rag_user"
    model_names = {"wm-1": "model_1"}
    rag_content_before_agent, retrieve_arg, db_imports = (
        get_rag_user_retrieve_config_str(
            agent=rag_user, agent_name=agent_name, model_names=model_names
        )
    )
    local_path = os.path.join(os.getcwd(), "data")
    assert (
        retrieve_arg
        == f"""{{
        "task": "default",
        "model": "model_1",
        "customized_answer_prefix": "",
        "new_docs": True,
        "update_context": True,
        "get_or_create": False,
        "overwrite": False,
        "recursive": True,
        "chunk_mode": "multi_lines",
        "must_break_at_empty_line": True,
        "collection_name": "autogen-docs",
        "distance_threshold": -1,
        "custom_token_count_function": "custom_token_count_function_rag_user",
        "custom_text_split_function": "custom_text_split_function_rag_user",
        "vector_db": ChromaVectorDB(
            client=chromadb.PersistentClient(path="{local_path}"),
            embedding_function=custom_embedding_function_rag_user,
        ),
    }}"""
    )
    assert db_imports == {
        "chromadb",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
    }
    local_path = os.path.join(os.getcwd(), "data")
    assert (
        rag_content_before_agent
        == f"""
rag_user_client = chromadb.PersistentClient(path="{local_path}")
try:
    rag_user_client.get_collection("autogen-docs")
except ValueError:
    rag_user_client.create_collection("autogen-docs")


def custom_embedding_function_rag_user():
    # type: () -> Callable[..., Any]
    return text.split


def custom_token_count_function_rag_user():
    # type: (str, str) -> int
    return len(text.split())


def custom_text_split_function_rag_user():
    # type: (str, int, str, bool, int) -> List[str]
    return text.split()

"""
    )
