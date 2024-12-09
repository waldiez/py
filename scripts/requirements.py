"""Generate requirements/*txt files from pyproject.toml."""

# type: ignore[unused-ignore]

# pylint: disable=import-error,import-outside-toplevel,too-few-public-methods,broad-except
# isort: skip_file
import os
import subprocess  # nosemgrep # nosec
import sys
from pathlib import Path
from typing import Any, Dict, Protocol


ROOT_DIR = Path(__file__).parent.parent
EXTRAS = [
    "dev",
    "test",
    "docs",
    "ag2_extras",
]

# toml uses 'r' mode, tomllib uses 'rb' mode
OPEN_MODE = "rb" if sys.version_info >= (3, 11) else "r"


class TomlLoader(Protocol):
    """Protocol for TOML loaders."""

    def __call__(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Load TOML data from a file."""


def get_loader() -> TomlLoader:
    """Get the TOML loader.

    Returns
    -------
    TomlLoader
        TOML loader function.

    Raises
    ------
    ImportError
        If the TOML library is not found and cannot be installed.
    """
    if sys.version_info >= (3, 11):
        import tomllib  # noqa

        return tomllib.load
    try:
        import toml  # noqa

        return toml.load
    except ImportError as error:
        print("`toml` library not found. Installing it now...")
        try:
            subprocess.check_call(  # nosemgrep # nosec
                [sys.executable, "-m", "pip", "install", "toml"],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            import toml  # noqa

            return toml.load
        except BaseException:
            try:
                subprocess.check_call(  # nosemgrep # nosec
                    [sys.executable, "-m", "pip", "install", "--user", "toml"],
                )
                import toml  # noqa

                return toml.load
            except Exception as err:
                raise ImportError(
                    "Failed to install the `toml` library. "
                    f"Please install it manually.\nError: {err}"
                ) from err
        raise ImportError("Failed to import the `toml` library.") from error


def _write_all_dot_txt() -> None:
    """Generate requirements/all.txt with references to all requirements."""
    items = EXTRAS + ["main"]
    items.sort()
    with open("requirements/all.txt", "w", encoding="utf-8") as file:
        for item in items:
            file.write(f"-r {item}.txt\n")


def _write_requirements_txt(toml_data: Dict[str, Any], extra: str) -> None:
    """Write requirements/*.txt file.

    Parameters
    ----------
    toml_data : Dict[str, Any]
        The parsed pyproject.toml data.
    extra : str
        The extra or main to write the requirements file for.
    """
    if extra == "main":
        requirements = toml_data["project"]["dependencies"]
    else:
        requirements = toml_data["project"]["optional-dependencies"][extra]
    if not requirements:
        return
    with open(f"requirements/{extra}.txt", "w", encoding="utf-8") as file:
        if extra != "main":
            file.write("-r main.txt\n")
        for requirement in sorted(requirements):
            file.write(f"{requirement}\n")


def main() -> None:
    """Generate requirements/*txt files from pyproject.toml."""
    loader = get_loader()
    py_project_toml = ROOT_DIR / "pyproject.toml"
    with open(py_project_toml, OPEN_MODE) as f:
        py_project_dict = loader(f)
    if not os.path.exists(ROOT_DIR / "requirements"):
        os.makedirs(ROOT_DIR / "requirements")
    to_write = ["main"] + EXTRAS
    for item in to_write:
        _write_requirements_txt(py_project_dict, item)
    _write_all_dot_txt()
    print("Done. Generated:")
    for file in os.listdir("requirements"):
        print(f"  - {file}")


if __name__ == "__main__":
    main()
