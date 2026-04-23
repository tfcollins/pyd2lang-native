from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

import d2

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def _requires_python() -> str:
    match = re.search(r'^requires-python = "([^"]+)"$', PYPROJECT, re.MULTILINE)
    assert match is not None
    return match.group(1)


def _classifiers() -> set[str]:
    return set(re.findall(r'^\s*"([^"]+)"[,]?$', PYPROJECT, re.MULTILINE))


def test_python_badge_uses_declared_requires_python():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    expected_url = f"https://img.shields.io/badge/python-{quote(_requires_python(), safe='')}-blue"

    assert expected_url in readme
    assert "img.shields.io/pypi/pyversions/pyd2lang-native" not in readme


def test_python_classifiers_match_wheel_builds():
    assert "Programming Language :: Python :: 3.10" in _classifiers()
    assert "Programming Language :: Python :: 3.11" in _classifiers()
    assert "Programming Language :: Python :: 3.12" in _classifiers()
    assert re.search(
        r"CIBW_BUILD:\s*cp310-\* cp311-\* cp312-\*",
        (ROOT / ".github/workflows/build_wheels.yml").read_text(encoding="utf-8"),
    )


def test_package_version_matches_release():
    assert d2.__version__ == "0.1.4"


def test_release_workflow_validates_tag_matches_package_version():
    workflow = (ROOT / ".github/workflows/build_wheels.yml").read_text(encoding="utf-8")

    assert "Validate tag version" in workflow
    assert "if: startsWith(github.ref, 'refs/tags/v')" in workflow
    assert "RELEASE_TAG: ${{ github.ref_name }}" in workflow
    assert 'Path("d2/__init__.py").read_text' in workflow
    assert 're.search(r\'^__version__\\s*=\\s*"([^"]+)"\'' in workflow
