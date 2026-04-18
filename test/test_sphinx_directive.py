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
    src.mkdir(exist_ok=True)
    (src / "conf.py").write_text(
        'extensions = ["d2.sphinx"]\n'
        'master_doc = "index"\n'
        'exclude_patterns = []\n'
        'suppress_warnings = ["app"]\n'
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


def test_dual_theme_emits_both_variants(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "\n"
        "   a -> b\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert warnings.strip() == ""
    assert 'class="only-light"' in html or 'class="only-light ' in html \
        or ' only-light"' in html or ' only-light ' in html
    assert "only-dark" in html
    # Two compiled SVGs embedded (each D2 SVG contains an outer + inner <svg>)
    svg_count = html.count("<svg")
    assert svg_count > 0 and svg_count % 2 == 0  # even: two variants
    assert svg_count >= 4  # at least two compilations worth


def test_theme_option_forces_single_variant(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: dark\n"
        "\n"
        "   a -> b\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert warnings.strip() == ""
    # Single variant: D2 SVGs have nested <svg>, so at least 1 but fewer than dual
    single_count = html.count("<svg")
    assert single_count > 0
    assert "only-light" not in html and "only-dark" not in html


def test_class_option_appends_to_wrapper(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :class: my-extra\n"
        "\n"
        "   a -> b\n"
    )
    html, _ = build_docs(tmp_path, rst)
    assert "my-extra" in html
    assert "only-light" in html and "only-dark" in html


def test_alt_option_lands_on_wrapper(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "   :alt: my diagram\n"
        "\n"
        "   a -> b\n"
    )
    html, _ = build_docs(tmp_path, rst)
    assert 'aria-label="my diagram"' in html


def test_alt_option_escapes_html_injection(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "   :alt: \"><script>alert(1)</script>\n"
        "\n"
        "   a -> b\n"
    )
    html_out, _ = build_docs(tmp_path, rst)
    # The script tag must be escaped, not pass through literally.
    assert "<script>alert(1)</script>" not in html_out
    assert "&lt;script&gt;" in html_out or "&#x3C;script&#x3E;" in html_out
