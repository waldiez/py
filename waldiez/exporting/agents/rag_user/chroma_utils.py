"""Get chroma db related imports and content."""

from typing import Set, Tuple

from waldiez.models import WaldieRagUser


def _get_chroma_client_string(agent: WaldieRagUser) -> Tuple[str, str]:
    """Get the ChromaVectorDB client string.

    Parameters
    ----------
    agent : WaldieRagUser
        The agent.
    agent_name : str
        The agent's name.

    Returns
    -------
    Tuple[str, str]
        The 'client' and what to import.
    """
    # TODO: also check `connection_url` (chroma in client-server mode)
    to_import = "chromadb"
    client_str = "chromadb."
    if (
        agent.retrieve_config.db_config.use_local_storage
        and agent.retrieve_config.db_config.local_storage_path is not None
    ):
        local_path = agent.retrieve_config.db_config.local_storage_path
        client_str += f'PersistentClient(path="{local_path}")'
    else:
        client_str += "Client()"
    return client_str, to_import


def _get_chroma_embedding_function_string(
    agent: WaldieRagUser, agent_name: str
) -> Tuple[str, str, str]:
    """Get the ChromaVectorDB embedding function string.

    Parameters
    ----------
    agent : WaldieRagUser
        The agent.
    agent_name : str
        The agent's name.

    Returns
    -------
    Tuple[str, str, str]
        The 'embedding_function', the import and the custom embedding function.
    """
    to_import = ""
    embedding_function_arg = ""
    embedding_function_body = ""
    vector_db_model = agent.retrieve_config.db_config.model
    if not agent.retrieve_config.use_custom_embedding:
        to_import = (
            "from chromadb.utils.embedding_functions."
            "sentence_transformer_embedding_function import "
            "SentenceTransformerEmbeddingFunction"
        )
        embedding_function_arg = "SentenceTransformerEmbeddingFunction("
        embedding_function_arg += f'model_name="{vector_db_model}")'
    else:
        embedding_function_arg = f"custom_embedding_function_{agent_name}"
        embedding_function_body = (
            f"\ndef custom_embedding_function_{agent_name}():\n"
            f"{agent.retrieve_config.embedding_function_string}\n"
        )

    return embedding_function_arg, to_import, embedding_function_body


def get_chroma_db_args(
    agent: WaldieRagUser, agent_name: str
) -> Tuple[str, Set[str], str]:
    """Get the 'kwargs to use for ChromaVectorDB.

    Parameters
    ----------
    agent : WaldieRagUser
        The agent.
    agent_name : str
        The agent's name.

    Returns
    -------
    Tuple[str, Set[str], str]
        The 'kwargs' string, the imports and the custom embedding function.
    """
    client_str, to_import_client = _get_chroma_client_string(agent)
    embedding_function_arg, to_import_embedding, embedding_function_body = (
        _get_chroma_embedding_function_string(agent, agent_name)
    )
    to_import = {to_import_client}
    if to_import_embedding:
        to_import.add(to_import_embedding)
    # kwargs: Dict[str, str] = {
    kwarg_string = (
        f"            client={client_str},\n"
        f"            embedding_function={embedding_function_arg},\n"
    )
    return kwarg_string, to_import, embedding_function_body
