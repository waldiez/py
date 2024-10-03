"""Test waldiez.models.flow.*."""

import pytest

from waldiez.models import (
    WaldieAgents,
    WaldieAgentTeachability,
    WaldieAgentTerminationMessage,
    WaldieAssistant,
    WaldieAssistantData,
    WaldieChat,
    WaldieChatData,
    WaldieChatNested,
    WaldieChatSummary,
    WaldieFlow,
    WaldieFlowData,
    WaldieGroupManager,
    WaldieGroupManagerData,
    WaldieGroupManagerSpeakers,
    WaldieModel,
    WaldieModelData,
    WaldieModelPrice,
    WaldieRagUser,
    WaldieRagUserData,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserVectorDbConfig,
    WaldieSkill,
    WaldieSkillData,
    WaldieUserProxy,
    WaldieUserProxyData,
)


def test_waldie_flow() -> None:
    """Test WaldieFlow."""
    # Given
    user = WaldieUserProxy(
        id="wa-1",
        name="user",
        type="agent",
        agent_type="user",
        description="User",
        tags=["user"],
        requirements=["user"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieUserProxyData(
            system_message="User message",
            human_input_mode="ALWAYS",
            max_tokens=100,
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            agent_default_auto_reply="User auto reply",
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                criterion="found",
                keywords=["TERMINATE"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
        ),
    )
    assistant = WaldieAssistant(
        id="wa-2",
        name="assistant",
        type="agent",
        agent_type="assistant",
        description="Assistant",
        tags=["assistant"],
        requirements=["assistant"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieAssistantData(
            system_message="Assistant message",
            human_input_mode="ALWAYS",
            max_tokens=100,
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            agent_default_auto_reply="Assistant auto reply",
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                criterion="found",
                keywords=["TERMINATE"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
        ),
    )
    manager = WaldieGroupManager(
        id="wa-3",
        name="manager",
        type="agent",
        agent_type="manager",
        description="Manager",
        tags=["manager"],
        requirements=["manager"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieGroupManagerData(
            system_message="Manager message",
            human_input_mode="ALWAYS",
            max_tokens=100,
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            agent_default_auto_reply="Manager auto reply",
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                criterion="found",
                keywords=["TERMINATE"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            max_round=1,
            enable_clear_history=False,
            admin_name="user",
            send_introductions=False,
            speakers=WaldieGroupManagerSpeakers(
                selection_method="round_robin",
                selection_custom_method=None,
                selection_mode="transition",
                transitions_type="allowed",
                allow_repeat=True,
                allowed_or_disallowed_transitions={
                    "wa-1": ["wa-2"],
                },
                max_retries_for_selecting=1,
            ),
        ),
    )
    rag_user = WaldieRagUser(
        id="wa-4",
        name="rag_user",
        type="agent",
        agent_type="rag_user",
        description="Rag user",
        tags=["rag_user"],
        requirements=["rag_user"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieRagUserData(
            system_message="Rag user message",
            use_message_generator=False,
            human_input_mode="ALWAYS",
            max_tokens=100,
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            agent_default_auto_reply="Rag user auto reply",
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                criterion="found",
                keywords=["TERMINATE"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            retrieve_config=WaldieRagUserRetrieveConfig(
                task="code",
                vector_db="chroma",
                db_config=WaldieRagUserVectorDbConfig(
                    local_storage_path="",
                    use_local_storage=False,
                    use_memory=False,
                    connection_url="",
                    wait_until_document_ready=None,
                    wait_until_index_ready=None,
                    metadata={},
                    model="all-MiniLM-L6-v2",
                ),
                distance_threshold=0.0,
                docs_path="",
                chunk_mode="multi_lines",
                chunk_token_size=100,
                collection_name="test",
                context_max_tokens=100,
                new_docs=False,
                model="gpt2",
                must_break_at_empty_line=False,
                get_or_create=True,
                overwrite=False,
                embedding_function=None,
                custom_text_split_function=None,
                use_custom_embedding=False,
                use_custom_text_split=False,
                use_custom_token_count=False,
                custom_text_types=None,
                custom_token_count_function=None,
                customized_answer_prefix="",
                customized_prompt="",
                update_context=False,
                recursive=False,
            ),
        ),
    )
    agents = WaldieAgents(
        users=[user],
        assistants=[assistant],
        managers=[manager],
        rag_users=[rag_user],
    )
    chats = [
        WaldieChat(
            id="wc-1",
            data=WaldieChatData(
                name="chat_data",
                description="Chat data",
                source="wa-1",
                target="wa-2",
                position=-1,
                order=0,
                clear_history=False,
                message="Hello there",
                max_turns=1,
                nested_chat=WaldieChatNested(message=None, reply=None),
                summary=WaldieChatSummary(
                    method="last_msg",
                    prompt="",
                    args={},
                ),
                silent=False,
                real_source=None,
                real_target=None,
            ),
        ),
        WaldieChat(
            id="wc-2",
            data=WaldieChatData(
                name="chat_data",
                description="Chat data",
                source="wa-3",
                target="wa-2",
                position=-1,
                order=1,
                clear_history=False,
                message="Hello there",
                max_turns=2,
                nested_chat=WaldieChatNested(message=None, reply=None),
                summary=WaldieChatSummary(
                    method="last_msg",
                    prompt="",
                    args={},
                ),
                silent=False,
                real_source=None,
                real_target=None,
            ),
        ),
        WaldieChat(
            id="wc-3",
            data=WaldieChatData(
                name="chat_data",
                description="Chat data",
                source="wa-3",
                target="wa-4",
                position=-1,
                order=-1,
                clear_history=False,
                message="Hello there",
                summary=WaldieChatSummary(
                    method="last_msg",
                    prompt="",
                    args={},
                ),
                max_turns=3,
                nested_chat=WaldieChatNested(message=None, reply=None),
                silent=False,
                real_source=None,
                real_target=None,
            ),
        ),
    ]
    skill = WaldieSkill(
        id="ws-1",
        name="skill_name",
        type="skill",
        description="Skill description",
        tags=["skill"],
        requirements=["skill"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieSkillData(
            content="def skill_name():\n    return 'Skill name'",
            secrets={},
        ),
    )
    model = WaldieModel(
        id="wm-1",
        name="model_name",
        type="model",
        description="Model description",
        tags=["model"],
        requirements=["model"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieModelData(
            api_key="-",
            api_type="openai",
            api_version="2020-05-03",
            base_url="https://example.com",
            temperature=0.1,
            top_p=None,
            max_tokens=100,
            default_headers={},
            price=WaldieModelPrice(
                prompt_price_per_1k=0.06,
                completion_token_price_per_1k=0.12,
            ),
        ),
    )
    flow_data = WaldieFlowData(
        nodes=[],
        edges=[],
        viewport={},
        agents=agents,
        models=[model],
        skills=[skill],
        chats=chats,
    )
    # When
    flow1 = WaldieFlow(
        id="wf-1",
        name="flow",
        type="flow",
        description="Flow",
        tags=["flow"],
        requirements=["flow"],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=flow_data,
    )
    # Then
    assert not flow1.data.nodes
    assert flow1.get_agent_by_id("wa-1").id == "wa-1"
    with pytest.raises(ValueError):
        flow1.get_agent_by_id("wa-5")
    assert not flow1.get_group_chat_members("wa-1")
    assert flow1.get_agent_connections("wa-1") == ["wa-2"]
    assert flow1.get_agent_connections("wa-2") == ["wa-1", "wa-3"]
    assert flow1.get_agent_connections("wa-3") == ["wa-2", "wa-4"]
    assert flow1.get_agent_connections("wa-3", False) == ["wa-2"]
    assert flow1.get_agent_connections("wa-2", False) == ["wa-1", "wa-3"]
    assert flow1.get_agent_connections("wa-1", False) == ["wa-2"]
    assert flow1.get_group_chat_members("wa-3") == [assistant, rag_user]

    with pytest.raises(ValueError):
        # no chats
        WaldieFlow(
            id="wf-2",
            name="flow",
            type="flow",
            description="Flow",
            tags=["flow"],
            requirements=["flow"],
            storage_id="flow-1",
            created_at="2021-01-01T00:00:00.000Z",
            updated_at="2021-01-01T00:00:00.000Z",
            data=WaldieFlowData(
                nodes=[],
                edges=[],
                viewport={},
                agents=agents,
                models=[model],
                skills=[skill],
                chats=[],
            ),
        )
    with pytest.raises(ValueError):
        # not unique skill IDs
        WaldieFlow(
            id="wf-2",
            name="flow",
            type="flow",
            description="Flow",
            tags=["flow"],
            requirements=["flow"],
            storage_id="flow-1",
            created_at="2021-01-01T00:00:00.000Z",
            updated_at="2021-01-01T00:00:00.000Z",
            data=WaldieFlowData(
                nodes=[],
                edges=[],
                viewport={},
                agents=agents,
                models=[],
                skills=[skill, skill],
                chats=chats,
            ),
        )

    with pytest.raises(ValueError):
        # not unique model IDs
        WaldieFlow(
            id="wf-3",
            name="flow",
            type="flow",
            description="Flow",
            tags=["flow"],
            requirements=["flow"],
            storage_id="flow-1",
            created_at="2021-01-01T00:00:00.000Z",
            updated_at="2021-01-01T00:00:00.000Z",
            data=WaldieFlowData(
                nodes=[],
                edges=[],
                viewport={},
                agents=agents,
                models=[model, model],
                skills=[],
                chats=chats,
            ),
        )
    assistant2 = WaldieAssistant(
        id="wa-5",
        name="assistant",
        type="agent",
        agent_type="assistant",
        description="Assistant",
        tags=["assistant"],
        requirements=["assistant"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieAssistantData(
            system_message="Assistant message",
            human_input_mode="ALWAYS",
            max_tokens=100,
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            agent_default_auto_reply="Assistant auto reply",
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=0.0,
                max_num_retrievals=0,
            ),
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                criterion="found",
                keywords=["TERMINATE"],
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
        ),
    )
    agents2 = WaldieAgents(
        users=[user],
        assistants=[assistant, assistant2],
        managers=[manager],
        rag_users=[rag_user],
    )
    with pytest.raises(ValueError):
        # agents do not connect to any other node
        WaldieFlow(
            id="wf-4",
            name="flow",
            type="flow",
            description="Flow",
            tags=["flow"],
            requirements=["flow"],
            storage_id="flow-1",
            created_at="2021-01-01T00:00:00.000Z",
            updated_at="2021-01-01T00:00:00.000Z",
            data=WaldieFlowData(
                nodes=[],
                edges=[],
                viewport={},
                agents=agents2,
                models=[model],
                skills=[skill],
                chats=chats,
            ),
        )
    # set positions < 0
    # and one chat in the flow
    agents3 = WaldieAgents(
        users=[user],
        assistants=[assistant],
        managers=[],
        rag_users=[],
    )
    chats2 = [
        WaldieChat(
            id="wc-1",
            data=WaldieChatData(
                name="chat_data",
                description="Chat data",
                source="wa-1",
                target="wa-2",
                position=-1,
                order=-1,
                clear_history=False,
                summary=WaldieChatSummary(
                    method="last_msg",
                    prompt="",
                    args={},
                ),
                message="Hello there",
                max_turns=1,
                nested_chat=WaldieChatNested(message=None, reply=None),
                silent=False,
                real_source=None,
                real_target=None,
            ),
        ),
    ]
    flow = WaldieFlow(
        id="wf-5",
        name="flow",
        type="flow",
        description="Flow",
        tags=["flow"],
        requirements=["flow"],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents3,
            models=[],
            skills=[],
            chats=chats2,
        ),
    )
    assert flow.ordered_flow == [(chats2[0], user, assistant)]
