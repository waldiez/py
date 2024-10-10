"""If eclint is installed, run it on the root of the repository.

https://gitlab.com/greut/eclint
go install gitlab.com/greut/eclint/cmd/eclint
"""

import os
import shutil
import subprocess  # nosemgrep # nosec
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def main() -> None:
    """Run eclint."""
    os.chdir(ROOT_DIR)
    eclint = shutil.which("eclint")
    if not eclint:
        print("eclint is not installed.")
        return
    subprocess.run(  # nosemgrep # nosec
        [eclint, "-v", "2"],
        check=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


if __name__ == "__main__":
    main()
