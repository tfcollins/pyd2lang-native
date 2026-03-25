"""Nox sessions for pyd2lang-native."""

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "test/", "-v", *session.posargs)


@nox.session
def lint(session: nox.Session) -> None:
    """Run ruff linter."""
    session.install("ruff")
    session.run("ruff", "check", "d2/", "test/", "noxfile.py", *session.posargs)


@nox.session
def fmt(session: nox.Session) -> None:
    """Run ruff formatter."""
    session.install("ruff")
    session.run("ruff", "format", "d2/", "test/", "noxfile.py", *session.posargs)


@nox.session
def fmt_check(session: nox.Session) -> None:
    """Check ruff formatting without modifying files."""
    session.install("ruff")
    session.run("ruff", "format", "--check", "d2/", "test/", "noxfile.py")


@nox.session
def typecheck(session: nox.Session) -> None:
    """Run ty type checker."""
    session.install("ty")
    session.install("-e", ".")
    session.run("ty", "check", "d2/", *session.posargs)


@nox.session
def docs(session: nox.Session) -> None:
    """Build Sphinx documentation."""
    session.install("-e", ".[docs]")
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@nox.session
def docs_serve(session: nox.Session) -> None:
    """Build and serve docs with live reload."""
    session.install("-e", ".[docs]", "sphinx-autobuild")
    session.run(
        "sphinx-autobuild",
        "docs",
        "docs/_build/html",
        "--port",
        "8080",
        "--open-browser",
    )


@nox.session
def act(session: nox.Session) -> None:
    """Run GitHub Actions workflows locally using act.

    Usage:
        nox -s act                        # Run all workflows
        nox -s act -- docs                # Run only the docs workflow
        nox -s act -- build_wheels        # Run only the build workflow
        nox -s act -- --list              # List available workflows
    """
    act_bin = session.run("which", "act", external=True, silent=True)
    if not act_bin or not act_bin.strip():
        session.error("act is not installed. Install from https://github.com/nektos/act")

    args = session.posargs

    if args and args[0] == "--list":
        session.run("act", "--list", external=True)
        return

    if args and not args[0].startswith("-"):
        # Treat first arg as workflow name
        workflow = args[0]
        extra = args[1:]
        session.run(
            "act",
            "push",
            "-W",
            f".github/workflows/{workflow}.yml",
            "--detect-event",
            *extra,
            external=True,
        )
    else:
        # Run all workflows
        session.run(
            "act",
            "push",
            "--detect-event",
            *args,
            external=True,
        )


@nox.session
def release(session: nox.Session) -> None:
    """Create a release: bump version, tag, and push.

    Usage:
        nox -s release                    # Patch bump (0.0.4 → 0.0.5)
        nox -s release -- minor           # Minor bump (0.0.4 → 0.1.0)
        nox -s release -- major           # Major bump (0.0.4 → 1.0.0)
    """
    bump = session.posargs[0] if session.posargs else "patch"
    session.run("bash", "scripts/release.sh", bump, external=True)
