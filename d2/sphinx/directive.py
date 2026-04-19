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


def _bool_option(value: str | None) -> bool:
    if value is None or value == "":
        return True
    lowered = value.strip().lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False
    raise ValueError(f"invalid :inline: {value!r}")


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
        "inline": _bool_option,
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

        svgs: list[tuple[str, str, str]] = []  # (variant, inline-safe, raw)
        for variant in variants:
            key = cache.make_key(source, library, variant, d2.__version__)
            raw = cache.get(cache_dir, key)
            if raw is None:
                try:
                    raw = d2.compile(source, library=library, theme=variant)
                except RuntimeError as exc:
                    self.state.document.reporter.warning(
                        f"D2 compile error ({variant}): {exc}", line=self.lineno
                    )
                    raw = placeholder_svg(str(exc))
                else:
                    cache.put(cache_dir, key, raw)
            svgs.append((variant, _strip_xml_declaration(raw), raw))

        if self.options.get("inline", True):
            return self._emit_inline(svgs)
        return self._emit_files(svgs, source, library)

    def _emit_inline(self, svgs: list[tuple[str, str, str]]) -> list[dnodes.Node]:
        extra_classes = self.options.get("class", []) or []
        align = self.options.get("align")
        alt = self.options.get("alt")

        if len(svgs) == 1:
            svg_node = d2_svg(svg=self._wrap_with_alt(svgs[0][1], alt))
            needs_wrapper = bool(extra_classes or align or self.options.get("name"))
            if not needs_wrapper:
                return [svg_node]
            container = dnodes.container(classes=list(extra_classes))
            if align:
                container["classes"].append(f"align-{align}")
            container += svg_node
            self.add_name(container)
            return [container]

        container = dnodes.container(classes=["d2-container", *extra_classes])
        if align:
            container["classes"].append(f"align-{align}")
        for variant, inline_svg, _raw in svgs:
            wrap_classes = [f"only-{variant}", *extra_classes]
            inner = dnodes.container(classes=wrap_classes)
            inner += d2_svg(svg=self._wrap_with_alt(inline_svg, alt))
            container += inner
        self.add_name(container)
        return [container]

    def _emit_files(
        self,
        svgs: list[tuple[str, str, str]],
        source: str,
        library: str | None,
    ) -> list[dnodes.Node]:
        imagedir = Path(self.config.d2_images_dir)
        imagedir.mkdir(parents=True, exist_ok=True)
        relpath = self.config.d2_images_relpath

        extra_classes = self.options.get("class", []) or []
        align = self.options.get("align")
        alt = self.options.get("alt") or ""
        alt_attr = html.escape(alt, quote=True)

        img_nodes: list[dnodes.Node] = []
        for variant, _inline, raw in svgs:
            key = cache.make_key(source, library, variant, d2.__version__)
            suffix = "" if variant == "light" else "-dark"
            filename = f"d2-{key[:12]}{suffix}.svg"
            (imagedir / filename).write_text(raw, encoding="utf-8")

            classes = ([f"only-{variant}"] if len(svgs) > 1 else []) + extra_classes
            class_attr = html.escape(" ".join(classes), quote=True) if classes else ""
            align_attr = f' align="{align}"' if align else ""
            class_markup = f' class="{class_attr}"' if class_attr else ""
            markup = f'<img src="{relpath}/{filename}" alt="{alt_attr}"{class_markup}{align_attr}>'
            img_nodes.append(dnodes.raw("", markup, format="html"))

        if len(img_nodes) == 1:
            self.add_name(img_nodes[0])
            return img_nodes
        container = dnodes.container(classes=["d2-container", *extra_classes])
        for n in img_nodes:
            container += n
        self.add_name(container)
        return [container]

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
