"""Helper functions for exporting chat data to code.

Functions
---------
export_single_chat_string
    Get the chat string when there is only one chat in the flow.
export_multiple_chats_string
    Get the chats content, when there are more than one chats in the flow.
"""

from typing import Any, Dict, List, Optional, Tuple

from waldiez.models import (
    WaldiezAgent,
    WaldiezChat,
    WaldiezChatMessage,
    WaldiezRagUser,
)

from ..utils import get_escaped_string, get_object_string


# pylint: disable=line-too-long
def export_single_chat_string(
    flow: Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent],
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chat string when there is only one chat in the flow.

    Parameters
    ----------
    flow : Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]
        The chat flow.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat string and additional methods string if any

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezChatData, WaldiezChatMessage
    >>> chat = WaldiezChat(
    ...     id="wc-1",
    ...     name="chat1",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat1"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-1",
    ...         recipient="wa-2",
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="Hello, how are you?",
    ...         ),
    ...     ),
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    >>> chat_names = {"wc-1": "chat1"}
    >>> export_single_chat_string((chat, agent1, agent2), agent_names, chat_names, 0)
    agent1.initiate_chat(
        agent2,
        message="Hello, how are you?",
    )
    ```
    """
    tab = "    " * tabs
    chat, sender, recipient = flow
    chat_args = chat.get_chat_args(sender=sender)
    if not chat_args:
        return _get_empty_simple_chat_string(
            tab,
            chat=chat,
            sender=sender,
            recipient=recipient,
            agent_names=agent_names,
        )
    return _get_simple_chat_string(
        chat=chat,
        chat_args=chat_args,
        sender=sender,
        recipient=recipient,
        agent_names=agent_names,
        chat_names=chat_names,
        tabs=tabs,
    )


def export_multiple_chats_string(
    main_chats: List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]],
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chats content, when there are more than one chats in the flow.

    Parameters
    ----------
    main_chats : List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]]
        The main chats.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The main chats content and additional methods string if any.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezChatData, WaldiezChatMessage
    >>> chat1 = WaldiezChat(
    ...     id="wc-1",
    ...     name="chat1",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat1"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-1",
    ...         recipient="wa-2",
    ...         position=0,
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="Hello, how are you?",
    ...         ),
    ...     ),
    ... )
    >>> chat2 = WaldiezChat(
    ...     id="wc-2",
    ...     name="chat2",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat2"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-2",
    ...         recipient="wa-1",
    ...         position=1,
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="I am good, thank you. How about you?",
    ...         ),
    ...     ),
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    >>> chat_names = {"wc-1": "chat1", "wc-2": "chat2"}
    >>> export_multiple_chats_string([(chat1, agent1, agent2), (chat2, agent2, agent1)], chat_names, agent_names, 0)
    initiate_chats([
        {
            "sender": agent1,
            "recipient": agent2,
            "message": "Hello, how are you?",
        },
        {
            "sender": agent2,
            "recipient": agent1,
            "message": "I am good, thank you. How about you?",
        },
    ])
    ```
    """
    tab = "    " * tabs
    content = "\n"
    additional_methods_string = ""
    content = "initiate_chats(["
    for chat, sender, recipient in main_chats:
        chat_string, additional_methods = _get_chat_dict_string(
            chat=chat,
            chat_names=chat_names,
            sender=sender,
            recipient=recipient,
            agent_names=agent_names,
            tabs=tabs + 1,
        )
        additional_methods_string += additional_methods
        content += f"\n{tab}    {chat_string}"
    content += "\n" + "    " * tabs + "])"
    return content, additional_methods_string


def _get_chat_message_string(
    chat: WaldiezChat,
    chat_names: Dict[str, str],
) -> Tuple[str, Optional[str]]:
    """Get the agent's message as a string.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name with all the chats in the flow.

    Returns
    -------
    Tuple[str, Optional[str]]
        If the message is a string, the message content and None.
        If the message is a method, the method name and the method content.
        If the message is None, 'None' and None.
    """
    if (
        not chat.message
        or chat.message.type == "none"
        or chat.message.content is None
        or chat.message_content is None
    ):
        return "None", None
    if chat.message.type == "string":
        return chat.message.content, None
    chat_name = chat_names[chat.id]
    original_function_name = "callable_message"
    method_args = "sender, recipient, context"
    function_name = f"{original_function_name}_{chat_name}"
    function_def = f"def {function_name}({method_args}):"
    return function_name, function_def + "\n" + chat.message_content + "\n"


def _get_chat_dict_string(
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get a chat dictionary string.

    If the chat message is a separate method and not a string or a lambda,
    we return the method string (definition and body) as well as the rest
    of the arguments.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat dictionary string and additional methods string if any.
    """
    tab = "    " * tabs
    chat_args = chat.get_chat_args(sender=sender)
    chat_string = "{"
    chat_string += "\n" + f'{tab}    "sender": {agent_names[sender.id]},'
    chat_string += "\n" + f'{tab}    "recipient": {agent_names[recipient.id]},'
    additional_methods_string = ""
    for key, value in chat_args.items():
        if isinstance(value, str):
            chat_string += "\n" + f'{tab}    "{key}": "{value}",'
        elif isinstance(value, dict):
            chat_string += (
                "\n"
                f'{tab}    "{key}": {get_object_string(value, tabs=tabs + 1)},'
            )
        else:
            chat_string += "\n" + f'{tab}    "{key}": {value},'
    if (
        sender.agent_type == "rag_user"
        and isinstance(sender, WaldiezRagUser)
        and chat.message.type == "rag_message_generator"
    ):
        message = f"{agent_names[sender.id]}.message_generator"
        chat_string += "\n" + f'{tab}    "message": {message},'
        chat_string += "\n" + tab + "},"
        return chat_string, additional_methods_string
    message, method_content = _get_chat_message_string(
        chat=chat,
        chat_names=chat_names,
    )
    if message and isinstance(chat.data.message, WaldiezChatMessage):
        message = get_escaped_string(message)
        if chat.data.message.type == "method":
            if method_content:
                additional_methods_string += "\n" + method_content
            chat_string += "\n" + f'{tab}    "message": {message},'
        elif chat.data.message.type == "string" and chat.data.message.content:
            chat_string += "\n" + f'{tab}    "message": "{message}",'
    chat_string += "\n" + tab + "},"
    return chat_string, additional_methods_string


