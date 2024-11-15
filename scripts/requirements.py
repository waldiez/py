"""Generate requirements/*txt files from pyproject.toml."""

import os
import shutil
import subprocess  # nosemgrep # nosec
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
EXTRAS = [
    "dev",
    "test",
    "docs",
    "ag2_extras",
]


def _write_all_dot_txt() -> None:
    """Generate requirements/all.txt with references to all requirements."""
    items = EXTRAS + ["main"]
    items.sort()
    with open("requirements/all.txt", "w", encoding="utf-8") as file:
        for item in items:
            file.write(f"-r {item}.txt\n")


def _ensure_uv() -> None:
    """Ensure that the `uv` tool is installed."""
    if not shutil.which("uv"):
        subprocess.run(  # nosemgrep # nosec
            ["python", "-m", "pip", "install", "uv"], check=True
        )
    try:
        subprocess.run(  # nosemgrep # nosec
            ["uv", "--version"], check=True, stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Failed to run `uv`.")
        print("Please make sure that the `uv` tool is installed.")
        print("You can install it using `python -m pip install uv`.")
        sys.exit(1)


def main() -> None:
    """Generate requirements/*txt files from pyproject.toml."""
    _ensure_uv()
    subprocess.run(  # nosemgrep # nosec
        [
            "uv",
            "pip",
            "compile",
            "pyproject.toml",
            "--output-file",
            "requirements/main.txt",
        ],
        check=True,
        cwd=str(ROOT_DIR),
    )
    for extra in EXTRAS:
        subprocess.run(  # nosemgrep # nosec
            [
                "uv",
                "pip",
                "compile",
                "pyproject.toml",
                "--output-file",
                f"requirements/{extra}.txt",
                f"--extra={extra}",
                "--no-deps",
                "--no-strip-extras",
            ],
            check=True,
            cwd=str(ROOT_DIR),
        )
    _write_all_dot_txt()
    print("Done. Generated:")
    for file in os.listdir("requirements"):
        print(f"  - {file}")


if __name__ == "__main__":
    main()
