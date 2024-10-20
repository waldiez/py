"""Test WaldieRunner."""

# pylint: disable=protected-access

from typing import Optional

import pytest

from waldiez import Waldie, WaldieIOStream, WaldieRunner
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
        description="User Agent",
        type="agent",
        agent_type="user",
        tags=["user"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
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
    )
    assistant = WaldieAssistant(
        id="wa-2",
        name="assistant",
        description="Assistant Agent",
        type="agent",
        agent_type="assistant",
        tags=["assistant"],
        requirements=[],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
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
        tags=["flow"],
        requirements=[],
        storage_id="flow-1",
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
        data=WaldieFlowData(
            nodes=[],
            edges=[],
            viewport={},
            agents=agents,
            models=[],
            skills=[],
            chats=[chat],
        ),
    )
    return flow


def test_runner() -> None:
    """Test WaldieRunner."""
    flow = get_runnable_flow()
    waldie = Waldie(flow=flow)
    runner = WaldieRunner(waldie)
    assert runner.waldie == waldie
    assert not runner.running

    prompt_input: Optional[str] = None
    stream: WaldieIOStream

    def on_prompt_input(prompt: str) -> None:
        nonlocal prompt_input, stream
        prompt_input = prompt
        stream.forward_input("Reply to prompt\n")

    stream = WaldieIOStream(
        on_prompt_input=on_prompt_input,
        print_function=print,
    )
    with WaldieIOStream.set_default(stream):
        runner.run(stream)
    assert not runner.running
    assert runner._stream.get() is None
    assert prompt_input is not None
    stream.close()


def test_waldie_with_invalid_requirement(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test Waldie with invalid requirement.

    Parameters
    ----------
    capsys : pytest.CaptureFixture[str]
        Pytest fixture to capture stdout and stderr.
    """
    flow_dict = get_runnable_flow().model_dump(by_alias=True)
    # add an invalid requirement
    flow_dict["requirements"] = ["invalid_requirement"]
    waldie = Waldie.from_dict(data=flow_dict)
    runner = WaldieRunner(waldie)
    runner._install_requirements()
    std_err = capsys.readouterr().out
    assert (
        "ERROR: No matching distribution found for invalid_requirement"
        in std_err
    )
