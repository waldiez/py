"""Helpers for getting a flow."""

from typing import List

from waldiez.models import (
    WaldiezAgentCodeExecutionConfig,
    WaldiezAgentLinkedSkill,
    WaldiezAgentNestedChat,
    WaldiezAgentNestedChatMessage,
    WaldiezAgents,
    WaldiezAgentTeachability,
    WaldiezAgentTerminationMessage,
    WaldiezAssistant,
    WaldiezAssistantData,
    WaldiezChat,
    WaldiezChatData,
    WaldiezChatMessage,
    WaldiezChatNested,
    WaldiezChatSummary,
    WaldiezFlow,
    WaldiezFlowData,
    WaldiezGroupManager,
    WaldiezGroupManagerData,
    WaldiezGroupManagerSpeakers,
    WaldiezModel,
    WaldiezModelData,
    WaldiezModelPrice,
    WaldiezRagUser,
    WaldiezRagUserData,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserVectorDbConfig,
    WaldiezSkill,
    WaldiezSkillData,
    WaldiezUserProxy,
    WaldiezUserProxyData,
)


def get_model(model_id: str = "wm-1") -> WaldiezModel:
    """Get a WaldiezModel.

    Parameters
    ----------
    model_id : str, optional
        The model ID, by default "wm-1"

    Returns
    -------
    WaldiezModel
        A WaldiezModel instance
    """
    return WaldiezModel(
        id=model_id,
        name="model_name",
        description="Model Description",
        tags=["model"],
        requirements=[],
        type="model",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezModelData(
            api_type="groq",  # to cover additional requirements
            api_key="api_key",
            api_version="2020-05-03",
            base_url="https://example.com/v1",
            price=WaldiezModelPrice(
                prompt_price_per_1k=0.06,
                completion_token_price_per_1k=0.12,
            ),
            temperature=0.5,
            top_p=None,
            max_tokens=1000,
            default_headers={},
        ),
    )


def get_skill(skill_id: str = "ws-1") -> WaldiezSkill:
    """Get a WaldiezSkill.

    Parameters
    ----------
    skill_id : str, optional
        The skill ID, by default "ws-1"

    Returns
    -------
    WaldiezSkill
        A WaldiezSkill instance.
    """
    return WaldiezSkill(
        id=skill_id,
        name="skill_name",
        description="Skill Description",
        tags=["skill"],
        requirements=["chess"],
        type="skill",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezSkillData(
            content=(
                "def skill_name():\n"
                '    """Skill Description."""\n'
                "    return 'Skill Response'"
            ),
            secrets={
                "SKILL_KEY": "skill_value",
            },
        ),
    )


def get_user_proxy(agent_id: str = "wa-1") -> WaldiezUserProxy:
    """Get a WaldiezUserProxy.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-1"

    Returns
    -------
    WaldiezUserProxy
        A WaldiezUserProxy instance.
    """
    return WaldiezUserProxy(
        id=agent_id,
        name="user",
        description="User Agent",
        type="agent",
        agent_type="user",
        tags=["user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezUserProxyData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=WaldiezAgentCodeExecutionConfig(
                work_dir="coding",
                use_docker=None,
                last_n_messages=3,
                functions=["ws-1"],
                timeout=40,
            ),
            agent_default_auto_reply="I am a user.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[
                WaldiezAgentLinkedSkill(
                    id="ws-1",
                    executor_id="wa-2",
                )
            ],
            nested_chats=[
                WaldiezAgentNestedChat(
                    triggered_by=["wa-1"],
                    messages=[
                        WaldiezAgentNestedChatMessage(
                            id="wc-2",
                            is_reply=True,
                        ),
                        WaldiezAgentNestedChatMessage(
                            id="wc-3",
                            is_reply=False,
                        ),
                    ],
                ),
            ],
            teachability=WaldiezAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_assistant(agent_id: str = "wa-2") -> WaldiezAssistant:
    """Get a WaldiezAssistant.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-2"

    Returns
    -------
    WaldiezAssistant
        A WaldiezAssistant instance.
    """
    assistant_termination = (
        "def is_termination_message(message):\n"
        '    """Check if the message is a termination message."""\n'
        "    return any(\n"
        '        keyword in message.get("content", "").lower()\n'
        '        for keyword in ["bye", "goodbye"]\n'
        "    )"
    )
    return WaldiezAssistant(
        id=agent_id,
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        tags=["assistant"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezAssistantData(
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am an assistant.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="method",
                keywords=[],
                criterion="found",
                method_content=assistant_termination,
            ),
            model_ids=["wm-1"],
            skills=[
                WaldiezAgentLinkedSkill(
                    id="ws-1",
                    executor_id="wa-2",
                ),
            ],
            nested_chats=[],
            teachability=WaldiezAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
            is_multimodal=True,
        ),
    )


