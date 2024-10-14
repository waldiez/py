"""Comment related string generation functions.
Functions
---------
comment
    Get a comment string.
get_comment
    Get a comment string for some common keys (notebook headings).
get_pylint_ignore_comment
    Get the pylint ignore comment string.
"""

from typing import List, Optional

from typing_extensions import Literal

PYLINT_RULES = [
    "line-too-long",
    "unknown-option-value",
    "unused-argument",
    "unused-import",
    "invalid-name",
    "import-error",
    "inconsistent-quotes",
    "missing-function-docstring",
    "missing-param-doc",
    "missing-return-doc",
]


def comment(notebook: bool, hashtags: int = 1) -> str:
    """Get the comment string.

    Parameters
    ----------
    notebook : bool
        Whether the comment is for a notebook or not.
    hashtags : int, optional
        The number of hashtags (for notebooks), by default 1.

    Returns
    -------
    str
        The comment string.
    Example
    -------
    ```python
    >>> comment(True, 2)
    '## '
    >>> comment(False)
    '# '
    ```
    """
    content = "# "
    if notebook:
        content += "#" * hashtags + " "
    return content


def get_comment(
    key: Literal["agents", "skills", "models", "nested", "run", "logging"],
    for_notebook: bool,
) -> str:
    """Get a comment string for some common keys.

    The key is a heading (in a notebook) or just a comment (in a script).

    Parameters
    ----------
    key : Literal["agents", "skills", "models", "nested", "run", "logging"]
        The key.
    for_notebook : bool
        Whether the comment is for a notebook.

    Returns
    -------
    str
        The comment string.

    Example
    -------
    ```python
    >>> get_comment("agents", True)

    '## Agents'
    >>> get_comment("skills", False)

    '# Skills'
    ```
    """
    # pylint: disable=too-many-return-statements
    if key == "agents":
        return "\n" + comment(for_notebook, 2) + "Agents\n"
    if key == "skills":
        return "\n" + comment(for_notebook, 2) + "Skills\n"
    if key == "models":
        return "\n" + comment(for_notebook, 2) + "Models\n"
    if key == "nested":
        return "\n" + comment(for_notebook, 2) + "Nested Chats\n"
    if key == "run":
        return "\n" + comment(for_notebook, 2) + "Run the flow\n"
    if key == "logging":
        return "\n" + comment(for_notebook, 2) + "Start Logging\n"
    return comment(for_notebook)


def get_pylint_ignore_comment(
    notebook: bool, rules: Optional[List[str]] = None
) -> str:
    """Get the pylint ignore comment string.

    Parameters
    ----------
    notebook : bool
        Whether the comment is for a notebook.
    rules : Optional[List[str]], optional
        The pylint rules to ignore, by default None.

    Returns
    -------
    str
        The pylint ignore comment string.

    Example
    -------
    ```python
    >>> get_pylint_ignore_comment(True, ["invalid-name", "line-too-long"])

    # pylint: disable=invalid-name, line-too-long
    ```
    """
    if not rules:
        rules = PYLINT_RULES
    line = "# pylint: disable=" + ",".join(rules)
    if notebook is True:
        line = "\n" + line
    return line + "\n"
