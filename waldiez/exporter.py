"""Waldiez exporter.

The role of the exporter is to export the model's data
to an autogen's flow with one or more chats.

The resulting file(s): a `flow.py` file with one `main()` function
to trigger the chat(s).
If additional tools/skills are used,
they are exported as their `skill_name` in the same directory with
the `flow.py` file. So the `flow.py` could have entries like:
`form {skill1_name} import {skill1_name}`
`form {skill2_name} import {skill2_name}`
"""

# pylint: disable=inconsistent-quotes

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

from .exporting import comment, export_flow, get_valid_instance_name
from .models import (
    Waldiez,
    WaldiezAgent,
    WaldiezChat,
    WaldiezModel,
    WaldiezSkill,
)


class WaldiezExporter:
    """Waldiez exporter.

    Attributes:
        waldiez (Waldiez): The Waldiez instance.
    """

    _agent_names: Dict[str, str]
    _model_names: Dict[str, str]
    _skill_names: Dict[str, str]
    _chat_names: Dict[str, str]
    _chats: List[WaldiezChat]
    _skills: List[WaldiezSkill]
    _models: List[WaldiezModel]
    _agents: List[WaldiezAgent]

    def __init__(self, waldiez: Waldiez) -> None:
        """Initialize the Waldiez exporter.

        Parameters:
            waldiez (Waldiez): The Waldiez instance.
        """
        self.waldiez = waldiez
        self._initialize()

    @classmethod
    def load(cls, file_path: Path) -> "WaldiezExporter":
        """Load the Waldiez instance from a file.

        Parameters
        ----------
        file_path : Path
            The file path.

        Returns
        -------
        WaldiezExporter
            The Waldiez exporter.
        """
        waldiez = Waldiez.load(file_path)
        return cls(waldiez)

    def _initialize(
        self,
    ) -> None:
        """Get all the names in the flow.

        We need to make sure that no duplicate names are used,
        and that the names can be used as python variables.
        """
        all_names: Dict[str, str] = {}
        agent_names: Dict[str, str] = {}
        model_names: Dict[str, str] = {}
        skill_names: Dict[str, str] = {}
        chat_names: Dict[str, str] = {}
        chats: List[WaldiezChat] = []
        skills: List[WaldiezSkill] = []
        models: List[WaldiezModel] = []
        agents: List[WaldiezAgent] = []
        for agent in self.waldiez.agents:
            all_names = get_valid_instance_name(
                (agent.id, agent.name), all_names, prefix="wa"
            )
            agent_names[agent.id] = all_names[agent.id]
            agents.append(agent)
        for model in self.waldiez.models:
            all_names = get_valid_instance_name(
                (model.id, model.name), all_names, prefix="wm"
            )
            model_names[model.id] = all_names[model.id]
            models.append(model)
        for skill in self.waldiez.skills:
            all_names = get_valid_instance_name(
                (skill.id, skill.name), all_names, prefix="ws"
            )
            skill_names[skill.id] = all_names[skill.id]
            skills.append(skill)
        for chat in self.waldiez.flow.data.chats:
            all_names = get_valid_instance_name(
                (chat.id, chat.name), all_names, prefix="wc"
            )
            chat_names[chat.id] = all_names[chat.id]
            chats.append(chat)
        self._agent_names = agent_names
        self._model_names = model_names
        self._skill_names = skill_names
        self._chat_names = chat_names
        self._chats = chats
        self._skills = skills
        self._models = models
        self._agents = agents

    def export(self, path: Union[str, Path], force: bool = False) -> None:
        """Export the Waldiez instance.

        Parameters
        ----------
        path : Union[str, Path]
            The path to export to.
        force : bool, optional
            Override the output file if it already exists, by default False.

        Raises
        ------
        FileExistsError
            If the file already exists and force is False.
        IsADirectoryError
            If the output is a directory.
        ValueError
            If the file extension is invalid.
        """
        if not isinstance(path, Path):
            path = Path(path)
        path = path.resolve()
        if path.is_dir():
            raise IsADirectoryError(f"Output is a directory: {path}")
        if path.exists():
            if force is False:
                raise FileExistsError(f"File already exists: {path}")
            path.unlink(missing_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        extension = path.suffix
        if extension == ".waldiez":
            self.to_waldiez(path)
        elif extension == ".py":
            self.to_py(path)
        elif extension == ".ipynb":
            self.to_ipynb(path)
        else:
            raise ValueError(f"Invalid extension: {extension}")

    def to_ipynb(self, path: Path) -> None:
        """Export flow to jupyter notebook.

        Parameters
        ----------
        path : Path
            The path to export to.

        Raises
        ------
        RuntimeError
            If the notebook could not be generated.
        """
        content = f"{comment(True)}{self.waldiez.name}" + "\n\n"
        content += f"{comment(True, 2)}Dependencies" + "\n\n"
        content += "import sys\n"
        requirements = " ".join(self.waldiez.requirements)
        if requirements:
            content += (
                f"# !{{sys.executable}} -m pip install -q {requirements}" + "\n"
            )
        content += export_flow(
            waldiez=self.waldiez,
            agents=(self._agents, self._agent_names),
            chats=(self._chats, self._chat_names),
            models=(self._models, self._model_names),
            skills=(self._skills, self._skill_names),
            output_dir=path.parent,
            notebook=True,
        )
        # we first create a .py file with the content
        # and then convert it to a notebook using jupytext
        py_path = path.with_suffix(".tmp.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(content)
        if not shutil.which("jupytext"):  # pragma: no cover
            run_command(
                [sys.executable, "-m", "pip", "install", "jupytext"],
                allow_error=False,
            )
        run_command(
            ["jupytext", "--to", "notebook", str(py_path)],
            allow_error=False,
        )
        ipynb_path = str(py_path).replace(".tmp.py", ".tmp.ipynb")
        if not os.path.exists(ipynb_path):  # pragma: no cover
            raise RuntimeError("Could not generate notebook")
        Path(ipynb_path).rename(ipynb_path.replace(".tmp.ipynb", ".ipynb"))
        py_path.unlink(missing_ok=True)

    def to_py(self, path: Path) -> None:
        """Export waldiez flow to python script.

        Parameters
        ----------
        path : Path
            The path to export to.
        """
        content = "#!/usr/bin/env python\n"
        content += f'"""{self.waldiez.name}\n\n'
        content += f"{self.waldiez.description}\n\n"
        content += f"Tags: {', '.join(self.waldiez.tags)}\n\n"
        content += f"Requirements: {', '.join(self.waldiez.requirements)}\n\n"
        content += '"""\n\n'
        content += "# cspell: disable\n"
        content += "# flake8: noqa\n\n"
        content += export_flow(
            waldiez=self.waldiez,
            agents=(self._agents, self._agent_names),
            chats=(self._chats, self._chat_names),
            models=(self._models, self._model_names),
            skills=(self._skills, self._skill_names),
            output_dir=path.parent,
            notebook=False,
        )
        content += '\n\nif __name__ == "__main__":\n'
        content += "    print(main())\n"
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    def to_waldiez(self, file_path: Path) -> None:
        """Export the Waldiez instance.

        Parameters
        ----------
        file_path : Path
            The file path.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.waldiez.model_dump_json())


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    allow_error: bool = True,
) -> None:
    """Run a command.

    Parameters
    ----------
    cmd : List[str]
        The command to run.
    cwd : Path, optional
        The working directory, by default None (current working directory).
    allow_error : bool, optional
        Whether to allow errors, by default True.

    Raises
    ------
    RuntimeError
        If the command fails and allow_error is False.
    """
    if not cwd:
        cwd = Path.cwd()
    # pylint: disable=broad-except
    try:
        subprocess.run(
            cmd,
            check=True,
            cwd=cwd,
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # nosemgrep # nosec
    except BaseException as error:  # pragma: no cover
        if allow_error:
            return
        raise RuntimeError(f"Error running command: {error}") from error
