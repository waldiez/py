"""Cleanup."""

# pylint: disable=duplicate-code,broad-except
import glob
import os
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

DIR_PATTERNS = [
    "__pycache__",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "*.egg-info",
    "htmlcov",
]

FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyc~",
    "*.py~",
    "*~",
    ".*~",
    ".DS_Store",
    "._DS_Store",
    "._.DS_Store",
    ".coverage*",
]

ROOT_LEVEL_DIRS = [
    "coding",
    "reports",
]


def _remove_dirs() -> None:
    for pattern in DIR_PATTERNS:
        for dirpath in glob.glob(f"./**/{pattern}", recursive=True):
            sys.stdout.write(f"removing {dirpath}\n")
            try:
                shutil.rmtree(dirpath)
            except BaseException:
                pass
    for dirname in ROOT_LEVEL_DIRS:
        directory = os.path.join(ROOT_DIR, dirname)
        if os.path.isdir(directory):
            sys.stdout.write(f"removing {dirname}\n")
            try:
                shutil.rmtree(directory)
            except BaseException:
                pass


def _remove_files() -> None:
    for pattern in FILE_PATTERNS:
        for filepath in glob.glob(f"./**/{pattern}", recursive=True):
            sys.stdout.write(f"removing {filepath}\n")
            os.remove(filepath)


def main() -> None:
    """Cleanup unnecessary files and directories."""
    _cwd = os.getcwd()
    os.chdir(ROOT_DIR)
    _remove_dirs()
    _remove_files()
    if os.getcwd() != _cwd:
        os.chdir(_cwd)


if __name__ == "__main__":
    main()
