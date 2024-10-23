"""Function related utilities."""

import ast
from typing import Dict, List, Literal, Optional, Tuple

WaldiezMethodName = Literal[
    "callable_message",  # Chat
    "is_termination_message",  # Agent
    "nested_chat_message",  # Agents' NestedChat
    "nested_chat_reply",  # Agents' NestedChat
    "custom_speaker_selection",  # GroupChat
    "custom_embedding_function",  # RAG
    "custom_token_count_function",  # RAG
    "custom_text_split_function",  # RAG
]

METHOD_ARGS: Dict[WaldiezMethodName, List[str]] = {
    "callable_message": ["sender", "recipient", "context"],
    "is_termination_message": ["message"],
    "nested_chat_message": ["recipient", "messages", "sender", "config"],
    "nested_chat_reply": ["recipient", "messages", "sender", "config"],
    "custom_speaker_selection": ["last_speaker", "groupchat"],
    "custom_embedding_function": [],
    "custom_token_count_function": ["text", "model"],
    "custom_text_split_function": [
        "text",
        "max_tokens",
        "chunk_mode",
        "must_break_at_empty_line",
        "overlap",
    ],
}

# pylint: disable=line-too-long
METHOD_TYPE_HINTS: Dict[WaldiezMethodName, str] = {
    "callable_message": "# type: (ConversableAgent, ConversableAgent, dict) -> Union[dict, str]",
    "is_termination_message": "# type: (dict) -> bool",
    "nested_chat_message": "# type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]",
    "nested_chat_reply": "# type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]",
    "custom_speaker_selection": "# type: (ConversableAgent, GroupChat) -> Union[Agent, str, None]",
    "custom_embedding_function": "# type: () -> Callable[..., Any]",
    "custom_token_count_function": "# type: (str, str) -> int",
    "custom_text_split_function": "# type: (str, int, str, bool, int) -> List[str]",
}


def parse_code_string(
    code_string: str,
) -> Tuple[Optional[str], Optional[ast.Module]]:
    """Parse the code string.

    Parameters
    ----------
    code_string : str
        The code string.

    Returns
    -------
    Tuple[Optional[str], Optional[ast.Module]]
        If valid, None and the ast module.
        If invalid, the error message and None.
    """
    # pylint: disable=broad-except
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return f"SyntaxError: {e}, in \n{code_string}", None
    except BaseException as e:  # pragma: no cover
        return f"Invalid code: {e}, in \n{code_string}", None
    return None, tree


def check_function(
    code_string: str,
    function_name: WaldiezMethodName,
    skip_type_hints: bool = False,
) -> Tuple[bool, str]:
    """Check the function.

    Parameters
    ----------
    code_string : str
        The code string.
    function_name : WaldiezMethodName
        The expected function name.
    skip_type_hints : bool, optional
        Whether to skip type hints in the function body, by default False.

    Returns
    -------
    Tuple[bool, str]
        If valid, True and the function body (only), no extra lines.
        If invalid, False and the error message.
    """
    error, tree = parse_code_string(code_string)
    if error is not None or tree is None:
        return False, error or "Invalid code"
    if function_name not in METHOD_ARGS:
        return False, f"Invalid function name: {function_name}"
    expected_method_args = METHOD_ARGS[function_name]
    return _get_function_body(
        tree,
        code_string,
        function_name,
        expected_method_args,
        skip_type_hints=skip_type_hints,
    )


def _get_function_body(
    tree: ast.Module,
    code_string: str,
    function_name: WaldiezMethodName,
    method_args: List[str],
    skip_type_hints: bool = False,
) -> Tuple[bool, str]:
    """Get the function body.

    Parameters
    ----------
    tree : ast.Module
        The ast module.
    code_string : str
        The code string.
    function_name : WaldiezMethodName
        The expected function name.
    method_args : List[str]
        The expected method arguments.

    Returns
    -------
    Tuple[bool, str]
        If valid, True and the function body (only), no extra lines.
        If invalid, False and the error message.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name != function_name:
                continue
            if len(node.args.args) != len(method_args):
                return (
                    False,
                    f"Invalid number of arguments in function {node.name}",
                )
            for arg, expected_arg in zip(node.args.args, method_args):
                if arg.arg != expected_arg:
                    return (
                        False,
                        f"Invalid argument name in function {node.name}",
                    )
            function_body_lines = code_string.splitlines()[
                node.lineno - 1 : node.end_lineno
            ]
            function_body = "\n".join(function_body_lines[1:])
            if not skip_type_hints:
                # add type hints after the function definition
                function_body = (
                    f"    {METHOD_TYPE_HINTS[function_name]}\n{function_body}"
                )
            return True, function_body
    error_msg = (
        f"No function with name `{function_name}`"
        f" and arguments `{method_args}` found"
    )
    return False, error_msg
