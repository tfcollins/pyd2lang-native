# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyd2lang-native provides Python bindings to the d2lang diagram compiler via a Go shared library loaded through ctypes. It compiles D2 source code to SVG natively without requiring the d2 CLI. Includes two component libraries: an ADI (Analog Devices) signal-chain library (64 shapes) and an SW (software/AI) architecture library (32 shapes), each with light/dark themes.

## Commands

```bash
# Testing
nox -s tests                    # Run pytest across Python 3.10/3.11/3.12
pytest test/test_d2.py -v       # Run tests directly (current Python only)
pytest test/test_d2.py::test_d2 -v  # Run a single test

# Linting & formatting
nox -s lint                     # Ruff linter
nox -s fmt                      # Ruff auto-format
nox -s fmt_check                # Check formatting without modifying
nox -s typecheck                # Type check with 'ty'

# Docs
nox -s docs                     # Build Sphinx docs
nox -s docs_serve               # Live preview at localhost:8080

# Release
nox -s release                  # Patch bump (default)
nox -s release -- minor         # Minor/major bump
```

Nox uses `uv` as its venv backend.

## Architecture

```
d2/__init__.py          Python API: compile(code, library="adi"|"sw"|None, theme="light") -> SVG
    ↓ ctypes
d2/resources/*.so       Pre-built Go shared library (built from lib/)
    ↓
lib/d2lib.go            C-exported functions:
                          runme()    - plain D2 compilation
                          runmeAdi() - prepends ADI theme + components, then compiles
                          runmeLib() - generic dispatch: selects library by name
lib/adi/                ADI assets: adi-components.d2 (64 icons), adi-theme.d2, adi-theme-dark.d2
lib/sw/                 SW assets: sw-components.d2 (32 icons), sw-theme.d2, sw-theme-dark.d2
lib/sw/icons/           Source SVGs for SW components (used by scripts/embed-sw-icons.sh)
```

The Go library embeds library assets at compile time via `//go:embed`. The Python side loads the shared library, calls the appropriate C function, and returns the SVG string or raises `RuntimeError`. The `library` parameter selects which component library to prepend (or `None` for plain D2).

## Key Conventions

- **Ruff config**: line-length 100, target Python 3.10, double quotes, rules: E/W/F/I/UP/B/SIM/RUF
- **Version**: single source of truth in `d2.__version__` (`d2/__init__.py`), read dynamically by pyproject.toml
- **Tests**: live in `test/` — `test_d2.py` (compilation smoke tests) and a Sphinx directive suite covering the directive (`test_sphinx_directive.py`), cache (`test_sphinx_cache.py`), and nodes (`test_sphinx_nodes.py`). `test_check_svg_backgrounds.py` keeps SVG-canvas-background unit tests. Compilation tests assert `"<?xml"` appears in output; directive tests drive end-to-end Sphinx builds.
- **ADI components**: defined as SVG icons in `lib/adi/adi-components.d2`, exposed as `d2.ADI_COMPONENTS` list
- **SW components**: defined as SVG icons in `lib/sw/sw-components.d2` (auto-generated from `lib/sw/icons/` via `scripts/embed-sw-icons.sh`), exposed as `d2.SW_COMPONENTS` list
- **CI**: cibuildwheel builds wheels on 5 OS matrix entries; docs auto-deploy to GitHub Pages on main
