"""Command line interface to convert or run a waldiez file."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from autogen import ChatResult  # type: ignore[import-untyped]

from . import Waldiez, __version__
from .exporter import WaldiezExporter
from .runner import WaldiezRunner


def get_parser() -> argparse.ArgumentParser:
    """Get the argument parser for the Waldiez package.

    Returns
    -------
    argparse.ArgumentParser
        The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Run or export a Waldiez flow.",
        prog="waldiez",
    )
    parser.add_argument(
        "waldiez",
        type=str,
        help="Path to the Waldiez flow (*.waldiez) file.",
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help=(
            "Export the Waldiez flow to a Python script or a jupyter notebook."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=(
            "Path to the output file. "
            "If exporting, the file extension determines the output format. "
            "If running, the output's directory will contain "
            "the generated flow (.py) and any additional generated files."
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help=("Override the output file if it already exists. "),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"waldiez version: {__version__}",
    )
    return parser


def _log_result(result: ChatResult) -> None:
    """Log the result of the Waldiez flow."""
    logger = logging.getLogger("waldiez::cli")
    logger.info("Chat History:\n")
    logger.info(result.chat_history)
    logger.info("Summary:\n")
    logger.info(result.summary)
    logger.info("Cost:\n")
    logger.info(result.cost)


def _run(data: Dict[str, Any], output_path: Optional[str]) -> None:
    """Run the Waldiez flow."""
    waldiez = Waldiez.from_dict(data)
    runner = WaldiezRunner(waldiez)
    results = runner.run(stream=None, output_path=output_path)
    if isinstance(results, list):
        for result in results:
            _log_result(result)
            sep = "-" * 80
            print(f"\n{sep}\n")
    else:
        _log_result(results)


def main() -> None:
    """Parse the command line arguments and run the Waldiez flow."""
    parser = get_parser()
    args = parser.parse_args()
    logger = _get_logger()
    waldiez_file: str = args.waldiez
    if not os.path.exists(waldiez_file):
        logger.error("File not found: %s", waldiez_file)
        sys.exit(1)
    if not waldiez_file.endswith((".json", ".waldiez")):
        logger.error("Only .json or .waldiez files are supported.")
        sys.exit(1)
    with open(waldiez_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.error("Invalid .waldiez file: %s. Not a valid json?", file)
            return
    if args.export is True:
        if args.output is None:
            logger.error("Please provide an output file.")
            sys.exit(1)
        if not args.output.endswith((".py", ".ipynb", ".json", ".waldiez")):
            logger.error(
                "Only Python scripts, Jupyter notebooks "
                "and JSON/Waldiez files are supported."
            )
            sys.exit(1)
        output_file = Path(args.output).resolve()
        waldiez = Waldiez.from_dict(data)
        exporter = WaldiezExporter(waldiez)
        exporter.export(output_file, force=args.force)
        generated = str(output_file).replace(os.getcwd(), ".")
        logger.info("Generated: %s", generated)
    else:
        _run(data, args.output)


def _get_logger(level: int = logging.INFO) -> logging.Logger:
    """Get the logger for the Waldiez package.

    Parameters
    ----------
    level : int or str, optional
        The logging level. Default is logging.INFO.

    Returns
    -------
    logging.Logger
        The logger.
    """
    # check if we already have setup a config

    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=level,
            format="%(levelname)s %(message)s",
            stream=sys.stderr,
            force=True,
        )
    logger = logging.getLogger("waldiez::cli")
    current_level = logger.getEffectiveLevel()
    if current_level != level:
        logger.setLevel(level)
    return logger


if __name__ == "__main__":
    main()
