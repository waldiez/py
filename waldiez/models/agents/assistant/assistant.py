"""Assistant agent model."""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import WaldieAgent
from .assistant_data import WaldieAssistantData


class WaldieAssistant(WaldieAgent):
    """Assistant agent model.

    A `WaldieAgent` with agent_type `assistant` and
    default `human_input_mode`: `"NEVER"`
    See `WaldieAgent`, `WaldieAssistantData`, `WaldieAgentData` for more info.

    Attributes
    ----------
    agent_type : Literal["assistant"]
        The agent type: 'assistant' for an assistant agent
    data : WaldieAssistantData
        The assistant agent's data
    """

    agent_type: Annotated[
        Literal["assistant"],
        Field(
            "assistant",
            title="Agent type",
            description="The agent type in a graph: 'assistant'",
            alias="agentType",
        ),
    ]
    data: Annotated[
        WaldieAssistantData,
        Field(
            title="Data",
            description="The assistant agent's data",
            default_factory=WaldieAssistantData,
        ),
    ]
