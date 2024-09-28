"""Logging related string generation functions.

Functions
---------
get_logging_start_string
    Get the string to start logging.
get_logging_stop_string
    Get the string to stop logging.
get_sqlite_to_csv_string
    Get the sqlite to csv conversion code string.
get_sqlite_to_csv_call_string
    Get the string to call the sqlite to csv conversion.
"""


# Check issue:
# https://github.com/microsoft/autogen/issues/2286
# we cannot log new agents if they have code_execution enabled
# we get `Path` is not JSON serializable (on code_executor)
# pylint: disable=inconsistent-quotes
def get_logging_start_string(tabs: int = 0) -> str:
    """Get the logging start string.

    Parameters
    ----------
    tabs : int, optional
        The number of tabs to use for indentation, by default 0

    Returns
    -------
    str
        The logging start string.

    Example
    -------
    ```python
    >>> get_logging_start_string()
    runtime_logging.start(
        logger_type="sqlite",
        config={"dbname": "flow.db"},
    )
    ```
    """
    tab = "    " * tabs
    content = f"{tab}runtime_logging.start(\n"
    content += f'{tab}    logger_type="sqlite",\n'
    content += f'{tab}    config={{"dbname": "flow.db"}},\n'
    content += f"{tab})\n"
    return content


def get_logging_stop_string(tabs: int = 0) -> str:
    """Get the logging stop string.

    Parameters
    ----------
    tabs : int, optional
        The number of tabs to use for indentation, by default 0

    Returns
    -------
    str
        The logging stop string

    Example
    -------
    ```python
    >>> get_logging_stop_string()
    runtime_logging.stop()
    ```
    """
    tab = "    " * tabs
    return f"{tab}runtime_logging.stop()\n"


# pylint: disable=differing-param-doc,differing-type-doc
def get_sqlite_to_csv_string() -> str:
    """Get the sqlite to csv conversion code string.

    Returns
    -------
    str
        The sqlite to csv conversion code string.

    Example
    -------
    ```python
    >>> get_sqlite_to_csv_string()
    def sqlite_to_csv(dbname: str, table: str, csv_file: str) -> None:
        \"\"\"Convert a sqlite table to a csv file.

        Parameters
        ----------
        dbname : str
            The sqlite database name.
        table : str
            The table name.
        csv_file : str
            The csv file name.
        \"\"\"
        conn = sqlite3.connect(dbname)
        query = f"SELECT * FROM {table}"  # nosec
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        conn.close()
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            _csv_writer = csv.DictWriter(file, fieldnames=column_names)
            _csv_writer.writeheader()
            _csv_writer.writerows(data)
    ```
    """
    content = "\n\n"
    content += (
        "def sqlite_to_csv(dbname: str, table: str, csv_file: str) -> None:\n"
    )
    content += '    """Convert a sqlite table to a csv file.\n\n'
    content += "    Parameters\n"
    content += "    ----------\n"
    content += "    dbname : str\n"
    content += "        The sqlite database name.\n"
    content += "    table : str\n"
    content += "        The table name.\n"
    content += "    csv_file : str\n"
    content += "        The csv file name.\n"
    content += '    """\n'
    content += "    conn = sqlite3.connect(dbname)\n"
    content += '    query = f"SELECT * FROM {table}"  # nosec\n'
    content += "    try:\n"
    content += "        cursor = conn.execute(query)\n"
    content += "    except sqlite3.OperationalError:\n"
    content += "        conn.close()\n"
    content += "        return\n"
    content += "    rows = cursor.fetchall()\n"
    content += "    column_names = [description[0] for description "
    content += "in cursor.description]\n"
    content += "    data = [dict(zip(column_names, row)) for row in rows]\n"
    content += "    conn.close()\n"
    content += (
        '    with open(csv_file, "w", newline="", encoding="utf-8") as file:\n'
    )
    content += (
        "        _csv_writer = csv.DictWriter(file, fieldnames=column_names)\n"
    )
    content += "        _csv_writer.writeheader()\n"
    content += "        _csv_writer.writerows(data)\n"
    content += "\n\n"
    return content


def get_sqlite_to_csv_call_string(tabs: int = 0) -> str:
    """Get the sqlite to csv conversion call string.

    Parameters
    ----------
    tabs : int, optional
        The number of tabs to use for indentation, by default 0

    Returns
    -------
    str
        The sqlite to csv conversion call string.

    Example
    -------
    ```python
    >>> get_sqlite_to_csv_call_string()
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
    ```
    """
    table_names = [
        "chat_completions",
        "agents",
        "oai_wrappers",
        "oai_clients",
        "version",
        "events",
        "function_calls",
    ]
    tab = "    " * tabs
    content = ""
    content += tab + 'if not os.path.exists("logs"):\n'
    content += tab + '    os.makedirs("logs")\n'
    content += tab + "for table in [\n"
    for table in table_names:
        content += tab + f'    "{table}",\n'
    content += tab + "]:\n"
    content += tab + '    dest = os.path.join("logs", f"{table}.csv")\n'
    content += tab + '    sqlite_to_csv("flow.db", table, dest)\n'
    return content
