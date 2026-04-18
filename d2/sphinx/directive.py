"""The ``.. d2::`` Sphinx directive."""

from __future__ import annotations

from pathlib import Path

from docutils import nodes as dnodes
from docutils.parsers.rst import Directive, directives

import d2
from d2.sphinx import cache
from d2.sphinx.nodes import d2_svg, placeholder_svg

_VALID_LIBRARIES = {"adi", "sw"}
_VALID_THEMES = {"light", "dark"}

_XML_DECL_PREFIX = "<?xml"


def _library_option(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    if value not in _VALID_LIBRARIES:
        raise ValueError(f"invalid :library: {value!r}")
    return value


def _theme_option(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    if value not in _VALID_THEMES:
        raise ValueError(f"invalid :theme: {value!r}")
    return value


def _strip_xml_declaration(svg: str) -> str:
    if svg.startswith(_XML_DECL_PREFIX):
        end = svg.find("?>")
        if end != -1:
            return svg[end + 2 :].lstrip()
    return svg


class D2Directive(Directive):
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    has_content = True

    option_spec = {  # noqa: RUF012 - docutils convention
        "library": _library_option,
        "theme": _theme_option,
        "alt": directives.unchanged,
    }

    def run(self) -> list[dnodes.Node]:
        source, err = self._resolve_source()
        if err is not None:
            self.state.document.reporter.warning(err, line=self.lineno)
            return [d2_svg(svg=placeholder_svg(err))]

        library = self.options.get("library")
        theme = self.options.get("theme") or "light"

        env = self.state.document.settings.env
        cache_dir = Path(env.app.outdir) / ".d2_cache"
        key = cache.make_key(source, library, theme, d2.__version__)
        svg = cache.get(cache_dir, key)
        if svg is None:
            try:
                svg = d2.compile(source, library=library, theme=theme)
            except RuntimeError as exc:
                self.state.document.reporter.warning(
                    f"D2 compile error: {exc}", line=self.lineno
                )
                svg = placeholder_svg(str(exc))
            else:
                cache.put(cache_dir, key, svg)

        inline = _strip_xml_declaration(svg)
        node = d2_svg(svg=inline)
        return [node]

    def _resolve_source(self) -> tuple[str, str | None]:
        body = "\n".join(self.content).strip()
        arg = self.arguments[0] if self.arguments else None

        if arg and body:
            return "", "D2 directive takes either a file path or inline content, not both"
        if not arg and not body:
            return "", "D2 directive requires either a file path or inline content"

        if arg:
            env = self.state.document.settings.env
            rst_path = Path(env.doc2path(env.docname))
            target = Path(arg)
            if not target.is_absolute():
                target = (rst_path.parent / target).resolve()
            try:
                return target.read_text(encoding="utf-8"), None
            except OSError as exc:
                return "", f"D2 directive cannot read {target}: {exc}"
        return body, None
