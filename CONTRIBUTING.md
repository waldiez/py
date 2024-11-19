# How to contribute to this project

## Getting Started

This project is a Python package managed with [uv](https://github.com/astral-sh/uv) and [hatch](https://github.com/pypa/hatch). To get started, clone the repository and install the dependencies:

```bash
git clone ssh://github.com/waldiez/waldiez.git
cd waldiez
# install uv if not already installed
python -m pip install uv
# generate a new venv
uv venv --python 3.10
# activate the venv
. .venv/bin/activate
# on windows
# .venv\Scripts\activate.ps1 or .venv\Scripts\activate.bat
# upgrade pip
uv pip install --upgrade pip
# install the dependencies
pip install -r requirements/all.txt
```

## Development

There are three core modules in this project:

- `waldiez.models`: Contains the pydantic models for the waldiez flow.
- `waldiez.exporting`: Contains the logic to export a waldiez flow to a python script or a jupyter notebook.
- `waldiez.io`: Contains the logic to provide the WaldiezIOStream (extends autogen.IOSream) to handle input and output.

The project is structured as follows:

``` bash
waldiez
├── __main__.py
├── cli.py
├── exporter.py
├── runner.py
├── exporting
│   ├── agents
│   │   ...
│   ├── chats
│   │   ...
│   ├── flow
│   │   ...
│   ├── models
│   │   ...
│   ├── skills
│   │   ...
│   └── utils
│       ...
├── models
│   ├── agents
│   │   ...
│   ├── chat
│   │   ...
│   ├── common
│   │   ...
│   ├── flow
│   │   ...
│   ├── model
│   │   ...
│   └── skill
│       ...
├── io
│   ├── __init__.py
├── _version.py
```

## Testing

To run the tests, use the following command:

```bash
# for all tests
make test
# for specific tests
make test_models
make test_exporting
```
