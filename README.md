# KOPP

![KOPP icon](art/kopp_icon.png)

KOPP is a desktop application for tracking working time, hour balances, annual leave, vacation time, and related comments.

The application is written in Python, uses wxPython for the graphical interface, Peewee with SQLite for local data storage, and PyInstaller for distributable builds.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/) for dependency and virtual environment management
- Git, used by the version generation script

The main runtime dependencies are declared in `pyproject.toml`:

- `wxPython`
- `peewee`
- `jinja2`
- `pyinstaller`

Development dependencies are in the `dev` dependency group:

- `pytest`
- `ruff`

## Installation

Install the project dependencies with uv:

```bash
uv sync
```

For development, include the dev dependency group:

```bash
uv sync --group dev
```

## Version File

KOPP generates `kopp/version.py` from the current Git state. The generated file contains the commit id, commit count, branch name, and application version prefix.

Generate it manually with:

```bash
uv run python kopp/createversion.py version.py
```

The packaging script also regenerates this file before building.

## Running the Application

Start KOPP from the project root:

```bash
uv run python -m kopp
```


## Tests and Linting

Run the unit tests:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

## Building Binaries

Application binaries are created with `install/createapp.py`, which wraps PyInstaller.

Supported platform arguments are:

- `Windows`
- `Linux`
- `OSX`

Examples:

```bash
uv run python install/createapp.py Windows
uv run python install/createapp.py OSX
uv run python install/createapp.py Linux
```

Build outputs are written under `bin/`. The generated executable or application bundle name includes the Git commit count, for example `kopp_31`.

## Linux and wxPython

wxPython Linux wheels are platform-specific. On Ubuntu 24.04 with Python 3.14, the CI workflow installs the matching wheel directly from the wxPython extras repository:

```bash
uv pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.5-cp314-cp314-linux_x86_64.whl
```

This avoids building wxPython from source during CI.

## Continuous Integration

The project uses three GitHub Actions workflows:

- Linux: runs on every push, installs development dependencies, runs Ruff, and runs the unit tests.
- Windows: runs on every push and on published GitHub releases, builds the application, uploads the workflow artifact, and attaches the zip file to the release.
- macOS: runs on every push and on published GitHub releases, builds the application, uploads the workflow artifact, and attaches the zip file to the release.

The Windows and macOS workflows intentionally do not run unit tests; they focus on binary packaging.

## Project Layout

```text
kopp/                 Application source code
kopp/templates/       HTML templates used by the application
test/                 Unit tests
install/createapp.py  PyInstaller build helper
art/                  Application icons and artwork
.github/workflows/    GitHub Actions workflows
```

## Generated and Local Files

The following paths are generated locally and should not be committed:

- `.venv/`
- `bin/`
- `kopp/version.py`
- Python cache files

See `.gitignore` for the full list.
