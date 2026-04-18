"""End-to-end Sphinx build tests for d2.sphinx."""

from __future__ import annotations

import io
import re
from pathlib import Path

import pytest

sphinx = pytest.importorskip("sphinx")
from sphinx.application import Sphinx  # noqa: E402

# ANSI escape sequence pattern (used by Sphinx colorized output)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _filter_sphinx_builtin_warnings(raw: str) -> str:
    """Strip ANSI codes and drop Sphinx built-in extension re-registration warnings."""
    lines = []
    for line in raw.splitlines():
        plain = _ANSI_RE.sub("", line)
        # Filter out only Sphinx's internal node/directive re-registration warnings
        if "sphinx.addnodes" in plain or "sphinx.domains" in plain:
            continue
        lines.append(plain)
    return "\n".join(lines).strip()


def build_docs(tmp_path: Path, rst: str, conf_extra: str = "") -> tuple[str, str]:
    """Build a single-page Sphinx project; return (html, warnings)."""
    src = tmp_path / "src"
    out = tmp_path / "out"
    doctrees = tmp_path / "doctrees"
    src.mkdir(exist_ok=True)
    (src / "conf.py").write_text(
        'extensions = ["d2.sphinx"]\n'
        'master_doc = "index"\n'
        'exclude_patterns = []\n'
        + conf_extra
    )
    (src / "index.rst").write_text(rst)
    warn_buf = io.StringIO()
    app = Sphinx(
        srcdir=str(src),
        confdir=str(src),
        outdir=str(out),
        doctreedir=str(doctrees),
        buildername="html",
        warning=warn_buf,
        freshenv=True,
    )
    app.build()
    html = (out / "index.html").read_text(encoding="utf-8")
    return html, _filter_sphinx_builtin_warnings(warn_buf.getvalue())


def test_file_path_source_renders_svg(tmp_path: Path):
    # Write a sibling D2 file next to index.rst
    src = tmp_path / "src"
    src.mkdir(exist_ok=True)
    (src / "shape.d2").write_text("x -> y\n")
    rst = (
        "Title\n=====\n\n"
        ".. d2:: shape.d2\n"
        "   :theme: light\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert warnings.strip() == ""
    assert "<svg" in html


def test_inline_body_single_theme_renders_svg(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "\n"
        "   a -> b\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert warnings.strip() == ""
    assert "<svg" in html
    assert "<?xml" not in html  # declaration stripped for inline mode
