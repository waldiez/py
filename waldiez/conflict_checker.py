"""Check for conflicts with 'autogen-agentchat' package."""

# pylint: disable=line-too-long

import sys
from importlib.metadata import PackageNotFoundError, version


# fmt: off
def check_conflicts() -> None:  # pragma: no cover
    """Check for conflicts with 'autogen-agentchat' package."""
    try:
        version("autogen-agentchat")
        print(
            "Conflict detected: 'autogen-agentchat' is installed, "
            "which conflicts with 'ag2' / 'pyautogen'.\n"
            "Please uninstall 'autogen-agentchat': pip uninstall -y autogen-agentchat \n"
            "And install 'pyautogen' (or 'waldiez') again: pip install --force pyautogen waldiez"
        )
        sys.exit(1)
    except PackageNotFoundError:
        pass

# fmt: on
