from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_checker_module():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "check_svg_backgrounds.py"
    )
    spec = importlib.util.spec_from_file_location("check_svg_backgrounds", script_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker_module()


def _svg_with_canvas_rect(rect_attrs: str) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
        f'<svg class="d2-svg"><rect {rect_attrs} /></svg>'
        "</svg>"
    )


def test_rejects_white_canvas_background():
    svg = _svg_with_canvas_rect(
        'x="0" y="0" width="10" height="10" fill="#FFFFFF" stroke-width="0"'
    )

    issue = checker.check_svg_text(svg)

    assert issue is not None
    assert "expected transparent" in issue


def test_accepts_transparent_canvas_background():
    svg = _svg_with_canvas_rect(
        'x="0" y="0" width="10" height="10" fill="transparent" stroke-width="0"'
    )

    issue = checker.check_svg_text(svg)

    assert issue is None


def test_docs_dark_svgs_have_transparent_canvas_backgrounds():
    dark_svgs = sorted(
        (Path(__file__).resolve().parents[1] / "docs" / "_static").glob("*dark*.svg")
    )
    assert dark_svgs, "Expected dark SVG files under docs/_static"

    issues = []
    for svg_path in dark_svgs:
        issue = checker.check_svg_file(svg_path)
        if issue:
            issues.append(f"{svg_path.name}: {issue}")

    assert not issues, "\n".join(issues)
