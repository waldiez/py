# Changelog

## v0.1.7

- Move `WaldiezIOStream` to `waldiez.io` module
- Move autogen imports to local imports
- Also Provide a container (docker/podman) image for running/exporting Waldiez flows

## v0.1.6

- Fix SyntaxError with quoted strings
- Update twisted to 24.10.0

## v0.1.5

- Fix Quoting issue in chat messages

## v0.1.4

- Fix #40 - AttributeError: 'NoneType' object has no attribute 'endswith' with keyword termination.

## v0.1.3

- Exporting: Use a separate file for the model API keys

## v0.1.2

- RAG: handle windows paths
- Remove max_tokens from agent data

## v0.1.1

- RAG: use string literals for paths, to avoid issues with backslashes in Windows

## v0.1.0

- Initial release