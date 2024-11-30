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
            "Conflict detected: 'autogen-agentchat' is installed, which conflicts with 'ag2'.\n"
            "Please uninstall 'autogen-agentchat': pip uninstall -y autogen-agentchat \n"
            "And install 'ag2' (or 'waldiez') again: pip install --force ag2"
        )
        sys.exit(1)
    except PackageNotFoundError:
        pass

# fmt: on
