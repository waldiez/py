"""Common fixtures for tests."""

import pytest

from waldiez.models import (
    WaldieAgents,
    WaldieAgentTeachability,
    WaldieAgentTerminationMessage,
    WaldieAssistant,
    WaldieAssistantData,
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
    WaldieChatSummary,
    WaldieFlow,
    WaldieFlowData,
    WaldieUserProxy,
    WaldieUserProxyData,
)


def get_runnable_flow() -> WaldieFlow:
    """Get a runnable WaldieFlow instance.

    without models and skills

    Returns
    -------
    WaldieFlow
        A WaldieFlow instance.
    """
    user = WaldieUserProxy(
        id="wa-1",
        name="user",
        agent_type="user",
        description="User Agent",
        type="agent",
        data=WaldieUserProxyData(
            system_message=None,
            human_input_mode="ALWAYS",
            max_tokens=100,
            code_execution_config=False,
            agent_default_auto_reply="I am a user.",
            max_consecutive_auto_reply=5,
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
        tags=["user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    assistant = WaldieAssistant(
        id="wa-2",
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        data=WaldieAssistantData(
            system_message=None,
            human_input_mode="NEVER",
            max_tokens=100,
            code_execution_config=False,
            agent_default_auto_reply="I am an assistant.",
            max_consecutive_auto_reply=5,
            termination=WaldieAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=WaldieAgentTeachability(
                enabled=False,
                verbosity=0,
                reset_db=False,
                recall_threshold=1.5,
                max_num_retrievals=10,
            ),
        ),
        tags=["assistant"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    chat = WaldieChat(
        id="wc-1",
        data=WaldieChatData(
            name="chat_1",
            description="Description of chat 1",
            source="wa-1",
            target="wa-2",
            position=-1,
            order=0,
            clear_history=True,
            silent=False,
            max_turns=2,
            message=WaldieChatMessage(
                type="string",
                use_carryover=False,
                content="Hello wa-1",
                context={},
            ),
            summary=WaldieChatSummary(
                method="last_msg",
                prompt="",
                args={},
            ),
            nested_chat=WaldieChatNested(
                message=None,
                reply=None,
            ),
            real_source=None,
            real_target=None,
        ),
    )
    agents = WaldieAgents(
        users=[user],
        assistants=[assistant],
        managers=[],
        rag_users=[],
    )
    flow = WaldieFlow(
        id="wf-1",
        name="flow_name",
        type="flow",
        description="Flow Description",
        data=WaldieFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents,
            models=[],
            skills=[],
            chats=[chat],
        ),
        tags=["flow"],
        requirements=[],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    return flow


@pytest.fixture(scope="function")
def waldie_flow() -> WaldieFlow:
    """Get a valid, runnable WaldieFlow instance.

    without models and skills

    Returns
    -------
    WaldieFlow
        A WaldieFlow instance.
    """
    return get_runnable_flow()
