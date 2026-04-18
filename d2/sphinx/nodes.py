"""Docutils node and helpers for embedding D2-rendered SVG."""

from __future__ import annotations

from xml.sax.saxutils import escape

from docutils import nodes

_PLACEHOLDER_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="60" '
    'role="img" aria-label="D2 compile error">'
    '<rect width="100%" height="100%" fill="#fff5f5" '
    'stroke="#c53030" stroke-width="2"/>'
    '<text x="12" y="24" font-family="monospace" font-size="12" '
    'fill="#c53030">D2 compile error</text>'
    '<text x="12" y="44" font-family="monospace" font-size="11" '
    'fill="#742a2a">{reason}</text>'
    "</svg>"
)


def placeholder_svg(reason: str) -> str:
    """Return a red-bordered SVG snippet summarizing a compile failure."""
    truncated = reason[:60] + ("…" if len(reason) > 60 else "")
    return _PLACEHOLDER_TEMPLATE.format(reason=escape(truncated))


class d2_svg(nodes.General, nodes.Element):
    """A node whose ``svg`` attribute holds raw SVG text to inline in HTML."""


def visit_d2_svg_html(self, node: d2_svg) -> None:
    self.body.append(node["svg"])


def depart_d2_svg_html(self, node: d2_svg) -> None:
    # No closing markup — the raw SVG from visit already includes </svg>.
    pass
