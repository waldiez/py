"""Test waldiez.exporting.agents.agent.*."""

from typing import List

from waldiez.exporting.agents.agent import export_agent, get_agent_class_name
from waldiez.models import (
    WaldieAgent,
    WaldieAgentCodeExecutionConfig,
    WaldieAgentLinkedSkill,
    WaldieAgentTeachability,
    WaldieAgentTerminationMessage,
    WaldieAssistant,
    WaldieAssistantData,
    WaldieGroupManager,
    WaldieGroupManagerData,
    WaldieGroupManagerSpeakers,
    WaldieModel,
    WaldieRagUser,
    WaldieRagUserData,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserVectorDbConfig,
    WaldieSkill,
    WaldieSkillData,
    WaldieUserProxy,
)

# pylint: disable=line-too-long


def test_get_agent_class_name() -> None:
    """Test get_agent_class_name()."""
    # Given
    user_proxy = WaldieUserProxy(  # type: ignore
        id="wa-1",
        name="user_proxy",
    )
    assistant = WaldieAssistant(  # type: ignore
        id="wa-2",
        name="assistant",
    )
    group_manager = WaldieGroupManager(  # type: ignore
        id="wa-3",
        name="group_manager",
    )
    rag_user = WaldieRagUser(  # type: ignore
        id="wa-4",
        name="rag_user",
    )
    # When
    user_proxy_class_name = get_agent_class_name(user_proxy)
    assistant_class_name = get_agent_class_name(assistant)
    group_manager_class_name = get_agent_class_name(group_manager)
    rag_user_class_name = get_agent_class_name(rag_user)
    # Then
    assert user_proxy_class_name == "UserProxyAgent"
    assert assistant_class_name == "AssistantAgent"
    assert group_manager_class_name == "GroupChatManager"
    assert rag_user_class_name == "RetrieveUserProxyAgent"


def test_export_agent() -> None:
    """Test export_agent()."""
    # Given
    user_proxy = WaldieUserProxy(  # type: ignore
        id="wa-1",
        name="user_proxy",
        agent_type="user",
    )
    agent_names = {"wa-1": "user_proxy"}
    model_names = {"wm-1": "model_1"}
    skill_names = {"ws-1": "skill_1"}
    all_skills: List[WaldieSkill] = []
    all_models: List[WaldieModel] = []
    group_chat_members: List[WaldieAgent] = []
    # When
    (
        agent_string,
        after_agent,
        imports,
    ) = export_agent(
        agent=user_proxy,
        agent_names=agent_names,
        model_names=model_names,
        skill_names=skill_names,
        all_models=all_models,
        all_skills=all_skills,
        group_chat_members=group_chat_members,
    )
    # Then
    assert (
        agent_string
        == """user_proxy = UserProxyAgent(
    name="user_proxy",
    description="Agent's description",
    llm_config=False,
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=None,
    default_auto_reply=None,
    code_execution_config=False,
    is_termination_msg=None,
)
"""
    )
    assert after_agent == ""
    assert imports == {"from autogen import UserProxyAgent"}


def test_export_agent_custom_termination() -> None:
    """Test export_agent() with custom termination message."""
    # Given
    message_content = (
        "def is_termination_message(message):\n"
        '    return "goodbye" in message.lower()\n'
    )
    assistant = WaldieAssistant(  # type: ignore
        id="wa-1",
        name="assistant",
        description="Agent's description",
        agent_type="assistant",
        data=WaldieAssistantData(  # type: ignore
            termination=WaldieAgentTerminationMessage(
                type="method",
                keywords=[],
                criterion=None,
                method_content=message_content,
            ),
        ),
    )
    agent_names = {"wa-1": "assistant"}
    model_names = {"wm-1": "model_1"}
    skill_names = {"ws-1": "skill_1"}
    all_skills: List[WaldieSkill] = []
    all_models: List[WaldieModel] = []
    group_chat_members: List[WaldieAgent] = []
    # When
    (
        agent_string,
        after_agent,
        imports,
    ) = export_agent(
        agent=assistant,
        agent_names=agent_names,
        model_names=model_names,
        skill_names=skill_names,
        all_skills=all_skills,
        all_models=all_models,
        group_chat_members=group_chat_members,
    )
    # Then
    assert (
        agent_string
        == """

def is_termination_message_assistant(message):
    # type: (dict) -> bool
    return "goodbye" in message.lower()


assistant = AssistantAgent(
    name="assistant",
    description="Agent's description",
    llm_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=None,
    default_auto_reply=None,
    code_execution_config=False,
    is_termination_msg=is_termination_message_assistant,
)
"""
    )
    assert after_agent == ""
    assert imports == {"from autogen import AssistantAgent"}