def get_group_manager(agent_id: str = "wa-3") -> WaldiezGroupManager:
    """Get a WaldiezGroupManager.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-3"

    Returns
    -------
    WaldiezGroupManager
        A WaldiezGroupManager instance.
    """
    custom_speaker_selection = (
        "def custom_speaker_selection(last_speaker, groupchat):\n"
        "    return last_speaker"
    )
    return WaldiezGroupManager(
        id=agent_id,
        name="group_manager",
        description="Group Manager Agent",
        type="agent",
        agent_type="manager",
        tags=["manager"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezGroupManagerData(
            max_round=10,
            admin_name="user",
            enable_clear_history=True,
            send_introductions=False,
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am a group manager.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="keyword",
                keywords=["TERMINATE"],
                criterion="exact",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            speakers=WaldiezGroupManagerSpeakers(
                selection_mode="transition",
                selection_method="custom",
                selection_custom_method=custom_speaker_selection,
                allow_repeat=["wa-1"],
                max_retries_for_selecting=3,
                allowed_or_disallowed_transitions={
                    "wa-1": ["wa-2"],
                    "wa-2": ["wa-1"],
                },
                transitions_type="allowed",
            ),
            teachability=WaldiezAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_rag_user(agent_id: str = "wa-4") -> WaldiezRagUser:
    """Get a WaldiezRagUser.

    Parameters
    ----------
    agent_id : str, optional
        The agent ID, by default "wa-4"

    Returns
    -------
    WaldiezRagUser
        A WaldiezRagUser instance.
    """
    custom_embedding = "def custom_embedding_function():\n    return list"
    return WaldiezRagUser(
        id=agent_id,
        name="rag_user",
        description="RAG User",
        tags=["rag_user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        type="agent",
        agent_type="rag_user",
        data=WaldiezRagUserData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=False,
            agent_default_auto_reply="I am a group manager.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="keyword",
                criterion="ending",
                keywords=["bye", "goodbye"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            retrieve_config=WaldiezRagUserRetrieveConfig(
                task="default",
                vector_db="chroma",
                db_config=WaldiezRagUserVectorDbConfig(
                    model=None,
                    use_memory=False,
                    use_local_storage=True,
                    local_storage_path="documents",
                    connection_url=None,
                    wait_until_document_ready=None,
                    wait_until_index_ready=None,
                    metadata=None,
                ),
                docs_path=[
                    "documents",
                    "C:\\Users\\username\\Documents\\file.txt",
                    "/home/username/Documents/",
                    "https://example.com/file.txt",
                ],
                new_docs=True,
                model=None,
                chunk_token_size=100,
                context_max_tokens=1000,
                chunk_mode="multi_lines",
                must_break_at_empty_line=True,
                use_custom_embedding=True,
                embedding_function=custom_embedding,
                use_custom_text_split=False,
                custom_text_split_function=None,
                use_custom_token_count=False,
                custom_token_count_function=None,
                collection_name="autogen-docs",
                custom_text_types=None,
                customized_answer_prefix=None,
                update_context=True,
                get_or_create=True,
                overwrite=True,
                recursive=True,
                distance_threshold=20,
                n_results=10,
                customized_prompt=None,
            ),
            teachability=WaldiezAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
    )


def get_chats(count: int = 3) -> List[WaldiezChat]:
    """Get a list of WaldiezChat instances.

    Parameters
    ----------
    count : int, optional
        The number of chats to generate, by default 3

    Returns
    -------
    List[WaldiezChat]
        A list of WaldiezChat instances
    """
    chats = []
    custom_message = (
        "def callable_message(sender, recipient, context):\n"
        '    return "hello!"'
    )
    for index in range(count):
        context = {"problem": "Solve tha task."} if index == 0 else {}
        nested_chat = WaldiezChatNested(
            message=None,
            reply=None,
        )
        source_index = index + 1
        target_index = index + 2
        chat = WaldiezChat(
            id=f"wc-{index + 1}",
            data=WaldiezChatData(
                name=f"chat_{index + 1}",
                description=f"Description of chat {index + 1}",
                source=f"wa-{source_index}",
                target=f"wa-{target_index}",
                position=-1,
                order=index,
                clear_history=True,
                silent=False,
                max_turns=5,
                message=WaldiezChatMessage(
                    type="string" if index != 2 else "method",
                    use_carryover=False,
                    content=(
                        f"Hello wa-{source_index}"
                        if index != 2
                        else custom_message
                    ),
                    context=context,
                ),
                summary=WaldiezChatSummary(
                    method="reflection_with_llm",
                    prompt="Summarize the chat.",
                    args={"summary_role": "user"},
                ),
                nested_chat=nested_chat,
                real_source=None,
                real_target=None,
            ),
        )
        chats.append(chat)
    return chats


def get_flow() -> WaldiezFlow:
    """Get a WaldiezFlow instance.

    Returns
    -------
    WaldiezFlow
        A WaldiezFlow instance.
    """
    model = get_model()
    skill = get_skill()
    user = get_user_proxy()
    assistant = get_assistant()
    manager = get_group_manager()
    rag_user = get_rag_user()
    chats = get_chats()
    agents = WaldiezAgents(
        users=[user],
        assistants=[assistant],
        managers=[manager],
        rag_users=[rag_user],
    )
    flow = WaldiezFlow(
        id="wf-1",
        name="flow_name",
        type="flow",
        description="Flow Description",
        tags=["flow"],
        requirements=[],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldiezFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents,
            models=[model],
            skills=[skill],
            chats=chats,
        ),
    )
    return flow
