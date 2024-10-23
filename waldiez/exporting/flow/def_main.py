"""Get the main function (if exporting to python)."""

from ..utils import (
    get_logging_start_string,
    get_logging_stop_string,
    get_sqlite_to_csv_call_string,
)


def get_def_main(waldiez_chats: str) -> str:
    """Get the main function.

    When exporting to python, waldiez_chats string will be the
    content of the main function. It contains either a
    `{sender.initiate_chat(recipient, ...)}` (if there is only one chat)
    or `initiate_chats([..])`, with the list of chats to initiate.

    Parameters
    ----------
    waldiez_chats : str
        The content of the main function.

    Returns
    -------
    str
        The main function.
    """
    content = """def main():
    # type: () -> Union[ChatResult, List[ChatResult]]
    \"\"\"Start chatting.\"\"\"
"""
    content += get_logging_start_string(1)
    content += f"    results = {waldiez_chats}" + "\n"
    content += get_logging_stop_string(1) + "\n"
    content += get_sqlite_to_csv_call_string(1) + "\n"
    content += "    return results\n"
    return content