def test_export_group_manager() -> None:
    """Test export_agent() with group manager."""
    user = WaldieUserProxy(  # type: ignore
        id="wa-1",
        name="user",
    )
    assistant = WaldieAssistant(  # type: ignore
        id="wa-2",
        name="assistant",
    )
    custom_speaker_selection = (
        "def custom_speaker_selection(last_speaker, groupchat):\n"
        "    return last_speaker"
    )
    manager = WaldieGroupManager(  # type: ignore
        id="wa-3",
        name="group_manager",
        data=WaldieGroupManagerData(  # type: ignore
            agent_default_auto_reply="I am the group manager.",
            enable_clear_history=True,
            speakers=WaldieGroupManagerSpeakers(
                selection_method="custom",
                selection_custom_method=custom_speaker_selection,
                max_retries_for_selecting=3,
                selection_mode="transition",
                allow_repeat=["wa-1", "wa-2"],
                transitions_type="allowed",
                allowed_or_disallowed_transitions={"wa-1": ["wa-2"]},
            ),
        ),
    )
    agent_names = {"wa-1": "user", "wa-2": "assistant", "wa-3": "group_manager"}
    model_names = {"wm-1": "model_1"}
    skill_names = {"ws-1": "skill_1"}
    all_skills: List[WaldieSkill] = []
    all_models: List[WaldieModel] = []
    group_chat_members: List[WaldieAgent] = [user, assistant]
    # When
    (
        agent_string,
        after_agent,
        imports,
    ) = export_agent(
        agent=manager,
        agent_names=agent_names,
        model_names=model_names,
        skill_names=skill_names,
        all_models=all_models,
        all_skills=all_skills,
        group_chat_members=group_chat_members,
    )
    # Then
    assert (
        agent_string
        == """def custom_speaker_selection_method_group_manager(
    last_speaker,
    groupchat,
):
    # type: (ConversableAgent, GroupChat) -> Union[Agent, str, None]
    return last_speaker


group_manager_group_chat = GroupChat(
    agents=[user, assistant],
    enable_clear_history=True,
    send_introductions=False,
    messages=[],
    max_retries_for_selecting_speaker=3,
    speaker_selection_method=custom_speaker_selection_method_group_manager,
    allowed_or_disallowed_speaker_transitions={
        user: [
            assistant
        ]
    },
    speaker_transitions_type="allowed",
)


group_manager = GroupChatManager(
    name="group_manager",
    description="Agent's description",
    llm_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=None,
    default_auto_reply="I am the group manager.",
    code_execution_config=False,
    is_termination_msg=None,
    groupchat=group_manager_group_chat,
)
"""
    )
    assert after_agent == ""
    assert imports == {
        "from autogen import GroupChat",
        "from autogen import GroupChatManager",
    }