def _get_empty_simple_chat_string(
    tab: str,
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    agent_names: Dict[str, str],
) -> Tuple[str, str]:
    content = tab
    sender_name = agent_names[sender.id]
    recipient_name = agent_names[recipient.id]
    content += f"{sender_name}.initiate_chat(\n"
    content += tab + f"    {recipient_name},\n"
    message_arg, _ = _get_chat_message(
        tab=tab,
        chat=chat,
        chat_names={},
        sender=sender,
        sender_name=sender_name,
    )
    content += message_arg
    content += tab + ")"
    return content, ""


def _get_chat_message(
    tab: str,
    chat: WaldiezChat,
    chat_names: Dict[str, str],
    sender: WaldiezAgent,
    sender_name: str,
) -> Tuple[str, str]:
    additional_methods_string = ""
    method_content: Optional[str] = None
    if (
        sender.agent_type == "rag_user"
        and isinstance(sender, WaldiezRagUser)
        and chat.message.type == "rag_message_generator"
    ):
        message = f"{sender_name}.message_generator"
        return f"\n{tab}    message={message},", additional_methods_string
    message, method_content = _get_chat_message_string(
        chat=chat,
        chat_names=chat_names,
    )
    if message and isinstance(chat.data.message, WaldiezChatMessage):
        message = get_escaped_string(message)
        if chat.data.message.type == "method":
            additional_methods_string += (
                method_content if method_content else ""
            )
            return f"\n{tab}    message={message},", additional_methods_string
        if chat.message.type == "string" and chat.data.message.content:
            return f'\n{tab}    message="{message}",', additional_methods_string
        return "", additional_methods_string
    return "", additional_methods_string  # pragma: no cover


def _get_simple_chat_string(
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    chat_args: Dict[str, Any],
    tabs: int,
) -> Tuple[str, str]:
    tab = "    " * tabs
    sender_name = agent_names[sender.id]
    recipient_name = agent_names[recipient.id]
    chat_string = f"{sender_name}.initiate_chat(\n"
    chat_string += f"{tab}    {recipient_name},"
    for key, value in chat_args.items():
        if isinstance(value, str):
            chat_string += f'\n{tab}    {key}="{value}",'
        elif isinstance(value, dict):
            chat_string += (
                f"\n{tab}    {key}={get_object_string(value, tabs + 1)},"
            )
        else:
            chat_string += f"\n{tab}    {key}={value},"
    message_arg, additional_methods_string = _get_chat_message(
        tab=tab,
        chat=chat,
        chat_names=chat_names,
        sender=sender,
        sender_name=sender_name,
    )
    chat_string += message_arg
    chat_string += f"\n{tab})"
    return chat_string, additional_methods_string
