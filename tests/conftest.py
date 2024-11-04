"""Common fixtures for tests."""

import pytest

from waldiez.models import (
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
    WaldiezUserProxy,
    WaldiezUserProxyData,
)


def get_runnable_flow() -> WaldiezFlow:
    """Get a runnable WaldiezFlow instance.

    without models and skills

    Returns
    -------
    WaldiezFlow
        A WaldiezFlow instance.
    """
    user = WaldiezUserProxy(
        id="wa-1",
        name="user",
        agent_type="user",
        description="User Agent",
        type="agent",
        data=WaldiezUserProxyData(
            system_message=None,
            human_input_mode="ALWAYS",
            code_execution_config=False,
            agent_default_auto_reply="I am a user.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=WaldiezAgentTeachability(
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
    assistant = WaldiezAssistant(
        id="wa-2",
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        data=WaldiezAssistantData(
            system_message=None,
            human_input_mode="NEVER",
            code_execution_config=False,
            agent_default_auto_reply="I am an assistant.",
            max_consecutive_auto_reply=5,
            termination=WaldiezAgentTerminationMessage(
                type="keyword",
                keywords=["bye", "goodbye"],
                criterion="found",
                method_content=None,
            ),
            model_ids=[],
            skills=[],
            nested_chats=[],
            teachability=WaldiezAgentTeachability(
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
    chat = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(
            name="chat_1",
            description="Description of chat 1",
            source="wa-1",
            target="wa-2",
            position=-1,
            order=0,
            clear_history=True,
            silent=False,
            max_turns=2,
            message=WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content="Hello wa-1",
                context={},
            ),
            summary=WaldiezChatSummary(
                method="last_msg",
                prompt="",
                args={},
            ),
            nested_chat=WaldiezChatNested(
                message=None,
                reply=None,
            ),
            real_source=None,
            real_target=None,
        ),
    )
    agents = WaldiezAgents(
        users=[user],
        assistants=[assistant],
        managers=[],
        rag_users=[],
    )
    flow = WaldiezFlow(
        id="wf-1",
        name="flow_name",
        type="flow",
        description="Flow Description",
        data=WaldiezFlowData(
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
def waldiez_flow() -> WaldiezFlow:
    """Get a valid, runnable WaldiezFlow instance.

    without models and skills

    Returns
    -------
    WaldiezFlow
        A WaldiezFlow instance.
    """
    return get_runnable_flow()


@pytest.fixture(scope="function")
def waldiez_flow_no_human_input() -> WaldiezFlow:
    """Get a valid, runnable WaldiezFlow instance with no human input.

    without models and skills

    Returns
    -------
    WaldiezFlow
        A WaldiezFlow instance.
    """
    flow = get_runnable_flow()
    dumped = flow.model_dump(by_alias=True)
    dumped["data"]["agents"]["users"][0]["data"]["humanInputMode"] = "NEVER"
    dumped["data"]["chats"][0]["data"]["maxTurns"] = 1
    return WaldiezFlow(**dumped)
