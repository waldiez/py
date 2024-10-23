"""Test waldiez.exporting.agents.rag_user.vector_db.*."""

import os

from waldiez.exporting.agents.rag_user.vector_db import (
    get_rag_user_vector_db_string,
)
from waldiez.models import (
    WaldiezRagUser,
    WaldiezRagUserData,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserVectorDbConfig,
)

# pylint: disable=line-too-long


def test_get_rag_user_vector_db_string_chroma() -> None:
    """Test get_rag_user_vector_db_string with ChromaVectorDB."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="chroma",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url=None,
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    local_path = os.path.join(os.getcwd(), "local_storage_path")
    assert before == (
        f'\nrag_user_client = chromadb.PersistentClient(path="{local_path}")\n'
        "try:\n"
        '    rag_user_client.get_collection("collection_name")\n'
        "except ValueError:\n"
        '    rag_user_client.create_collection("collection_name")\n'
    )
    assert arg == (
        "ChromaVectorDB(\n"
        f'            client=chromadb.PersistentClient(path="{local_path}"),\n'
        '            embedding_function=SentenceTransformerEmbeddingFunction(model_name="model"),\n'
        "        )"
    )
    assert imports == {
        "from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
        "chromadb",
    }


def test_get_rag_user_vector_db_string_qdrant() -> None:
    """Test get_rag_user_vector_db_string with QdrantVectorDB."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="qdrant",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url=None,
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    assert before == ""
    assert arg == (
        "QdrantVectorDB(\n"
        '            client=QdrantClient(location=":memory:"),\n'
        '            embedding_function=FastEmbedEmbeddingFunction(model_name="model"),\n'
        "        )"
    )
    assert imports == {
        "from autogen.agentchat.contrib.vectordb.qdrant import FastEmbedEmbeddingFunction",
        "from autogen.agentchat.contrib.vectordb.qdrant import QdrantVectorDB",
        "from qdrant_client import QdrantClient",
    }


def test_get_rag_user_vector_db_string_mongodb() -> None:
    """Test get_rag_user_vector_db_string with MongoDBAtlasVectorDB."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="mongodb",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url="connection_url",
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    assert before == ""
    assert arg == (
        "MongoDBAtlasVectorDB(\n"
        '            connection_string="connection_url",\n'
        '            embedding_function=SentenceTransformer("model").encode,\n'
        "        )"
    )
    assert imports == {
        "from autogen.agentchat.contrib.vectordb.mongo import MongoDBAtlasVectorDB",
        "from sentence_transformers import SentenceTransformer",
    }


def test_get_rag_user_vector_db_string_pgvector() -> None:
    """Test get_rag_user_vector_db_string with PGVectorDB."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="pgvector",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url="connection_url",
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    assert before == ""
    assert arg == (
        "PGVectorDB(\n"
        '            client=psycopg.connect("connection_url"),\n'
        '            embedding_function=SentenceTransformer("model").encode,\n'
        "        )"
    )
    assert imports == {
        "from autogen.agentchat.contrib.vectordb.pgvector import PGVectorDB",
        "from sentence_transformers import SentenceTransformer",
        "psycopg",
    }


def test_get_rag_user_vector_db_string_custom_embedding() -> None:
    """Test get_rag_user_vector_db_string with custom embedding."""
    # Given
    custom_embedding = (
        "def custom_embedding_function():\n"
        "    # pylint: disable=import-outside-toplevel\n"
        "    from sentence_transformers import SentenceTransformer\n"
        '    return SentenceTransformer("model").encode\n'
    )
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="description",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="chroma",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url=None,
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=True,
                embedding_function=custom_embedding,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    local_path = os.path.join(os.getcwd(), "local_storage_path")
    assert (
        before
        == f"""
rag_user_client = chromadb.PersistentClient(path="{local_path}")
try:
    rag_user_client.get_collection("collection_name")
except ValueError:
    rag_user_client.create_collection("collection_name")


def custom_embedding_function_rag_user():
    # type: () -> Callable[..., Any]
    # pylint: disable=import-outside-toplevel
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("model").encode

"""
    )
    assert arg == (
        "ChromaVectorDB(\n"
        f'            client=chromadb.PersistentClient(path="{local_path}"),\n'
        "            embedding_function=custom_embedding_function_rag_user,\n"
        "        )"
    )
    assert imports == {
        "chromadb",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
    }


def test_get_rag_user_vector_db_string_with_metadata() -> None:
    """Test get_rag_user_vector_db_string with metadata."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="rag user description",
        tags=[],
        requirements=[],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="chroma",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url=None,
                    use_memory=True,
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                    metadata={
                        "hnsw:space": "ip",
                        "hnsw:construction_ef": 30,
                        "hnsw:M": 32,
                        "other": "4.2",
                    },
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    before, arg, imports = get_rag_user_vector_db_string(rag_user, agent_name)
    # Then
    local_path = os.path.join(os.getcwd(), "local_storage_path")
    assert (
        before
        == f"""
rag_user_client = chromadb.PersistentClient(path="{local_path}")
try:
    rag_user_client.get_collection("collection_name")
except ValueError:
    rag_user_client.create_collection("collection_name")
"""
    )
    assert arg == (
        "ChromaVectorDB(\n"
        f'            client=chromadb.PersistentClient(path="{local_path}"),\n'
        '            embedding_function=SentenceTransformerEmbeddingFunction(model_name="model"),\n'
        "            metadata={\n"
        '                "hnsw:space": "ip",\n'
        '                "hnsw:construction_ef": 30,\n'
        '                "hnsw:M": 32,\n'
        '                "other": 4.2,\n'
        "            },\n"
        "        )"
    )
    assert imports == {
        "chromadb",
        "from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB",
        "from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction",
    }
