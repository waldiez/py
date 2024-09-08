"""Waldie models package.

- Agents (Users, Assistants, Group Managers, etc.).
- Chat (Messages, Summaries, etc.).
- Model (LLM config, API type, etc.).
- Skill (Skills/Tools to be registered).
- Flow (Flow of the conversation).
"""

from .agents import (
    WaldieAgent,
    WaldieAgentCodeExecutionConfig,
    WaldieAgentData,
    WaldieAgentLinkedSkill,
    WaldieAgentNestedChat,
    WaldieAgentNestedChatMessage,
    WaldieAgents,
    WaldieAgentTeachability,
    WaldieAgentTerminationMessage,
    WaldieAgentType,
    WaldieAssistant,
    WaldieAssistantData,
    WaldieGroupManager,
    WaldieGroupManagerData,
    WaldieGroupManagerSpeakers,
    WaldieGroupManagerSpeakersSelectionMethod,
    WaldieGroupManagerSpeakersSelectionMode,
    WaldieGroupManagerSpeakersTransitionsType,
    WaldieRagUser,
    WaldieRagUserChunkMode,
    WaldieRagUserData,
    WaldieRagUserModels,
    WaldieRagUserRetrieveConfig,
    WaldieRagUserTask,
    WaldieRagUserVectorDb,
    WaldieRagUserVectorDbConfig,
    WaldieUserProxy,
    WaldieUserProxyData,
)
from .chat import (
    WaldieChat,
    WaldieChatData,
    WaldieChatMessage,
    WaldieChatNested,
    WaldieChatSummary,
    WaldieChatSummaryMethod,
)
from .common import METHOD_ARGS, METHOD_TYPE_HINTS, WaldieMethodName
from .flow import WaldieFlow, WaldieFlowData
from .model import (
    WaldieModel,
    WaldieModelAPIType,
    WaldieModelData,
    WaldieModelPrice,
)
from .skill import WaldieSkill, WaldieSkillData

# pylint: disable=duplicate-code
__all__ = [
    "METHOD_ARGS",
    "METHOD_TYPE_HINTS",
    "WaldieMethodName",
    "WaldieAgent",
    "WaldieAgentCodeExecutionConfig",
    "WaldieAgentData",
    "WaldieAgentLinkedSkill",
    "WaldieAgentNestedChat",
    "WaldieAgentNestedChatMessage",
    "WaldieAgents",
    "WaldieAgentTeachability",
    "WaldieAgentTerminationMessage",
    "WaldieAgentType",
    "WaldieAssistant",
    "WaldieAssistantData",
    "WaldieChat",
    "WaldieChatData",
    "WaldieChatSummary",
    "WaldieChatNested",
    "WaldieChatSummaryMethod",
    "WaldieFlow",
    "WaldieFlowData",
    "WaldieGroupManager",
    "WaldieGroupManagerData",
    "WaldieGroupManagerSpeakers",
    "WaldieGroupManagerSpeakersSelectionMethod",
    "WaldieGroupManagerSpeakersSelectionMode",
    "WaldieGroupManagerSpeakersTransitionsType",
    "WaldieChatMessage",
    "WaldieModel",
    "WaldieModelAPIType",
    "WaldieModelData",
    "WaldieModelPrice",
    "WaldieRagUser",
    "WaldieRagUserData",
    "WaldieSkill",
    "WaldieSkillData",
    "WaldieUserProxy",
    "WaldieUserProxyData",
    "WaldieRagUserRetrieveConfig",
    "WaldieRagUserTask",
    "WaldieRagUserChunkMode",
    "WaldieRagUserVectorDb",
    "WaldieRagUserVectorDbConfig",
    "WaldieRagUserModels",
]
