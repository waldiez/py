# Waldiez

![CI Build](https://github.com/waldiez/waldiez/actions/workflows/main.yaml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/waldiez/waldiez/badge.svg)](https://coveralls.io/github/waldiez/waldiez) [![PyPI version](https://badge.fury.io/py/waldiez.svg?icon=si%3Apython)](https://badge.fury.io/py/waldiez)

Translate a Waldiez flow:

![Flow](https://raw.githubusercontent.com/waldiez/waldiez/refs/heads/main/docs/static/images/overview.webp)

To a python script or a jupyter notebook with the corresponding [ag2](https://github.com/ag2ai/ag2/) agents and chats.

## Features

- Export .waldiez flows to .py or .ipynb
- Run a .waldiez flow
- Include a `logs` folder with the logs of the flow in csv format
- Provide a custom [IOSStream](https://ag2ai.github.io/ag2/docs/reference/io/base#iostream) to handle input and output.

## Installation

On PyPI:

```bash
python -m pip install waldiez
```

From the repository:

```bash
python -m pip install git+https://github.com/waldiez/waldiez.git
```

## Usage

### CLI

```bash
# Export a Waldiez flow to a python script or a jupyter notebook
waldiez --export /path/to/a/flow.waldiez --output /path/to/an/output/flow[.py|.ipynb]
# Export and run the script, optionally force generation if the output file already exists
waldiez /path/to/a/flow.waldiez --output /path/to/an/output/flow[.py] [--force]
```

### Using docker/podman

```shell
CONTAINER_COMMAND=docker # or podman
# pull the image
$CONTAINER_COMMAND pull waldiez/waldiez
# Export a Waldiez flow to a python script or a jupyter notebook
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.waldiez:/flow.waldiez \
  -v /path/to/an/output:/output \
  waldiez/waldiez --export /flow.waldiez --output /output/flow[.py|.ipynb]

# with selinux and/or podman, you might get permission (or file not found) errors, so you can try:
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.waldiez:/flow.waldiez \
  -v /path/to/an/output:/output \
  --userns=keep-id \
  --security-opt label=disable \
  waldiez/waldiez --export /flow.waldiez --output /output/flow[.py|.ipynb]
```

```shell
# Export and run the script
$CONTAINER_COMMAND run --rm -v /path/to/a/flow.waldiez:/flow.waldiez -v /path/to/an/output:/output waldiez/waldiez /flow.waldiez --output /output/output[.py]
```

### As a library

#### Export a flow

```python
# Export a Waldiez flow to a python script or a jupyter notebook
from waldiez import WaldiezExporter
flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"  # or .ipynb
exporter = WaldiezExporter.load(flow_path)
exporter.export(output_path)
```
  
#### Run a flow

```python
# Run a flow
from waldiez import WaldiezRunner
flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"
runner = WaldiezRunner.load(flow_path)
runner.run(output_path=output_path)
```

#### Run a flow with a custom IOStream

```python
# Run the flow with a custom IOStream
# In case the standard 'input' and 'print' functions cannot be used
import time
import threading

from typing import Any

from waldiez import WaldiezRunner
from waldiez.io import WaldiezIOStream

flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"


def custom_print_function(*args: Any, sep: str = " ", **kwargs: Any) -> None:
    """Custom print function."""
    print(*args, sep=sep, **kwargs)


# Custom input handler
class InputProcessorWrapper:
    """Wrapper input processor.
    
    To manage the interaction between the custom input processor and IOStream.
    """

    def __init__(self):
        self.stream = None  # Placeholder for the WaldiezIOStream instance
        self.lock = threading.Lock()  # Ensure thread-safe operations

    def custom_input_processor(self, prompt: str) -> None:
        """Simulate external input and send it back to the IOStream."""
        def external_input_simulation():
            with self.lock:  # Ensure thread-safe access
                time.sleep(2)  # Simulate delay for network input
                if self.stream:
                    self.stream.set_input("Simulated external input")
                else:
                    raise RuntimeError("Stream reference not set!")

        threading.Thread(target=external_input_simulation, daemon=True).start()

    def set_stream(self, stream: "WaldiezIOStream"):
        """Set the WaldiezIOStream instance."""
        with self.lock:  # Ensure thread-safe setting of the stream
            self.stream = stream

processor_wrapper = InputProcessorWrapper()

stream = WaldiezIOStream(
    input_timeout=30,
    print_function=
    on_prompt_input=processor_wrapper.custom_input_processor,
)

# Link the processor wrapper to the WaldiezIOStream instance
processor_wrapper.set_stream(custom_stream)

with WaldiezIOStream.set_default(io_stream):
    runner = WaldiezRunner.load(flow_path)
    runner.run(stream=io_stream, output_path=output_path)

```

### Tools

- [ag2 (formerly AutoGen)](https://github.com/ag2ai/ag2)
- [juptytext](https://github.com/mwouts/jupytext)
- [pydantic](https://github.com/pydantic/pydantic)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/waldiez/waldiez/blob/main/LICENSE) file for details.
