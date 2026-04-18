"""End-to-end Sphinx build tests for d2.sphinx."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

sphinx = pytest.importorskip("sphinx")
from sphinx.application import Sphinx  # noqa: E402


def build_docs(tmp_path: Path, rst: str, conf_extra: str = "") -> tuple[str, str]:
    """Build a single-page Sphinx project; return (html, warnings)."""
    src = tmp_path / "src"
    out = tmp_path / "out"
    doctrees = tmp_path / "doctrees"
    src.mkdir()
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
    return html, warn_buf.getvalue()


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
