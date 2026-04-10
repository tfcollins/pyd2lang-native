from __future__ import annotations

import shutil
import subprocess
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import pytest

DISALLOWED_DARK_FILLS = ("#ffffff", "#fff", "white", "#f5f5f5")
SHAPE_TAGS = {"rect", "path", "polygon", "circle", "ellipse"}
NON_RENDERED_CONTAINERS = {"defs", "mask", "clippath", "marker"}


class _ExamplesImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.image_sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "img":
            return

        attrs_dict = dict(attrs)
        src = attrs_dict.get("src")
        if not src or not src.lower().endswith(".svg"):
            return

        classes = set((attrs_dict.get("class") or "").split())
        is_dark_variant = src.lower().endswith("-dark.svg")
        is_only_dark = "only-dark" in classes
        if is_dark_variant or is_only_dark:
            self.image_sources.append(src)


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _extract_style_fill(style: str) -> str | None:
    for part in style.split(";"):
        key, sep, value = part.partition(":")
        if sep and key.strip().lower() == "fill":
            return value.strip().lower()
    return None


def _find_disallowed_visible_fills(svg_text: str) -> list[str]:
    root = ET.fromstring(svg_text)
    bad_fills: list[str] = []

    def walk(node: ET.Element, hidden_depth: int = 0) -> None:
        name = _local_name(node.tag).lower()
        hidden = hidden_depth > 0 or name in NON_RENDERED_CONTAINERS
        next_hidden_depth = hidden_depth + 1 if name in NON_RENDERED_CONTAINERS else hidden_depth

        if not hidden and name in SHAPE_TAGS:
            fill = node.attrib.get("fill")
            if fill is None:
                fill = _extract_style_fill(node.attrib.get("style", ""))
            if fill and fill.strip().lower() in DISALLOWED_DARK_FILLS:
                bad_fills.append(fill.strip().lower())

        for child in node:
            walk(child, next_hidden_depth)

    walk(root)
    return bad_fills


def test_sphinx_examples_dark_images_have_no_white_background_fills(
    tmp_path: Path,
) -> None:
    required_modules = ("sphinx", "sphinx_copybutton", "furo")
    missing = [m for m in required_modules if importlib.util.find_spec(m) is None]
    if missing:
        pytest.skip(f"Missing docs dependencies: {', '.join(missing)}")

    sphinx_build = shutil.which("sphinx-build")
    if not sphinx_build and importlib.util.find_spec("sphinx") is None:
        pytest.skip("sphinx-build is not available in PATH")

    repo_root = Path(__file__).resolve().parents[1]
    docs_src = repo_root / "docs"
    docs_out = tmp_path / "html"
    subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", str(docs_src), str(docs_out)],
        check=True,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    examples_html = docs_out / "examples.html"
    parser = _ExamplesImageParser()
    parser.feed(examples_html.read_text(encoding="utf-8"))

    assert parser.image_sources, "No dark example SVG images found in examples.html"

    issues: list[str] = []
    for src in parser.image_sources:
        img_path = docs_out / src
        if not img_path.exists():
            issues.append(f"{src}: image file not found")
            continue

        svg_text = img_path.read_text(encoding="utf-8")
        disallowed = _find_disallowed_visible_fills(svg_text)
        if disallowed:
            values = ", ".join(sorted(set(disallowed)))
            issues.append(f"{src}: found disallowed fills {values}")

    assert not issues, "Dark example SVG background fills failed checks:\n" + "\n".join(
        issues
    )
