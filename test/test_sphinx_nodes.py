"""Tests for d2.sphinx.nodes."""

from __future__ import annotations

from d2.sphinx import nodes


def test_placeholder_svg_contains_error_marker():
    svg = nodes.placeholder_svg("compile failed")
    assert svg.startswith("<svg ")
    assert "D2 compile error" in svg
    assert "compile failed" in svg


def test_placeholder_svg_truncates_long_reasons():
    long = "x" * 200
    svg = nodes.placeholder_svg(long)
    # 60-char cap plus an ellipsis marker
    assert "x" * 60 in svg
    assert "x" * 200 not in svg


def test_placeholder_svg_escapes_xml_special_chars():
    svg = nodes.placeholder_svg("oops <&>")
    assert "&lt;" in svg and "&amp;" in svg and "&gt;" in svg
