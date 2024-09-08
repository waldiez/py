"""Command line interface to convert or run a waldie file."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from autogen import ChatResult  # type: ignore[import-untyped]

from . import Waldie, __version__
from .exporter import WaldieExporter
from .runner import WaldieRunner


def get_parser() -> argparse.ArgumentParser:
    """Get the argument parser for the Waldie package.

    Returns
    -------
    argparse.ArgumentParser
        The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Run or export a Waldie flow.",
        prog="waldiez",
    )
    parser.add_argument(
        "waldie",
        type=str,
        help="Path to the Waldie flow (*.waldiez) file.",
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help="Export the Waldie flow to a Python script or a jupyter notebook.",
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
    """Log the result of the Waldie flow."""
    logger = logging.getLogger("waldiez::cli")
    logger.info("Chat History:\n")
    logger.info(result.chat_history)
    logger.info("Summary:\n")
    logger.info(result.summary)
    logger.info("Cost:\n")
    logger.info(result.cost)


def _run(data: Dict[str, Any], output_path: Optional[str]) -> None:
    """Run the Waldie flow."""
    waldie = Waldie.from_dict(data)
    runner = WaldieRunner(waldie)
    results = runner.run(stream=None, output_path=output_path)
    if isinstance(results, list):
        for result in results:
            _log_result(result)
            sep = "-" * 80
            print(f"\n{sep}\n")
    else:
        _log_result(results)


def main() -> None:
    """Parse the command line arguments and run the Waldie flow."""
    parser = get_parser()
    args = parser.parse_args()
    logger = _get_logger()
    waldie_file: str = args.waldie
    if not os.path.exists(waldie_file):
        logger.error("File not found: %s", waldie_file)
        sys.exit(1)
    if not waldie_file.endswith((".json", ".waldiez")):
        logger.error("Only .json or .waldiez files are supported.")
        sys.exit(1)
    with open(waldie_file, "r", encoding="utf-8") as file:
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
                "and JSON/Waldie files are supported."
            )
            sys.exit(1)
        output_file = Path(args.output).resolve()
        waldie = Waldie.from_dict(data)
        exporter = WaldieExporter(waldie)
        exporter.export(output_file, force=args.force)
        generated = str(output_file).replace(os.getcwd(), ".")
        logger.info("Generated: %s", generated)
    else:
        _run(data, args.output)


def _get_logger(level: int = logging.INFO) -> logging.Logger:
    """Get the logger for the Waldie package.

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
