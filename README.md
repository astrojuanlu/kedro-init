# kedro-init

[![Documentation Status](https://readthedocs.org/projects/kedro-init/badge/?version=latest)](https://kedro-init.readthedocs.io/en/latest/?badge=latest)
[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/kedro-init)](https://pypi.org/project/kedro-init)

A simple CLI command that initialises a Kedro project from an existing Python package

## Installation and usage

To use, run

```
$ uvx kedro-init .
```

Or, alternatively,

```
$ pipx run kedro-init .
```

For example, from a Poetry package:

```
(.venv) $ poetry new --src test-project && cd test-project
(.venv) $ kedro-init .
[00:19:38] Looking for existing package directories                             cli.py:25
[00:19:45] Initialising config directories                                      cli.py:25
           Creating modules                                                     cli.py:25
           🔶 Kedro project successfully initialised!                           cli.py:26
```

And with a uv package:

```
$ mkdir test-project && cd test-project && uv init
Initialized project `test-project`
$ uvx kedro-init .
[09:06:24] Looking for existing package directories                      cli.py:25
[09:06:25] Initialising config directories                               cli.py:25
           Creating modules                                              cli.py:25
           🔶 Kedro project successfully initialised!                    cli.py:26
```

## Development

To run style checks:

```
(.venv) $ pip install tox
(.venv) $ tox
```
