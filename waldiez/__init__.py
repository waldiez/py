"""Waldiez package."""

import logging
import warnings

from ._version import __version__
from .conflict_checker import check_conflicts
from .exporter import WaldiezExporter
from .models import Waldiez
from .runner import WaldiezRunner

warnings.filterwarnings("ignore", "flaml.automl is not available")


# pylint: disable=too-few-public-methods
class FlamlFilter(logging.Filter):
    """Filter out flaml.automl is not available message."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out flaml.automl is not available message.

        this is just annoying:

        ```
        flaml.automl is not available.
        Please install flaml[automl] to enable AutoML functionalities.
        ```

        Parameters
        ----------
        record : logging.LogRecord
            Log record to filter.

        Returns
        -------
        bool
            Whether to filter out the log record.
        """
        return "flaml.automl is not available" not in record.getMessage()


# flag to check if ag2 and autogen-agentchat
# are installed at the same time
__WALDIEZ_CHECKED_FOR_CONFLICTS = False
# flag to handle flaml logging
# suppress the annoying message about flaml.automl
__WALDIEZ_HANDLED_FLAML_LOGGING = False


def _check_conflicts() -> None:
    """Check for conflicts once."""
    # pylint: disable=global-statement
    global __WALDIEZ_CHECKED_FOR_CONFLICTS
    if __WALDIEZ_CHECKED_FOR_CONFLICTS is False:
        check_conflicts()
        __WALDIEZ_CHECKED_FOR_CONFLICTS = True


def _handle_flaml_logging() -> None:
    """Handle flaml logging once."""
    # pylint: disable=global-statement
    global __WALDIEZ_HANDLED_FLAML_LOGGING
    if __WALDIEZ_HANDLED_FLAML_LOGGING is False:
        __WALDIEZ_HANDLED_FLAML_LOGGING = True
        flam_logger = logging.getLogger("flaml")
        flam_logger.addFilter(FlamlFilter())


_check_conflicts()
_handle_flaml_logging()

__all__ = [
    "Waldiez",
    "WaldiezExporter",
    "WaldiezRunner",
    "__version__",
]
