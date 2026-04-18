"""The ``.. d2::`` Sphinx directive."""

from __future__ import annotations

import html
from pathlib import Path

from docutils import nodes as dnodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

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


class D2Directive(SphinxDirective):
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    has_content = True

    option_spec = {  # noqa: RUF012 - docutils convention
        "library": _library_option,
        "theme": _theme_option,
        "alt": directives.unchanged,
        "class": directives.class_option,
        "align": lambda v: directives.choice(v, ("left", "center", "right")),
        "name": directives.unchanged,
    }

    def run(self) -> list[dnodes.Node]:
        source, err = self._resolve_source()
        if err is not None:
            self.state.document.reporter.warning(err, line=self.lineno)
            return [d2_svg(svg=placeholder_svg(err))]

        library = self.options.get("library") or self.config.d2_default_library
        theme_opt = self.options.get("theme")
        dual_default = self.config.d2_default_theme_dual
        if theme_opt is None and dual_default:
            variants = ["light", "dark"]
        else:
            variants = [theme_opt or "light"]

        cache_dir = Path(self.config.d2_cache_dir)

        svgs: list[tuple[str, str]] = []  # (variant, inline-safe svg)
        for variant in variants:
            key = cache.make_key(source, library, variant, d2.__version__)
            svg = cache.get(cache_dir, key)
            if svg is None:
                try:
                    svg = d2.compile(source, library=library, theme=variant)
                except RuntimeError as exc:
                    self.state.document.reporter.warning(
                        f"D2 compile error ({variant}): {exc}", line=self.lineno
                    )
                    svg = placeholder_svg(str(exc))
                else:
                    cache.put(cache_dir, key, svg)
            svgs.append((variant, _strip_xml_declaration(svg)))

        return self._emit_inline(svgs)

    def _emit_inline(self, svgs: list[tuple[str, str]]) -> list[dnodes.Node]:
        extra_classes = self.options.get("class", []) or []
        align = self.options.get("align")
        alt = self.options.get("alt")

        if len(svgs) == 1:
            node = d2_svg(svg=self._wrap_with_alt(svgs[0][1], alt))
            self._apply_wrapper_attrs(node, extra_classes, align)
            return [node]

        container = dnodes.container(classes=["d2-container", *extra_classes])
        if align:
            container["classes"].append(f"align-{align}")
        for variant, svg in svgs:
            wrap_classes = [f"only-{variant}", *extra_classes]
            inner = dnodes.container(classes=wrap_classes)
            inner += d2_svg(svg=self._wrap_with_alt(svg, alt))
            container += inner
        return [container]

    def _apply_wrapper_attrs(
        self, node: dnodes.Node, extra_classes: list[str], align: str | None
    ) -> None:
        if extra_classes:
            node["classes"] = extra_classes
        if align:
            node.setdefault("classes", []).append(f"align-{align}")

    def _wrap_with_alt(self, svg: str, alt: str | None) -> str:
        if not alt:
            return svg
        head_end = svg.find(">")
        if head_end == -1 or not svg.startswith("<svg"):
            return svg
        return svg[:head_end] + f' aria-label="{html.escape(alt, quote=True)}"' + svg[head_end:]

    def _resolve_source(self) -> tuple[str, str | None]:
        body = "\n".join(self.content).strip()
        arg = self.arguments[0] if self.arguments else None

        if arg and body:
            return "", "D2 directive takes either a file path or inline content, not both"
        if not arg and not body:
            return "", "D2 directive requires either a file path or inline content"

        if arg:
            rst_path = Path(self.env.doc2path(self.env.docname))
            target = Path(arg)
            if not target.is_absolute():
                target = (rst_path.parent / target).resolve()
            try:
                return target.read_text(encoding="utf-8"), None
            except OSError as exc:
                return "", f"D2 directive cannot read {target}: {exc}"
        return body, None
