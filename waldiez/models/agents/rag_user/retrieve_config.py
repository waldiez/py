"""RAG user agent retrieve config."""

from typing import Dict, List, Optional, Union

from pydantic import ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Literal, Self

from ...common import WaldiezBase, WaldiezMethodName, check_function
from .vector_db_config import WaldiezRagUserVectorDbConfig

WaldiezRagUserTask = Literal["code", "qa", "default"]
WaldiezRagUserVectorDb = Literal["chroma", "pgvector", "mongodb", "qdrant"]
WaldiezRagUserChunkMode = Literal["multi_lines", "one_line"]
WaldiezRagUserModels: Dict[WaldiezRagUserVectorDb, str] = {
    "chroma": "all-MiniLM-L6-v2",
    "mongodb": "all-MiniLM-L6-v2",
    "pgvector": "all-MiniLM-L6-v2",
    "qdrant": "BAAI/bge-small-en-v1.5",
}


class WaldiezRagUserRetrieveConfig(WaldiezBase):
    """RAG user agent.

    Attributes
    ----------
    task : Literal["code", "qa", "default"]
        The task of the retrieve chat.
        Possible values are 'code', 'qa' and 'default'.
        System prompt will be different for different tasks.
        The default value is default, which supports both code and qa,
        and provides source information in the end of the response.
    vector_db : Literal["chroma", "pgvector", "mongodb", "qdrant"]
        The vector db for the retrieve chat.
    db_config : Annotated[WaldiezVectorDbConfig, Field]
        The config for the selected vector db.
    docs_path : Optional[Union[str, List[str]]]
        The path to the docs directory. It can also be the path to a single
        file, the url to a single file or a list of directories, files and
        urls. Default is None, which works only if the collection is already
        created.
    new_docs : bool
        When True, only adds new documents to the collection; when False,
        updates existing documents and adds new ones. Default is True.
        Document id is used to determine if a document is new or existing.
        By default, the id is the hash value of the content.
    model : Optional[str]
        The model to use for the retrieve chat. If key not provided, a default
        model gpt-4 will be used.
    chunk_token_size : Optional[int]
        The chunk token size for the retrieve chat. If key not provided, a
        default size max_tokens * 0.4 will be used.
    context_max_tokens : Optional[int]
        The context max token size for the retrieve chat. If key not provided,
        a default size max_tokens * 0.8 will be used.
    chunk_mode : Optional[str]
        The chunk mode for the retrieve chat. Possible values are 'multi_lines'
        and 'one_line'. If key not provided, a default mode multi_lines will be
        used.
    must_break_at_empty_line : bool
        Chunk will only break at empty line if True. Default is True. If
        chunk_mode is 'one_line', this parameter will be ignored.
    use_custom_embedding: bool
        Whether to use custom embedding for the retrieve chat. Default is False.
        If True, the embedding_function should be provided.
    embedding_function : Optional[str]
        The embedding function for creating the vector db. Default is None,
        SentenceTransformer with the given embedding_model will be used. If
        you want to use OpenAI, Cohere, HuggingFace or other embedding
        functions, you can pass it here, follow the examples in
        https://docs.trychroma.com/guides/embeddings.
    customized_prompt : Optional[str]
        The customized prompt for the retrieve chat. Default is None.
    customized_answer_prefix : Optional[str]
        The customized answer prefix for the retrieve chat. Default is ''. If
        not '' and the customized_answer_prefix is not in the answer, Update
        Context will be triggered.
    update_context : bool
        If False, will not apply Update Context for interactive retrieval.
        Default is True.
    collection_name : Optional[str]
        The name of the collection. If key not provided, a default name
        autogen-docs will be used.
    get_or_create : bool
        Whether to get the collection if it exists. Default is False.
    overwrite : bool
        Whether to overwrite the collection if it exists. Default is False.
        Case 1. if the collection does not exist, create the collection. Case
        2. the collection exists, if overwrite is True, it will overwrite the
        collection. Case 3. the collection exists and overwrite is False, if
        get_or_create is True, it will get the collection, otherwise it raise a
        ValueError.
    use_custom_token_count: bool
        Whether to use custom token count function for the retrieve chat.
        Default is False. If True, the custom_token_count_function should be
        provided.
    custom_token_count_function : Optional[str]
        A custom function to count the number of tokens in a string. The
        function should take (text:str, model:str) as input and return the
        token_count(int). the retrieve_config['model'] will be passed in the
        function. Default is autogen.token_count_utils.count_token that uses
        tiktoken, which may not be accurate for non-OpenAI models.
    use_custom_text_split: bool
        Whether to use custom text split function for the retrieve chat. Default
        is False. If True, the custom_text_split_function should be provided.
    custom_text_split_function : Optional[str]
        A custom function to split a string into a list of strings. Default is
        None, will use the default function in autogen.retrieve_utils.
        split_text_to_chunks.
    custom_text_types : Optional[List[str]]
        A list of file types to be processed. Default is autogen.retrieve_utils.
        TEXT_FORMATS. This only applies to files under the directories in
        docs_path. Explicitly included files and urls will be chunked
        regardless of their types.
    recursive : bool
        Whether to search documents recursively in the docs_path. Default is
        True.
    distance_threshold : float
        The threshold for the distance score, only distance smaller than it
        will be returned. Will be ignored if < 0. Default is -1.
    embedding_function_string : Optional[str]
        The embedding function string (if use_custom_embedding is True).
    token_count_function_string : Optional[str]
        The token count function string (if use_custom_token_count is True).
    text_split_function_string : Optional[str]
        The text split function string (if use_custom_text_split is True).
    n_results: Optional[int]
        The number of results to return. Default is None, which will return all

    Functions
    ---------
    validate_custom_embedding_function
        Validate the custom embedding function.
    validate_custom_token_count_function
        Validate the custom token count function.
    validate_custom_text_split_function
        Validate the custom text split function.
    validate_rag_user_data
        Validate the RAG user data.
    """

    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        populate_by_name=True,
        frozen=False,
    )

    task: Annotated[
        WaldiezRagUserTask,
        Field(
            "default",
            title="Task",
            description=(
                "The task of the retrieve chat. "
                "Possible values are 'code', 'qa' and 'default'. "
                "System prompt will be different for different tasks. "
                "The default value is default, which supports both code, "
                "and qa and provides source information in the end of "
                "the response."
            ),
        ),
    ]
    vector_db: Annotated[
        WaldiezRagUserVectorDb,
        Field(
            "chroma",
            title="Vector DB",
            description="The vector db for the retrieve chat.",
        ),
    ]
    db_config: Annotated[
        WaldiezRagUserVectorDbConfig,
        Field(
            title="DB Config",
            description="The config for the selected vector db.",
            default_factory=WaldiezRagUserVectorDbConfig,
        ),
    ]
    docs_path: Annotated[
        Optional[Union[str, List[str]]],
        Field(
            default=None,
            title="Docs Path",
            description=(
                "The path to the docs directory. It can also be the path to "
                "a single file, the url to a single file or a list of "
                "directories, files and urls. Default is None, which works "
                "only if the collection is already created."
            ),
        ),
    ]
    new_docs: Annotated[
        bool,
        Field(
            default=True,
            title="New Docs",
            description=(
                "When True, only adds new documents to the collection; "
                "when False, updates existing documents and adds new ones. "
                "Default is True. Document id is used to determine if a "
                "document is new or existing. By default, the id is the "
                "hash value of the content."
            ),
        ),
    ]
    model: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Model",
            description=(
                "The model to use for the retrieve chat. If key not provided, "
                "we check for models linked to the agent."
            ),
        ),
    ]
    chunk_token_size: Annotated[
        Optional[int],
        Field(
            default=None,
            title="Chunk Token Size",
            description=(
                "The chunk token size for the retrieve chat.  "
                "If key not provided, a default size max_tokens * 0.4 "
                "will be used."
            ),
        ),
    ]
    context_max_tokens: Annotated[
        Optional[int],
        Field(
            default=None,
            title="Context Max Tokens",
            description=(
                "The context max token size for the retrieve chat. "
                "If key not provided, a default size max_tokens * 0.8 "
                "will be used."
            ),
        ),
    ]
    chunk_mode: Annotated[
        WaldiezRagUserChunkMode,
        Field(
            default="multi_lines",
            title="Chunk Mode",
            description=(
                "The chunk mode for the retrieve chat. Possible values are "
                "'multi_lines' and 'one_line'. If key not provided, "
                "a default mode multi_lines will be used."
            ),
        ),
    ]

    must_break_at_empty_line: Annotated[
        bool,
        Field(
            default=True,
            title="Must Break at Empty Line",
            description=(
                "Chunk will only break at empty line if True. Default is True. "
                "If chunk_mode is 'one_line', this parameter will be ignored."
            ),
        ),
    ]
    use_custom_embedding: Annotated[
        bool,
        Field(
            default=False,
            title="Use Custom Embedding",
            description=(
                "Whether to use custom embedding for the retrieve chat. "
                "Default is False. If True, the embedding_function should be "
                "provided."
            ),
        ),
    ]
    embedding_function: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Embedding Function",
            description=(
                "The embedding function for creating the vector db. "
                "Default is None, SentenceTransformer with the given "
                "embedding_model will be used. If you want to use OpenAI, "
                "Cohere, HuggingFace or other embedding functions, "
                "you can pass it here, follow the examples in "
                "https://docs.trychroma.com/guides/embeddings."
            ),
        ),
    ]
    customized_prompt: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Customized Prompt",
            description=(
                "The customized prompt for the retrieve chat. Default is None."
            ),
        ),
    ]
    customized_answer_prefix: Annotated[
        Optional[str],
        Field(
            default="",
            title="Customized Answer Prefix",
            description=(
                "The customized answer prefix for the retrieve chat. "
                "Default is ''. If not '' and the customized_answer_prefix is "
                "not in the answer, Update Context will be triggered."
            ),
        ),
    ]
    update_context: Annotated[
        bool,
        Field(
            default=True,
            title="Update Context",
            description=(
                "If False, will not apply Update Context for interactive "
                "retrieval. Default is True."
            ),
        ),
    ]
    collection_name: Annotated[
        str,
        Field(
            default="autogen-docs",
            title="Collection Name",
            description=(
                "The name of the collection. If key not provided, "
                "a default name autogen-docs will be used."
            ),
        ),
    ]
    get_or_create: Annotated[
        bool,
        Field(
            default=False,
            title="Get or Create",
            description=(
                "Whether to get the collection if it exists. Default is False."
            ),
        ),
    ]
    overwrite: Annotated[
        bool,
        Field(
            default=False,
            title="Overwrite",
            description=(
                "Whether to overwrite the collection if it exists. "
                "Default is False. "
                "Case 1. if the collection does not exist,"
                " create the collection. "
                "Case 2. the collection exists, if overwrite is True,"
                " it will overwrite the collection. "
                "Case 3. the collection exists and overwrite is False, if"
                " get_or_create is True, it will get the collection,"
                " otherwise it raise a ValueError."
            ),
        ),
    ]
    use_custom_token_count: Annotated[
        bool,
        Field(
            default=False,
            title="Use Custom Token Count",
            description=(
                "Whether to use custom token count function for the retrieve "
                "chat. Default is False. If True, the "
                "custom_token_count_function should be provided."
            ),
        ),
    ]
    custom_token_count_function: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Custom Token Count Function",
            description=(
                "A custom function to count the number of tokens in a string. "
                "The function should take (text:str, model:str) as input "
                "and return the token_count(int). the retrieve_config['model'] "
                "will be passed in the function. "
                "Default is autogen.token_count_utils.count_token that uses "
                "tiktoken, which may not be accurate for non-OpenAI models."
            ),
        ),
    ]
    use_custom_text_split: Annotated[
        bool,
        Field(
            default=False,
            title="Use Custom Text Split",
            description=(
                "Whether to use custom text split function for the retrieve "
                "chat. Default is False. If True, the "
                "custom_text_split_function should be provided."
            ),
        ),
    ]
    custom_text_split_function: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Custom Text Split Function",
            description=(
                "A custom function to split a string into a list of strings. "
                "Default is None, will use the default function in "
                "autogen.retrieve_utils.split_text_to_chunks."
            ),
        ),
    ]
    custom_text_types: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            title="Custom Text Types",
            description=(
                "A list of file types to be processed. "
                "Default is autogen.retrieve_utils.TEXT_FORMATS. "
                "This only applies to files under the directories in "
                "docs_path. Explicitly included files and urls will be "
                "chunked regardless of their types."
            ),
        ),
    ]
    recursive: Annotated[
        bool,
        Field(
            default=True,
            title="Recursive",
            description=(
                "Whether to search documents recursively in the docs_path. "
                "Default is True."
            ),
        ),
    ]
    distance_threshold: Annotated[
        float,
        Field(
            default=-1,
            title="Distance Threshold",
            description=(
                "The threshold for the distance score, only distance"
                " smaller than this will be returned. "
                "Will be ignored if < 0. Default is -1."
            ),
        ),
    ]
    n_results: Annotated[
        Optional[int],
        Field(
            default=None,
            title="Number of Results",
            description=(
                "The number of results to return. Default is None, "
                "which will return all."
                "Use None or <1 to return all results."
            ),
        ),
    ]
    _embedding_function_string: Optional[str] = None

    _token_count_function_string: Optional[str] = None

    _text_split_function_string: Optional[str] = None

    @property
    def embedding_function_string(self) -> Optional[str]:
        """Get the embedding function string.

        Returns
        -------
        Optional[str]
            The embedding function string.
        """
        return self._embedding_function_string

    @property
    def token_count_function_string(self) -> Optional[str]:
        """Get the token count function string.

        Returns
        -------
        Optional[str]
            The token count function string.
        """
        return self._token_count_function_string

    @property
    def text_split_function_string(self) -> Optional[str]:
        """Get the text split function string.

        Returns
        -------
        Optional[str]
            The text split function string.
        """
        return self._text_split_function_string

    def validate_custom_embedding_function(self) -> None:
        """Validate the custom embedding function.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.use_custom_embedding:
            if not self.embedding_function:
                raise ValueError(
                    "The embedding_function is required "
                    "if use_custom_embedding is True."
                )
            function_name: WaldiezMethodName = "custom_embedding_function"
            valid, error_or_content = check_function(
                self.embedding_function, function_name
            )
            if not valid:
                raise ValueError(error_or_content)
            self._embedding_function_string = error_or_content

    def validate_custom_token_count_function(self) -> None:
        """Validate the custom token count function.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.use_custom_token_count:
            if not self.custom_token_count_function:
                raise ValueError(
                    "The custom_token_count_function is required "
                    "if use_custom_token_count is True."
                )
            function_name: WaldiezMethodName = "custom_token_count_function"
            valid, error_or_content = check_function(
                self.custom_token_count_function, function_name
            )
            if not valid:
                raise ValueError(error_or_content)
            self._token_count_function_string = error_or_content

    def validate_custom_text_split_function(self) -> None:
        """Validate the custom text split function.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.use_custom_text_split:
            if not self.custom_text_split_function:
                raise ValueError(
                    "The custom_text_split_function is required "
                    "if use_custom_text_split is True."
                )
            function_name: WaldiezMethodName = "custom_text_split_function"
            valid, error_or_content = check_function(
                self.custom_text_split_function, function_name
            )
            if not valid:
                raise ValueError(error_or_content)
            self._text_split_function_string = error_or_content

    @model_validator(mode="after")
    def validate_rag_user_data(self) -> Self:
        """Validate the RAG user data.

        Raises
        ------
        ValueError
            If the validation fails.

        Returns
        -------
        WaldiezRagUserData
            The validated RAG user data.
        """
        self.validate_custom_embedding_function()
        self.validate_custom_token_count_function()
        self.validate_custom_text_split_function()
        if not self.db_config.model:
            self.db_config.model = WaldiezRagUserModels[self.vector_db]
        if isinstance(self.n_results, int) and self.n_results < 1:
            self.n_results = None
        return self
