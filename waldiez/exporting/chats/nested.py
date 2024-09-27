"""Nested chats exporting."""

from typing import Dict, List, Optional, Tuple

from waldiez.models import (
    WaldieAgent,
    WaldieAgentNestedChat,
    WaldieAgentNestedChatMessage,
    WaldieChat,
)

from ..utils import get_escaped_string, get_object_string


def get_nested_chat_trigger_agent_names(
    all_chats: List[WaldieChat],
    nested_chat: WaldieAgentNestedChat,
    agent_names: Dict[str, str],
) -> str:
    """Get the trigger agent names for the nested chat.

    Parameters
    ----------
    all_chats : List[WaldieChat]
        All the chats in the flow.
    nested_chat : WaldieAgentNestedChat
        The nested chat.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.

    Returns
    -------
    str
        The trigger agent names.
    """
    trigger_agent_ids: List[str] = []
    for message in nested_chat.triggered_by:
        waldie_chat = next(chat for chat in all_chats if chat.id == message.id)
        if message.is_reply:
            trigger_agent_ids.append(waldie_chat.target)
        else:
            trigger_agent_ids.append(waldie_chat.source)
    agents = [agent_names[agent_id] for agent_id in trigger_agent_ids]
    trigger_string = f'{[", ".join(agents)]}'
    return trigger_string.replace("'", '"')


def get_nested_chat_message_string(
    waldie_chat: WaldieChat,
    message: WaldieAgentNestedChatMessage,
    agent: WaldieAgent,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
) -> Tuple[str, Optional[str]]:
    """Get the nested chat message string.

    Parameters
    ----------
    waldie_chat : WaldieChat
        The chat.
    message : WaldieAgentNestedChatMessage
        The message.
    agent : WaldieAgent
        The agent.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.

    Returns
    -------
    Tuple[str, Optional[str]]
        The message string and the method name if the message is a method.
    """
    sender_name: Optional[str] = None
    sender_id = waldie_chat.target if message.is_reply else waldie_chat.source
    recipient_id = (
        waldie_chat.source if message.is_reply else waldie_chat.target
    )
    if sender_id != agent.id:
        sender_name = agent_names[sender_id]
    recipient_name = agent_names[recipient_id]
    chat_dict = waldie_chat.get_chat_args()
    chat_dict["recipient"] = recipient_name
    if sender_name:
        chat_dict["sender"] = sender_name
    message_value, message_source = get_chat_nested_string(
        chat=waldie_chat, is_reply=message.is_reply, chat_names=chat_names
    )
    chat_dict["message"] = message_value
    message_dict_str = get_object_string(chat_dict, tabs=1)
    if message_source:
        # it's not a string, its the name of the function
        message_dict_str = message_dict_str.replace(
            f': "{message_value}"', f": {message_value}"
        )
    if sender_name:
        message_dict_str = message_dict_str.replace(
            f': "{sender_name}"', f": {sender_name}"
        )
    if recipient_name:
        message_dict_str = message_dict_str.replace(
            f': "{recipient_name}"', f": {recipient_name}"
        )
    return message_dict_str, message_source


def get_nested_chat_queue(
    nested_chat: WaldieAgentNestedChat,
    agent: WaldieAgent,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    all_chats: List[WaldieChat],
) -> Tuple[str, List[str]]:
    """Get the nested chat queue.

    Parameters
    ----------
    nested_chat : WaldieAgentNestedChat
        The nested chat.
    agent : WaldieAgent
        The agent.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    all_chats : List[WaldieChat]
        All the chats in the flow.

    Returns
    -------
    Tuple[str, List[str]]
        The nested chat queue and the methods to include.
    """
    message_methods_to_include = []
    chat_messages_str = "[\n"
    for message in nested_chat.messages:
        waldie_chat = next(chat for chat in all_chats if chat.id == message.id)
        message_str, message_source = get_nested_chat_message_string(
            waldie_chat=waldie_chat,
            message=message,
            agent=agent,
            agent_names=agent_names,
            chat_names=chat_names,
        )
        if message_source:
            message_methods_to_include.append(message_source)
        chat_messages_str += f"    {message_str}," + "\n"
    chat_messages_str += "]"
    if chat_messages_str == "[\n]":
        return "", message_methods_to_include
    return chat_messages_str, message_methods_to_include


def get_chat_nested_string(
    chat: WaldieChat,
    is_reply: bool,
    chat_names: Dict[str, str],
) -> Tuple[str, Optional[str]]:
    """Get the nested chat message.

    Parameters
    ----------
    chat : WaldieChat
        The chat.
    is_reply : bool
        Whether to use the nested chat's reply message or not.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name

    Returns
    -------
    Tuple[str, Optional[str]]
        If the message is a string, the message content and None.
        If the message is a method, the method name and the method content.
        If the message is None, 'None' and None.
    """
    message = (
        chat.data.nested_chat.reply
        if is_reply
        else chat.data.nested_chat.message
    )
    if not message or message.type == "none" or message.content is None:
        return "None", None
    if message.type == "string":
        return get_escaped_string(message.content), None
    chat_name = chat_names[chat.id]
    method_args = "recipient, messages, sender, config"
    function_name = "nested_chat_reply" if is_reply else "nested_chat_message"
    new_function_name = f"{function_name}_{chat_name}"
    function_def = f"\ndef {new_function_name}({method_args}):"
    return new_function_name, function_def + "\n" + message.content + "\n"


def export_nested_chat(
    agent: WaldieAgent,
    all_chats: List[WaldieChat],
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
) -> str:
    """Get the nested chat string.

    Parameters
    ----------
    agent : WaldieAgent
        The agent.
    all_chats : List[WaldieChat]
        All the chats in the flow.
    chat_names : Dict[str, str]
        The chat names.
    agent_names : Dict[str, str]
        The agent names.

    Returns
    -------
    str
        The nested chat string.
    """
    if not agent.data.nested_chats:
        return ""
    content = ""
    extra_contents = []
    agent_name = agent_names[agent.id]
    use_suffix = len(agent.data.nested_chats) > 1
    for index, entry in enumerate(agent.data.nested_chats):
        trigger_names = get_nested_chat_trigger_agent_names(
            all_chats=all_chats, nested_chat=entry, agent_names=agent_names
        )
        chat_queue, extra_methods = get_nested_chat_queue(
            nested_chat=entry,
            agent=agent,
            agent_names=agent_names,
            chat_names=chat_names,
            all_chats=all_chats,
        )
        if not chat_queue:
            continue
        extra_contents.extend(extra_methods)
        var_name = (
            f"{agent_name}_chat_queue_{index}"
            if use_suffix
            else f"{agent_name}_chat_queue"
        )
        content += f"\n{var_name} = {chat_queue}" + "\n"
        content += f"""\n
{agent_name}.register_nested_chats(
    trigger={trigger_names},
    chat_queue={var_name},
)\n
"""
    functions_string = "\n".join(sorted(extra_contents))
    if functions_string:
        functions_string = functions_string + "\n"
    content = f"{functions_string}{content}"
    return (
        content.replace('"None"', "None")
        .replace("'None'", "None")
        .replace('"False"', "False")
        .replace("'False'", "False")
        .replace("'True'", "True")
        .replace('"True"', "True")
    )