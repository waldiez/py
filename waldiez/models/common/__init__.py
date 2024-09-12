"""Common utils for all models."""

from datetime import datetime, timezone

from .base import WaldieBase
from .method_utils import (
    METHOD_ARGS,
    METHOD_TYPE_HINTS,
    WaldieMethodName,
    check_function,
    parse_code_string,
)


def now() -> str:
    """Get the current date and time in UTC.

    Returns
    -------
    str
        The current date and time in UTC.
    """
    return (
        datetime.now(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


__all__ = [
    "WaldieBase",
    "METHOD_ARGS",
    "METHOD_TYPE_HINTS",
    "WaldieMethodName",
    "now",
    "check_function",
    "parse_code_string",
]
