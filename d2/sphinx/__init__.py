"""Sphinx extension entry point for the ``.. d2::`` directive.

Sphinx is imported lazily inside :func:`setup` so ``import d2`` remains
free of optional dependencies.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _resolve_paths(app: Any) -> None:
    """Fill in cache + images paths from app once the builder is up."""
    if not app.config.d2_cache_dir:
        app.config.d2_cache_dir = str(Path(app.outdir) / ".d2_cache")
    # Write generated SVGs into srcdir/_images/ so Sphinx can discover and
    # copy them to outdir/_images/ via the normal image pipeline.
    app.config.d2_images_dir = str(Path(app.srcdir) / app.builder.imagedir)
    app.config.d2_images_relpath = app.builder.imagedir


def setup(app: Any) -> dict[str, Any]:
    from d2.sphinx.directive import D2Directive
    from d2.sphinx.nodes import d2_svg, depart_d2_svg_html, visit_d2_svg_html

    app.add_node(d2_svg, override=True, html=(visit_d2_svg_html, depart_d2_svg_html))
    app.add_directive("d2", D2Directive, override=True)

    app.add_config_value("d2_default_library", None, "env")
    app.add_config_value("d2_default_theme_dual", True, "env")
    app.add_config_value("d2_cache_dir", None, "env")
    app.add_config_value("d2_images_dir", None, "env")
    app.add_config_value("d2_images_relpath", "_images", "env")

    app.connect("builder-inited", _resolve_paths)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
