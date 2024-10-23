"""Get the `is_termination_message` check for the agent."""

from typing import Tuple

from waldiez.models import WaldiezAgent


def get_is_termination_message(
    agent: WaldiezAgent, agent_name: str
) -> Tuple[str, str]:
    """Get the `is_termination_message` argument and content (if any).

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_name : str
        The agent name.

    Returns
    -------
    Tuple[str, str]
        - The termination function name or lambda or None.
        - The termination function definition and content if any.

    Raises
    ------
    ValueError
        If the termination type is invalid.
    """
    if agent.data.termination.type == "none":
        return "None", ""
    if agent.data.termination.type == "keyword":
        return agent.data.termination.string, ""
    if agent.data.termination.type == "method":
        method_name = f"is_termination_message_{agent_name}"
        content = (
            "\n\n"
            + f"def is_termination_message_{agent_name}(message):"
            + "\n"
            + f"{agent.data.termination.string}"
            + "\n\n"
        )
        return method_name, content
    raise ValueError(f"Invalid termination type: {agent.data.termination.type}")
