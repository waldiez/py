"""Test waldiez.exporting.utils.logging_utils.*."""

# pylint: disable=inconsistent-quotes, line-too-long

from waldiez.exporting.utils.logging_utils import (
    get_logging_start_string,
    get_logging_stop_string,
    get_sqlite_to_csv_call_string,
    get_sqlite_to_csv_string,
)


def test_get_logging_start_string() -> None:
    """Test get_logging_start_string."""
    # Given
    tabs = 0
    # When
    result = get_logging_start_string(tabs)
    # Then
    assert result == (
        "runtime_logging.start(\n"
        '    logger_type="sqlite",\n'
        '    config={"dbname": "flow.db"},\n'
        ")\n"
    )
    # Given
    tabs = 1
    # When
    result = get_logging_start_string(tabs)
    # Then
    assert result == (
        "    runtime_logging.start(\n"
        '        logger_type="sqlite",\n'
        '        config={"dbname": "flow.db"},\n'
        "    )\n"
    )


def test_get_logging_stop_string() -> None:
    """Test get_logging_stop_string."""
    # Given
    tabs = 0
    # When
    result = get_logging_stop_string(tabs)
    # Then
    assert result == "runtime_logging.stop()\n"
    # Given
    tabs = 1
    # When
    result = get_logging_stop_string(tabs)
    # Then
    assert result == "    runtime_logging.stop()\n"


def test_get_sqlite_to_csv_call_string() -> None:
    """Test get_sqlite_to_csv_call_string."""
    # Given
    tabs = 0
    # When
    result = get_sqlite_to_csv_call_string(tabs)
    # Then
    assert result == (
        'if not os.path.exists("logs"):\n'
        '    os.makedirs("logs")\n'
        "for table in [\n"
        '    "chat_completions",\n'
        '    "agents",\n'
        '    "oai_wrappers",\n'
        '    "oai_clients",\n'
        '    "version",\n'
        '    "events",\n'
        '    "function_calls",\n'
        "]:\n"
        '    dest = os.path.join("logs", f"{table}.csv")\n'
        '    sqlite_to_csv("flow.db", table, dest)\n'
    )


def test_get_sqlite_to_csv_string() -> None:
    """Test get_sqlite_to_csv_string."""
    # When
    result = get_sqlite_to_csv_string()
    # Then
    assert result == (
        "\n\n"
        "def sqlite_to_csv(dbname: str, table: str, csv_file: str) -> None:\n"
        '    """Convert a sqlite table to a csv file.\n\n'
        "    Parameters\n"
        "    ----------\n"
        "    dbname : str\n"
        "        The sqlite database name.\n"
        "    table : str\n"
        "        The table name.\n"
        "    csv_file : str\n"
        "        The csv file name.\n"
        '    """\n'
        "    conn = sqlite3.connect(dbname)\n"
        '    query = f"SELECT * FROM {table}"  # nosec\n'
        "    try:\n"
        "        cursor = conn.execute(query)\n"
        "    except sqlite3.OperationalError:\n"
        "        conn.close()\n"
        "        return\n"
        "    rows = cursor.fetchall()\n"
        "    column_names = [description[0] for description "
        "in cursor.description]\n"
        "    data = [dict(zip(column_names, row)) for row in rows]\n"
        "    conn.close()\n"
        '    with open(csv_file, "w", newline="", encoding="utf-8") as file:\n'
        "        _csv_writer = csv.DictWriter(file, fieldnames=column_names)\n"
        "        _csv_writer.writeheader()\n"
        "        _csv_writer.writerows(data)\n"
        "\n\n"
    )
