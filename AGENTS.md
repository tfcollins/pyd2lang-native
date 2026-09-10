# Repository Guidelines

## Project Structure & Module Organization

- `d2/` contains the Python package. `d2/__init__.py` exposes the native D2 compiler bindings, while `d2/sphinx/` contains the Sphinx directive, nodes, and cache support.
- `lib/` contains the Go bridge (`d2lib.go`), build scripts, and bundled D2 shape/theme libraries under `lib/adi/`, `lib/sw/`, `lib/jif/`, `lib/datax/`, `lib/clean/`, and `lib/editorial/`.
- `test/` contains pytest coverage for package behavior, Sphinx integration, scripts, and visual fixtures under `test/visual-tests/`.
- `docs/` contains Sphinx documentation and generated/static assets in `docs/_static/`.
- `scripts/` contains maintenance utilities for icon embedding, SVG cleanup, and releases.

## Build, Test, and Development Commands

- `python -m pip install -e ".[dev,sphinx]"` installs the package with development and Sphinx extras.
- `bash lib/build.sh` builds the native shared library for local development.
- `pytest test/ -v` runs the main test suite.
- `nox -s tests` runs tests across Python 3.10, 3.11, and 3.12 using uv-backed environments.
- `nox -s lint` runs Ruff checks; `nox -s fmt` formats Python files.
- `nox -s typecheck` runs `ty check` against `d2/`.
- `nox -s docs` builds HTML docs into `docs/_build/html`; `nox -s docs_serve` starts live docs on port 8080.
- `nox -s embed_check` verifies generated ADI component embeddings match icon sources.

## Coding Style & Naming Conventions

Use Python 3.10+ syntax. Ruff is configured for 100-character lines, double quotes, space indentation, import sorting, pyupgrade, bugbear, simplify, and Ruff-specific rules. Keep public Python APIs in `d2` concise and typed where practical. Name pytest files `test_*.py` and Sphinx modules by responsibility (`directive.py`, `nodes.py`, `cache.py`).

## Testing Guidelines

Add or update tests in `test/` for behavior changes. Prefer focused pytest tests and fixtures over broad integration-only checks. For Sphinx changes, run `nox -s sphinx_tests`. For icon/library generation changes, run `nox -s embed_check` and relevant script tests.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects such as `Fix release tag validation in publish workflow` and `Render JIF converters as top-level shapes`. Keep subjects specific and under one logical change. PRs should include a concise summary, verification commands, linked issues when applicable, and screenshots or docs preview links for visual documentation changes.

## Security & Configuration Tips

Do not commit built wheels, local virtual environments, caches, or generated scratch diagrams unless they are intentional fixtures. Native library changes should include the Go dependency update, rebuilt shared library path expectations, and test evidence across supported platforms when relevant.
