"""Export the chats content."""

from typing import Dict, List, Tuple

from waldiez.models import WaldiezAgent, WaldiezChat

from .helpers import export_multiple_chats_string, export_single_chat_string


def export_chats(
    main_chats: List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]],
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chats content.

    Parameters
    ----------
    main_chats : List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]]
        The main flow chats.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chats content and additional methods string if any.
    """
    if len(main_chats) == 1:
        return export_single_chat_string(
            flow=main_chats[0],
            agent_names=agent_names,
            chat_names=chat_names,
            tabs=tabs,
        )
    return export_multiple_chats_string(
        main_chats=main_chats,
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=tabs,
    )
