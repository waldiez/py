"""Test waldiez.exporting.flow.def_main."""

from waldiez.exporting.flow.def_main import get_def_main


def test_get_def_main() -> None:
    """Test get_def_main."""
    waldiez_chats = "waldiez_chats"
    expected = """def main():
    # type: () -> Union[ChatResult, List[ChatResult]]
    \"\"\"Start chatting.\"\"\"
    results = waldiez_chats
    runtime_logging.stop()

    if not os.path.exists("logs"):
        os.makedirs("logs")
    for table in [
        "chat_completions",
        "agents",
        "oai_wrappers",
        "oai_clients",
        "version",
        "events",
        "function_calls",
    ]:
        dest = os.path.join("logs", f"{table}.csv")
        sqlite_to_csv("flow.db", table, dest)

    return results
"""
    assert get_def_main(waldiez_chats) == expected