def test_export_rag_user() -> None:
    """Test export_agent() RAG user."""
    user = WaldieUserProxy(  # type: ignore
        id="wa-1",
        name="user",
    )
    assistant = WaldieAssistant(  # type: ignore
        id="wa-2",
        name="assistant",
    )
    custom_embedding = (
        "def custom_embedding_function():\n"
        "    # pylint: disable=import-outside-toplevel\n"
        "    from sentence_transformers import SentenceTransformer\n"
        '    return SentenceTransformer("model").encode\n'
    )
    rag_user = WaldieRagUser(  # type: ignore
        id="wa-3",
        name="rag_user",
        data=WaldieRagUserData(
            agent_default_auto_reply="I am the RAG user.",
            human_input_mode="ALWAYS",
            system_message="Do stuff using docs.",
            max_tokens=100,
            max_consecutive_auto_reply=2,
            model_ids=[],
            skills=[],
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                keywords=["goodbye"],
                criterion="exact",
                method_content=None,
            ),
            code_execution_config=False,
            nested_chats=[],
            retrieve_config=WaldieRagUserRetrieveConfig(
                task="default",
                vector_db="qdrant",
                docs_path=None,
                new_docs=True,
                model=None,
                chunk_mode="multi_lines",
                chunk_token_size=512,
                collection_name="autogen-docs",
                context_max_tokens=100,
                must_break_at_empty_line=True,
                use_custom_embedding=True,
                embedding_function=custom_embedding,
                use_custom_token_count=False,
                custom_token_count_function=None,
                use_custom_text_split=False,
                custom_text_split_function=None,
                custom_text_types=None,
                customized_prompt=None,
                customized_answer_prefix=None,
                update_context=True,
                get_or_create=True,
                overwrite=False,
                recursive=True,
                distance_threshold=-1,
                n_results=None,
                db_config=WaldieRagUserVectorDbConfig(
                    model=None,
                    use_local_storage=False,
                    use_memory=True,
                    connection_url=None,
                    local_storage_path=None,
                    wait_until_document_ready=10,
                    wait_until_index_ready=0.5,
                    metadata={
                        "hnsw:space": "ip",
                        "hnsw:construction_ef": 30,
                        "hnsw:M": 32,
                    },
                ),
            ),
        ),
    )
    agent_names = {"wa-1": "user", "wa-2": "assistant", "wa-3": "rag_user"}
    model_names = {"wm-1": "model_1"}
    skill_names = {"ws-1": "skill_1"}
    all_skills: List[WaldieSkill] = [
        WaldieSkill(  # type: ignore
            id="ws-1",
            name="skill_1",
            description="Skill's description",
            data=WaldieSkillData(
                content="def skill_1():\n    return 'skill_1'",
                secrets={},
            ),
        )
    ]
    all_models: List[WaldieModel] = []
    group_chat_members: List[WaldieAgent] = [user, assistant]
    # When
    (
        agent_string,
        after_agent,
        imports,
    ) = export_agent(
        agent=rag_user,
        agent_names=agent_names,
        model_names=model_names,
        skill_names=skill_names,
        all_models=all_models,
        all_skills=all_skills,
        group_chat_members=group_chat_members,
    )
    # Then
    assert (
        agent_string
        == """

def custom_embedding_function_rag_user():
    # type: () -> Callable[..., Any]
    # pylint: disable=import-outside-toplevel
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("model").encode


rag_user = RetrieveUserProxyAgent(
    name="rag_user",
    description="Agent's description",
    llm_config=False,
    system_message="Do stuff using docs.",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=2,
    default_auto_reply="I am the RAG user.",
    code_execution_config=False,
    is_termination_msg=lambda x: any(x.get("content", "") == keyword for keyword in ["goodbye"]),
    retrieve_config={
        "task": "default",
        "model": "BAAI/bge-small-en-v1.5",
        "chunk_token_size": 512,
        "context_max_tokens": 100,
        "new_docs": True,
        "update_context": True,
        "get_or_create": True,
        "overwrite": False,
        "recursive": True,
        "chunk_mode": "multi_lines",
        "must_break_at_empty_line": True,
        "collection_name": "autogen-docs",
        "distance_threshold": -1.0,
        "vector_db": QdrantVectorDB(
            client=QdrantClient(location=":memory:"),
            embedding_function=custom_embedding_function_rag_user,
            metadata={
                "hnsw:space": "ip",
                "hnsw:construction_ef": 30,
                "hnsw:M": 32,
            },
        ),
    },
)
"""
    )
    assert after_agent == ""
    assert imports == {
        "from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent",
        "from autogen.agentchat.contrib.vectordb.qdrant import QdrantVectorDB",
        "from qdrant_client import QdrantClient",
    }


def test_export_agent_with_skills_and_code_execution() -> None:
    """Test export_agent() with skills."""
    user = WaldieUserProxy(  # type: ignore
        id="wa-1",
        name="user",
    )
    assistant_skill = WaldieSkill(  # type: ignore
        id="ws-1",
        name="skill_1",
        description="Skill's description",
        data=WaldieSkillData(
            content="def skill_1():\n    return 'skill_1'",
            secrets={},
        ),
    )
    assistant = WaldieAssistant(  # type: ignore
        id="wa-2",
        name="assistant",
        data=WaldieAssistantData(  # type: ignore
            code_execution_config=WaldieAgentCodeExecutionConfig(
                work_dir="coding",
                use_docker=False,
                timeout=10,
                last_n_messages=5,
                functions=["ws-1"],
            ),
            skills=[WaldieAgentLinkedSkill(id="ws-1", executor_id="wa-1")],
        ),
    )
    agent_names = {"wa-1": "user", "wa-2": "assistant"}
    model_names = {"wm-1": "model_1"}
    skill_names = {"ws-1": "skill_1"}
    all_skills: List[WaldieSkill] = [assistant_skill]
    all_models: List[WaldieModel] = []
    group_chat_members: List[WaldieAgent] = [user, assistant]
    # When
    (
        agent_string,
        after_agent,
        imports,
    ) = export_agent(
        agent=assistant,
        agent_names=agent_names,
        model_names=model_names,
        skill_names=skill_names,
        all_models=all_models,
        all_skills=all_skills,
        group_chat_members=group_chat_members,
    )
    # Then
    assert (
        agent_string
        == """assistant_executor = LocalCommandLineCodeExecutor(
    work_dir="coding",
    timeout=10.0,
    functions=[skill_1],
)


assistant = AssistantAgent(
    name="assistant",
    description="Agent's description",
    llm_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=None,
    default_auto_reply=None,
    code_execution_config={"executor": assistant_executor},
    is_termination_msg=None,
)
"""
    )
    assert (
        after_agent
        == """
register_function(
    skill_1,
    caller=assistant,
    executor=user,
    name="skill_1",
    description="Skill's description",
)


"""
    )
    assert imports == {
        "from autogen import register_function",
        "from autogen import AssistantAgent",
        "from autogen.coding import LocalCommandLineCodeExecutor",
    }
