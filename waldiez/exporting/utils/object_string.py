"""Function to convert an object to a formatted string with indentation.

To be used with dicts and/or lists.
"""

from typing import Any


def get_object_string(obj: Any, tabs: int = 1) -> str:
    """Convert an object to a formatted string with given indentation.

    Parameters
    ----------
    obj : Any
        The object to convert.
    tabs : int, optional
        The number of tabs, by default 1.

    Returns
    -------
    str
        The formatted string.

    Example
    -------
    ```python
    >>> obj = {"a": 1, "b": [1, 2, 3]}
    >>> get_object_string(obj)
    {
        "a": 1,
        "b": [
            1,
            2,
            3
        ]
    }
    >>> obj = {"a": 1, "b": [1, 2, 3], "c": {"d": 4}}
    >>> get_object_string(obj, 2)
    {
            "a": 1,
            "b": [
                1,
                2,
                3
            ],
            "c": {
                "d": 4
            }
    }
    ```
    """
    indent = " " * 4 * tabs  # Number of spaces corresponding to the tabs
    next_indent = (
        " " * 4 * (tabs + 1)
    )  # Number of spaces corresponding to the next tab level
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            items.append(
                f'{next_indent}"{key}": {get_object_string(value, tabs + 1)}'
            )
        # python3.10? f-string expression part cannot include a backslash
        items_string = ",\n".join(items)
        to_return = "\n" + items_string + "\n" + indent
        return f"{{{to_return}}}"
        # return f'{{\n{",\n".join(items)}\n{indent}}}'
    if isinstance(obj, list):
        items = []
        for item in obj:
            items.append(f"{next_indent}{get_object_string(item, tabs + 1)}")
        # python3.10? f-string expression part cannot include a backslash
        items_string = ",\n".join(items)
        to_return = "\n" + items_string + "\n" + indent
        return f"[{to_return}]"

    if isinstance(obj, str):
        if obj.startswith("r'") or obj.startswith('r"'):
            return obj
        return f'"{obj}"'

    if obj is None:
        return "None"
    return str(obj)
