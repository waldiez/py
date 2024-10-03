"""Test waldiez.models.agents.rag_user.retrieve_config.*."""

import pytest

from waldiez.models.agents.rag_user.retrieve_config import (
    WaldieRagUserRetrieveConfig,
)
from waldiez.models.agents.rag_user.vector_db_config import (
    WaldieRagUserVectorDbConfig,
)


def test_waldie_rag_user_retrieve_config() -> None:
    """Test WaldieRagUserRetrieveConfig."""
    retrieve_config = WaldieRagUserRetrieveConfig(
        task="default",
        vector_db="chroma",
        db_config=WaldieRagUserVectorDbConfig(
            model="all-MiniLM-L6-v2",
            use_memory=True,
            use_local_storage=False,
            local_storage_path=None,
            connection_url=None,
            wait_until_index_ready=None,
            wait_until_document_ready=None,
            metadata={},
        ),
        docs_path=None,
        new_docs=True,
        model=None,
        chunk_token_size=None,
        context_max_tokens=None,
        chunk_mode="multi_lines",
        must_break_at_empty_line=True,
        use_custom_embedding=False,
        embedding_function=None,
        customized_prompt=None,
        customized_answer_prefix="",
        update_context=True,
        collection_name="autogen-docs",
        get_or_create=False,
        overwrite=False,
        use_custom_token_count=False,
        custom_token_count_function=None,
        use_custom_text_split=False,
        custom_text_split_function=None,
        custom_text_types=None,
        recursive=False,
        distance_threshold=-1.0,
        n_results=-1,
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.text_split_function_string is None
    assert retrieve_config.token_count_function_string is None


def test_waldie_rag_user_retrieve_config_custom_embedding() -> None:
    """Test WaldieRagUserRetrieveConfig with custom embedding."""
    embedding_function = """
def custom_embedding_function():
    return list
"""
    retrieve_config = WaldieRagUserRetrieveConfig(  # type: ignore
        use_custom_embedding=True,
        embedding_function=embedding_function,
    )
    assert retrieve_config.embedding_function_string is not None
    assert (
        retrieve_config.embedding_function_string
        == "    # type: () -> Callable[..., Any]\n    return list"
    )
    assert retrieve_config.text_split_function_string is None
    assert retrieve_config.token_count_function_string is None

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore
            use_custom_embedding=True,
            embedding_function=None,
        )

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore
            use_custom_embedding=True,
            embedding_function="def something():\n   return list",
        )


def test_waldie_rag_user_retrieve_config_custom_token_count() -> None:
    """Test WaldieRagUserRetrieveConfig with custom token count."""
    token_count_function = """
def custom_token_count_function(text, model):
    return 0
"""  # nosemgrep # nosec
    retrieve_config = WaldieRagUserRetrieveConfig(  # type: ignore
        use_custom_token_count=True,
        custom_token_count_function=token_count_function,
    )
    assert retrieve_config.token_count_function_string is not None
    assert (
        retrieve_config.token_count_function_string
        == "    # type: (str, str) -> int\n    return 0"  # nosemgrep # nosec
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.text_split_function_string is None

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore
            use_custom_token_count=True,
            custom_token_count_function=None,
        )

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore  # nosemgrep # nosec
            use_custom_token_count=True,
            custom_token_count_function="def something():\n    return 0",
        )


# pylint: disable=line-too-long
def test_waldie_rag_user_retrieve_config_custom_text_split() -> None:
    """Test WaldieRagUserRetrieveConfig with custom text split."""
    text_split_function = """
def custom_text_split_function(text, max_tokens, chunk_mode, must_break_at_empty_line, overlap):
    return [text]
"""
    retrieve_config = WaldieRagUserRetrieveConfig(  # type: ignore
        use_custom_text_split=True,
        custom_text_split_function=text_split_function,
    )
    assert retrieve_config.text_split_function_string is not None
    assert (
        retrieve_config.text_split_function_string
        == "    # type: (str, int, str, bool, int) -> List[str]\n    return [text]"
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.token_count_function_string is None

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore
            use_custom_text_split=True,
            custom_text_split_function=None,
        )

    with pytest.raises(ValueError):
        WaldieRagUserRetrieveConfig(  # type: ignore
            use_custom_text_split=True,
            custom_text_split_function="def something():\n    return []",
        )
