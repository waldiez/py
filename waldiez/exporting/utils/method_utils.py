"""Method related string generation utilities."""

from waldiez.models import METHOD_ARGS, WaldiezMethodName


def get_method_string(
    method_name: WaldiezMethodName, renamed_method_name: str, method_body: str
) -> str:
    """Get a function string.

    Parameters
    ----------
    method_name : WaldiezMethodName
        The method name.
    renamed_method_name : str
        The renamed method name.
    method_body : str
        The method body.

    Returns
    -------
    str
        The function string having the definition, type hints and body.
    """
    method_args = METHOD_ARGS[method_name]
    content = f"def {renamed_method_name}("
    if len(method_args) == 0:
        content += "):"
    else:
        content += "\n"
        for arg in method_args:
            content += f"    {arg},\n"
        content += "):"
    content += f"\n{method_body}"
    return content
