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


def test_inline_false_emits_img_and_writes_file(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "   :inline: false\n"
        "\n"
        "   a -> b\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert warnings.strip() == ""
    assert "<svg" not in html  # No inlined SVG
    # <img> points into _images/
    import re
    match = re.search(r'<img[^>]+src="([^"]+)"', html)
    assert match is not None
    src = match.group(1)
    assert "_images" in src
    # And the file landed there
    out = tmp_path / "out"
    assert (out / src.lstrip("./")).is_file()


def test_missing_source_warns_and_emits_placeholder(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert "D2 directive requires either" in warnings
    assert "D2 compile error" in html  # placeholder text


def test_both_source_forms_warns(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(exist_ok=True)
    (src / "a.d2").write_text("x\n")
    rst = (
        "Title\n=====\n\n"
        ".. d2:: a.d2\n"
        "\n"
        "   y -> z\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert "either a file path or inline content, not both" in warnings
    assert "D2 compile error" in html


def test_missing_file_warns(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2:: does_not_exist.d2\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert "cannot read" in warnings
    assert "D2 compile error" in html


def test_compile_failure_warns_and_emits_placeholder(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "\n"
        "   invalid {{ syntax\n"
    )
    html, warnings = build_docs(tmp_path, rst)
    assert "D2 compile error" in warnings
    assert "D2 compile error" in html


def test_invalid_library_raises_directive_error(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :library: bogus\n"
        "\n"
        "   a -> b\n"
    )
    _html, warnings = build_docs(tmp_path, rst)
    # Invalid option values raise during parsing; docutils logs them as errors
    assert "invalid" in warnings.lower() or "bogus" in warnings.lower()


def test_second_build_is_a_cache_hit(tmp_path: Path):
    rst = (
        "Title\n=====\n\n"
        ".. d2::\n"
        "   :theme: light\n"
        "\n"
        "   a -> b\n"
    )
    # First build populates the cache
    build_docs(tmp_path, rst)
    cache_dir = tmp_path / "out" / ".d2_cache"
    assert cache_dir.is_dir()
    entries_before = sorted(p.relative_to(cache_dir) for p in cache_dir.rglob("*.svg"))
    mtimes_before = {p: (cache_dir / p).stat().st_mtime_ns for p in entries_before}
    assert entries_before  # at least one entry

    # Rebuild using the same source; no new files should appear, existing mtimes stable.
    build_docs(tmp_path, rst)
    entries_after = sorted(p.relative_to(cache_dir) for p in cache_dir.rglob("*.svg"))
    assert entries_after == entries_before
    for p in entries_after:
        assert (cache_dir / p).stat().st_mtime_ns == mtimes_before[p]
