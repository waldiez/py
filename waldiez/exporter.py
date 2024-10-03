"""Waldie exporter.

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
from .models import WaldieAgent, WaldieChat, WaldieModel, WaldieSkill
from .waldie import Waldie


class WaldieExporter:
    """Waldie exporter.

    Attributes:
        waldie (Waldie): The Waldie instance.
    """

    _agent_names: Dict[str, str]
    _model_names: Dict[str, str]
    _skill_names: Dict[str, str]
    _chat_names: Dict[str, str]
    _chats: List[WaldieChat]
    _skills: List[WaldieSkill]
    _models: List[WaldieModel]
    _agents: List[WaldieAgent]

    def __init__(self, waldie: Waldie) -> None:
        """Initialize the Waldie exporter.

        Parameters:
            waldie (Waldie): The Waldie instance.
        """
        self.waldie = waldie
        self._initialize()

    @classmethod
    def load(cls, file_path: Path) -> "WaldieExporter":
        """Load the Waldie instance from a file.

        Parameters
        ----------
        file_path : Path
            The file path.

        Returns
        -------
        WaldieExporter
            The Waldie exporter.
        """
        waldie = Waldie.load(file_path)
        return cls(waldie)

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
        chats: List[WaldieChat] = []
        skills: List[WaldieSkill] = []
        models: List[WaldieModel] = []
        agents: List[WaldieAgent] = []
        for agent in self.waldie.agents:
            all_names = get_valid_instance_name(
                (agent.id, agent.name), all_names, prefix="wa"
            )
            agent_names[agent.id] = all_names[agent.id]
            agents.append(agent)
        for model in self.waldie.models:
            all_names = get_valid_instance_name(
                (model.id, model.name), all_names, prefix="wm"
            )
            model_names[model.id] = all_names[model.id]
            models.append(model)
        for skill in self.waldie.skills:
            all_names = get_valid_instance_name(
                (skill.id, skill.name), all_names, prefix="ws"
            )
            skill_names[skill.id] = all_names[skill.id]
            skills.append(skill)
        for chat in self.waldie.flow.data.chats:
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
        """Export the Waldie instance.

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
            path.unlink()
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        extension = path.suffix
        if extension == ".waldiez":
            self.to_waldie(path)
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
        include_retrieve_chat = self.waldie.has_rag_agents
        pip_install_autogen = (
            "# !{sys.executable} -m pip install -q 'pyautogen[retrievechat]'\n"
            if include_retrieve_chat
            else "# !{sys.executable} -m pip install -q pyautogen\n"
        )
        content = f"{comment(True)}{self.waldie.name}" + "\n\n"
        content += f"{comment(True, 2)}Dependencies" + "\n\n"
        content += "import sys\n"
        content += pip_install_autogen
        extra_requirements = " ".join(self.waldie.requirements)
        if extra_requirements:
            content += (
                f"# !{{sys.executable}} -m pip install -q {extra_requirements}"
                + "\n"
            )
        content += export_flow(
            waldie=self.waldie,
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
        if not shutil.which("jupytext"):
            run_command(
                [sys.executable, "-m", "pip", "install", "jupytext"],
                allow_error=False,
                silent=True,
            )
        run_command(
            ["jupytext", "--to", "notebook", str(py_path)],
            silent=True,
            allow_error=False,
        )
        ipynb_path = str(py_path).replace(".tmp.py", ".tmp.ipynb")
        if not os.path.exists(ipynb_path):
            raise RuntimeError("Could not generate notebook")
        Path(ipynb_path).rename(ipynb_path.replace(".tmp.ipynb", ".ipynb"))
        py_path.unlink()

    def to_py(self, path: Path) -> None:
        """Export waldie flow to python script.

        Parameters
        ----------
        path : Path
            The path to export to.
        """
        content = "#!/usr/bin/env python\n"
        content += f'"""{self.waldie.name}\n\n'
        content += f"{self.waldie.description}\n\n"
        content += f"Tags: {', '.join(self.waldie.tags)}\n\n"
        content += f"Requirements: {', '.join(self.waldie.requirements)}\n\n"
        content += '"""\n\n'
        content += "# cspell: disable\n\n"
        content += export_flow(
            waldie=self.waldie,
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

    def to_waldie(self, file_path: Path) -> None:
        """Export the Waldie instance.

        Parameters
        ----------
        file_path : Path
            The file path.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.waldie.model_dump_json())


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    allow_error: bool = True,
    silent: bool = False,
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
    silent : bool, optional
        Whether to print the command, by default False.

    Raises
    ------
    RuntimeError
        If the command fails and allow_error is False.
    """
    if not cwd:
        cwd = Path.cwd()
    if silent is False:
        # pylint: disable=inconsistent-quotes
        print(f"Running command: \n{' '.join(cmd)}\n")
    try:
        subprocess.run(
            cmd,
            check=True,
            cwd=cwd,
            env=os.environ,
            stdout=sys.stdout if silent is False else subprocess.DEVNULL,
            stderr=sys.stderr if allow_error is False else subprocess.DEVNULL,
        )  # nosemgrep # nosec
    except BaseException as error:  # pylint: disable=broad-except
        if allow_error:
            return
        raise RuntimeError(f"Error running command: {error}") from error
