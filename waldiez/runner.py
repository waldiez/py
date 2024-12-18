"""Waldiez Flow runner.

Run a waldiez flow.
The flow is first converted to an autogen flow with agents, chats and skills.
We then chown to temporary directory, call the flow's `main()` and
return the results. Before running the flow, any additional environment
variables specified in the waldiez file are set.
"""

# pylint: disable=import-outside-toplevel,reimported

import datetime
import importlib.util
import io
import os
import shutil
import site
import subprocess  # nosemgrep # nosec
import sys
import tempfile
import warnings
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from .exporter import WaldiezExporter
from .models.waldiez import Waldiez

if TYPE_CHECKING:
    from autogen import ChatResult  # type: ignore


@contextmanager
def _chdir(to: Union[str, Path]) -> Iterator[None]:
    """Change the current working directory in a context.

    Parameters
    ----------
    to : Union[str, Path]
        The directory to change to.

    Yields
    ------
    Iterator[None]
        The context manager.
    """
    old_cwd = str(os.getcwd())
    os.chdir(to)
    try:
        yield
    finally:
        os.chdir(old_cwd)


class WaldiezRunner:
    """Waldiez runner class."""

    def __init__(
        self, waldiez: Waldiez, file_path: Optional[Union[str, Path]] = None
    ) -> None:
        """Initialize the Waldiez manager."""
        self._waldiez = waldiez
        self._running = False
        self._file_path = file_path
        self._exporter = WaldiezExporter(waldiez)
        self._called_install_requirements = False

    @classmethod
    def load(
        cls,
        waldiez_file: Union[str, Path],
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        requirements: Optional[List[str]] = None,
    ) -> "WaldiezRunner":
        """Create a WaldiezRunner instance from a file.

        Parameters
        ----------
        waldiez_file : Union[str, Path]
            The file path.
        name : Optional[str], optional
            The name of the Waldiez, by default None.
        description : Optional[str], optional
            The description of the Waldiez, by default None.
        tags : Optional[List[str]], optional
            The tags of the Waldiez, by default None.
        requirements : Optional[List[str]], optional
            The requirements of the Waldiez, by default None.

        Returns
        -------
        WaldiezRunner
            The Waldiez runner instance.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        RuntimeError
            If the file is not a valid Waldiez file.
        """
        waldiez = Waldiez.load(
            waldiez_file,
            name=name,
            description=description,
            tags=tags,
            requirements=requirements,
        )
        return cls(waldiez, file_path=waldiez_file)

    def __enter__(
        self,
    ) -> "WaldiezRunner":
        """Enter the context manager."""
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        """Exit the context manager."""
        if self._running:
            self._running = False

    @property
    def waldiez(self) -> Waldiez:
        """Get the Waldiez instance."""
        return self._waldiez

    @property
    def running(self) -> bool:
        """Get the running status."""
        return self._running

    def install_requirements(self) -> None:
        """Install the requirements for the flow."""
        self._called_install_requirements = True
        printer = get_printer()
        extra_requirements = set(
            req for req in self.waldiez.requirements if req not in sys.modules
        )
        if extra_requirements:
            printer(f"Installing requirements: {', '.join(extra_requirements)}")
            pip_install = [sys.executable, "-m", "pip", "install"]
            if not in_virtualenv():
                pip_install.append("--user")
            pip_install.extend(extra_requirements)
            with subprocess.Popen(
                pip_install,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) as proc:
                if proc.stdout:
                    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                        printer(line.strip())
                if proc.stderr:
                    for line in io.TextIOWrapper(proc.stderr, encoding="utf-8"):
                        printer(line.strip())
            refresh_environment()

    @staticmethod
    def _after_run(
        temp_dir: Path,
        output_path: Optional[Union[str, Path]],
        printer: Callable[..., None],
    ) -> None:
        if output_path:
            destination_dir = Path(output_path).parent
            destination_dir = (
                destination_dir
                / "waldiez_out"
                / datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            )
            destination_dir.mkdir(parents=True, exist_ok=True)
            # copy the contents of the temp dir to the destination dir
            printer(f"Copying the results to {destination_dir}")
            for item in temp_dir.iterdir():
                # skip cache files
                if (
                    item.name.startswith("__pycache__")
                    or item.name.endswith(".pyc")
                    or item == ".cache"
                ):
                    continue
                if item.is_file():
                    shutil.copy(item, destination_dir)
                else:
                    shutil.copytree(item, destination_dir / item.name)
        shutil.rmtree(temp_dir)

    def _set_env_vars(self) -> Dict[str, str]:
        """Set environment variables and return the old ones (if any)."""
        old_vars: Dict[str, str] = {}
        for var_key, var_value in self.waldiez.get_flow_env_vars():
            if var_key:
                current = os.environ.get(var_key, "")
                old_vars[var_key] = current
                os.environ[var_key] = var_value
        return old_vars

    @staticmethod
    def _reset_env_vars(old_vars: Dict[str, str]) -> None:
        """Reset the environment variables."""
        for var_key, var_value in old_vars.items():
            if not var_value:
                os.environ.pop(var_key, "")
            else:
                os.environ[var_key] = var_value

    def _do_run(
        self,
        output_path: Optional[Union[str, Path]],
        uploads_root: Optional[Union[str, Path]],
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow.

        Parameters
        ----------
        output_path : Optional[Union[str, Path]]
            The output path.
        uploads_root : Optional[Union[str, Path]]
            The runtime uploads root.

        Returns
        -------
        Union[ChatResult, List[ChatResult]]
            The result(s) of the chat(s).
        """
        if not self._called_install_requirements:
            self.install_requirements()
        else:
            refresh_environment()
        printer = get_printer()
        printer(
            "Requirements installed.\n"
            "NOTE: If new packages were added and you are using Jupyter, "
            "you might need to restart the kernel."
        )
        results: Union["ChatResult", List["ChatResult"]] = []
        if not uploads_root:
            uploads_root = Path(tempfile.mkdtemp())
        else:
            uploads_root = Path(uploads_root)
        if not uploads_root.exists():
            uploads_root.mkdir(parents=True)
        temp_dir = Path(tempfile.mkdtemp())
        file_name = "flow.py" if not output_path else Path(output_path).name
        if file_name.endswith((".json", ".waldiez")):
            file_name = file_name.replace(".json", ".py").replace(
                ".waldiez", ".py"
            )
        if not file_name.endswith(".py"):
            file_name += ".py"
        module_name = file_name.replace(".py", "")
        with _chdir(to=temp_dir):
            self._exporter.export(Path(file_name))
            spec = importlib.util.spec_from_file_location(
                module_name, temp_dir / file_name
            )
            if not spec or not spec.loader:
                raise ImportError("Could not import the flow")
            sys.path.insert(0, str(temp_dir))
            old_vars = self._set_env_vars()
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            printer("<Waldiez> - Starting workflow...")
            results = module.main()
            sys.path.pop(0)
            self._reset_env_vars(old_vars)
        self._after_run(temp_dir, output_path, printer)
        return results

    def run(
        self,
        output_path: Optional[Union[str, Path]] = None,
        uploads_root: Optional[Union[str, Path]] = None,
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow.

        Parameters
        ----------
        output_path : Optional[Union[str, Path]], optional
            The output path, by default None.
        uploads_root : Optional[Union[str, Path]], optional
            The uploads root, to get user-uploaded files, by default None.

        Returns
        -------
        Union[ChatResult, List[ChatResult]]
            The result(s) of the chat(s).

        Raises
        ------
        RuntimeError
            If the workflow is already running.
        """
        if self._running is True:
            raise RuntimeError("Workflow already running")
        self._running = True
        file_path = output_path or self._file_path
        try:
            return self._do_run(file_path, uploads_root)
        finally:
            self._running = False


def in_virtualenv() -> bool:
    """Check if we are inside a virtualenv.

    Returns
    -------
    bool
        True if inside a virtualenv, False otherwise.
    """
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def refresh_environment() -> None:
    """Refresh the environment."""
    # backup the default IOStream
    from autogen.io import IOStream  # type: ignore

    default_io_stream = IOStream.get_default()
    site.main()
    # pylint: disable=import-outside-toplevel
    modules_to_reload = [
        mod for mod in sys.modules if mod.startswith("autogen")
    ]
    for mod in modules_to_reload:
        del sys.modules[mod]
    import autogen
    from autogen.io import IOStream

    importlib.reload(autogen)
    # restore the default IOStream
    IOStream.set_global_default(default_io_stream)
    warnings.filterwarnings("ignore", "flaml.automl is not available")


def get_printer() -> Callable[..., None]:
    """Get the printer function.

    Returns
    -------
    Callable[..., None]
        The printer function.
    """
    from autogen.io import IOStream

    printer = IOStream.get_default().print

    def safe_printer(*args: object, **kwargs: object) -> None:
        try:
            printer(*args, **kwargs)
        except UnicodeEncodeError:
            # pylint: disable=too-many-try-statements
            try:
                msg, flush = get_what_to_print(*args, **kwargs)
                printer(msg, end="", flush=flush)
            except UnicodeEncodeError:
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer, encoding="utf-8"
                )
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer, encoding="utf-8"
                )
                try:
                    printer(*args, **kwargs)
                except UnicodeEncodeError:
                    sys.stderr.write(
                        "Could not print the message due to encoding issues.\n"
                    )

    return safe_printer


def get_what_to_print(*args: object, **kwargs: object) -> Tuple[str, bool]:
    """Get what to print.

    Parameters
    ----------
    args : object
        The arguments.
    kwargs : object
        The keyword arguments.

    Returns
    -------
    Tuple[str, bool]
        The message and whether to flush.
    """
    sep = kwargs.get("sep", " ")
    if not isinstance(sep, str):
        sep = " "
    end = kwargs.get("end", "\n")
    if not isinstance(end, str):
        end = "\n"
    flush = kwargs.get("flush", False)
    if not isinstance(flush, bool):
        flush = False
    msg = sep.join(str(arg) for arg in args) + end
    utf8_msg = msg.encode("utf-8", errors="replace").decode("utf-8")
    return utf8_msg, flush
