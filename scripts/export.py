"""Export the .waldiez files in examples to {.py,ipynb} files."""

import os
import subprocess  # nosemgrep # nosec
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

EXAMPLES_DIR = ROOT_DIR / "examples"


def main() -> None:
    """Export the .waldiez files in examples to {.py,ipynb} files."""
    os.chdir(ROOT_DIR)
    # do not check in .ipynb_checkpoints directories
    for example in EXAMPLES_DIR.glob("**/*.waldiez"):
        # do not check in .ipynb_checkpoints directories
        if ".ipynb_checkpoints" in str(example):
            continue
        example_path = example.resolve()
        example_name = example_path.stem
        example_dir = example_path.parent
        export_path = example_dir / f"{example_name}.ipynb"
        # print(f"Exporting {example_path} to {export_path}")
        subprocess.run(  # nosemgrep # nosec
            [
                sys.executable,
                "-m",
                "waldiez",
                "convert",
                "--file",
                str(example_path),
                "--output",
                str(export_path),
                "--force",
            ],
            check=True,
        )
        export_path = example_dir / f"{example_name}.py"
        # print(f"Exporting {example_path} to {export_path}")
        subprocess.run(  # nosemgrep # nosec
            # --export, --output, --force
            [
                sys.executable,
                "-m",
                "waldiez",
                "convert",
                "--file",
                str(example_path),
                "--output",
                str(export_path),
                "--force",
            ],
            check=True,
        )


if __name__ == "__main__":
    if EXAMPLES_DIR.exists():
        main()
