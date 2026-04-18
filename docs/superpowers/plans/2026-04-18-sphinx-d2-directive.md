# Sphinx `.. d2::` directive — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a bundled Sphinx extension `d2.sphinx` with a `.. d2::` directive that compiles D2 source (inline or file) via `d2.compile()`, emits dual light/dark SVGs (inlined by default), caches by content hash, warns gracefully on errors — then migrate this repo's own docs onto it.

**Architecture:** New subpackage `d2/sphinx/` with four small modules (`__init__`, `directive`, `cache`, `nodes`). Sphinx is an optional extra so `import d2` stays dependency-free. Directive produces a custom `d2_svg` docutils node whose HTML visitor inlines raw SVG; file-mode path emits a regular `docutils.nodes.image`.

**Tech Stack:** Python 3.10+, Sphinx 6+ (optional), docutils, pytest, the existing `d2.compile()` native binding.

**Spec:** `docs/superpowers/specs/2026-04-18-sphinx-d2-directive-design.md`

---

## File Structure

**Create:**
- `d2/sphinx/__init__.py` — `setup(app)` entry point; lazy Sphinx imports
- `d2/sphinx/cache.py` — `make_key()`, `cache_path()`, `get()`, `put()`
- `d2/sphinx/nodes.py` — `d2_svg` docutils node + HTML visitors + `placeholder_svg()`
- `d2/sphinx/directive.py` — `D2Directive` class with option parsing, source resolution, compile orchestration
- `test/test_sphinx_cache.py` — unit tests for cache module
- `test/test_sphinx_directive.py` — end-to-end Sphinx build tests
- `test/fixtures/sphinx_directive/conf.py` — minimal Sphinx conf used by tests
- `test/fixtures/sphinx_directive/index.rst` — drives each directive variant

**Modify:**
- `pyproject.toml` — add `[sphinx]` optional extra; extend `[docs]` to include it
- `noxfile.py` — install `.[sphinx]` in `tests`; add `sphinx_tests` session
- `docs/conf.py` — append `"d2.sphinx"` to `extensions`
- `docs/examples.rst` — replace each paired `.. image::` pair with one `.. d2::` directive call
- `CLAUDE.md` — update the Tests convention line to list the surviving test files

**Delete (after migration, with audit):**
- `scripts/update_example_svgs.py`
- `docs/_static/example-*.svg` (18 files)
- Possibly `scripts/check_svg_backgrounds.py`, `test/test_check_svg_backgrounds.py`, `test/test_sphinx_dark_examples.py` — see Task 13

---

## Task 1: Add `[sphinx]` optional extra to pyproject.toml

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Edit the optional-dependencies table**

Change the `[project.optional-dependencies]` table from:

```toml
[project.optional-dependencies]
docs = ["sphinx", "furo", "sphinx-copybutton"]
dev = ["nox", "uv", "ruff", "ty", "pytest"]
```

to:

```toml
[project.optional-dependencies]
sphinx = ["sphinx>=6"]
docs = ["sphinx", "furo", "sphinx-copybutton", "pyd2lang-native[sphinx]"]
dev = ["nox", "uv", "ruff", "ty", "pytest"]
```

- [ ] **Step 2: Verify the extra resolves**

Run: `pip install --dry-run -e '.[sphinx]' 2>&1 | tail -5`
Expected: reports Sphinx would be installed, exits 0.

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "Add [sphinx] optional extra"
```

---

## Task 2: Cache module with TDD

**Files:**
- Create: `d2/sphinx/__init__.py` (empty sentinel for now)
- Create: `d2/sphinx/cache.py`
- Create: `test/test_sphinx_cache.py`

- [ ] **Step 1: Create the empty subpackage marker**

Create `d2/sphinx/__init__.py` with no content yet — we'll populate it in Task 7. Just creating it now so the package is importable.

```bash
: > d2/sphinx/__init__.py
```

- [ ] **Step 2: Write failing test for key stability**

Create `test/test_sphinx_cache.py`:

```python
"""Tests for d2.sphinx.cache."""

from __future__ import annotations

from pathlib import Path

import pytest

from d2.sphinx import cache


def test_make_key_is_deterministic():
    k1 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    k2 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    assert k1 == k2


def test_make_key_changes_with_source():
    k1 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    k2 = cache.make_key("a -> c", "adi", "light", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_library():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "sw", "light", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_theme():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "adi", "dark", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_version():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "adi", "light", "0.1.2")
    assert k1 != k2


def test_make_key_handles_none_library():
    k = cache.make_key("x", None, "light", "0.1.1")
    assert isinstance(k, str) and len(k) == 64  # sha256 hex
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest test/test_sphinx_cache.py -v`
Expected: collection error — `ModuleNotFoundError: No module named 'd2.sphinx.cache'`.

- [ ] **Step 4: Implement `make_key` in `d2/sphinx/cache.py`**

```python
"""Content-hash cache for compiled D2 SVGs.

Keyed on (source, library, theme, d2.__version__) so a library version
bump invalidates all entries automatically. Null-byte separators prevent
boundary-collision false hits between adjacent fields.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def make_key(source: str, library: str | None, theme: str, version: str) -> str:
    parts = [source, str(library), theme, version]
    data = "\x00".join(parts).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def cache_path(cache_dir: Path, key: str) -> Path:
    return Path(cache_dir) / key[:2] / f"{key}.svg"


def get(cache_dir: Path, key: str) -> str | None:
    path = cache_path(cache_dir, key)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def put(cache_dir: Path, key: str, svg: str) -> None:
    path = cache_path(cache_dir, key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest test/test_sphinx_cache.py -v`
Expected: 6 passed.

- [ ] **Step 6: Add put/get round-trip and fanout tests**

Append to `test/test_sphinx_cache.py`:

```python
def test_put_and_get_round_trip(tmp_path: Path):
    key = cache.make_key("a", "adi", "light", "0.1.1")
    cache.put(tmp_path, key, "<svg>hello</svg>")
    assert cache.get(tmp_path, key) == "<svg>hello</svg>"


def test_get_returns_none_when_missing(tmp_path: Path):
    key = cache.make_key("missing", None, "light", "0.1.1")
    assert cache.get(tmp_path, key) is None


def test_cache_path_uses_two_char_fanout(tmp_path: Path):
    key = "abcdef0123456789" + "0" * 48
    path = cache.cache_path(tmp_path, key)
    assert path.parent.name == "ab"
    assert path.name == f"{key}.svg"


def test_put_creates_fanout_directory(tmp_path: Path):
    key = cache.make_key("x", None, "light", "0.1.1")
    cache.put(tmp_path, key, "<svg/>")
    assert (tmp_path / key[:2]).is_dir()
    assert (tmp_path / key[:2] / f"{key}.svg").is_file()
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `pytest test/test_sphinx_cache.py -v`
Expected: 10 passed.

- [ ] **Step 8: Commit**

```bash
git add d2/sphinx/__init__.py d2/sphinx/cache.py test/test_sphinx_cache.py
git commit -m "Add d2.sphinx.cache content-hash SVG cache"
```

---

## Task 3: Custom docutils node + placeholder helper

**Files:**
- Create: `d2/sphinx/nodes.py`
- Modify: `test/test_sphinx_cache.py` (no — create separate test file)
- Create: `test/test_sphinx_nodes.py`

- [ ] **Step 1: Write failing tests for `placeholder_svg`**

Create `test/test_sphinx_nodes.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest test/test_sphinx_nodes.py -v`
Expected: `ModuleNotFoundError: No module named 'd2.sphinx.nodes'`.

- [ ] **Step 3: Implement `d2/sphinx/nodes.py`**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest test/test_sphinx_nodes.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add d2/sphinx/nodes.py test/test_sphinx_nodes.py
git commit -m "Add d2_svg docutils node and placeholder helper"
```

---

## Task 4: Directive skeleton — inline body, single variant, happy path

Build up `D2Directive` in stages. This task lands the minimal shape: inline body + `:library:` + `:theme:` → one inlined SVG.

**Files:**
- Create: `d2/sphinx/directive.py`
- Modify: `d2/sphinx/__init__.py` (provisional setup to register directive + node so tests can drive it end-to-end)

- [ ] **Step 1: Write failing test for a basic inline dark-theme build**

Create `test/test_sphinx_directive.py`:

```python
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
    src.mkdir()
    (src / "conf.py").write_text(
        'extensions = ["d2.sphinx"]\n'
        'master_doc = "index"\n'
        'exclude_patterns = []\n'
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: fails — directive `d2` not registered.

- [ ] **Step 3: Implement the initial `D2Directive` in `d2/sphinx/directive.py`**

```python
"""The ``.. d2::`` Sphinx directive."""

from __future__ import annotations

from pathlib import Path
from typing import Any

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

    option_spec = {
        "library": _library_option,
        "theme": _theme_option,
        "alt": directives.unchanged,
    }

    def run(self) -> list[dnodes.Node]:
        source = "\n".join(self.content).strip()
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
```

- [ ] **Step 4: Register the directive and node in `d2/sphinx/__init__.py`**

```python
"""Sphinx extension entry point for the ``.. d2::`` directive.

Sphinx is imported lazily inside :func:`setup` so ``import d2`` remains
free of optional dependencies.
"""

from __future__ import annotations

from typing import Any


def setup(app: Any) -> dict[str, Any]:
    from d2.sphinx.directive import D2Directive
    from d2.sphinx.nodes import d2_svg, depart_d2_svg_html, visit_d2_svg_html

    app.add_node(d2_svg, html=(visit_d2_svg_html, depart_d2_svg_html))
    app.add_directive("d2", D2Directive)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest test/test_sphinx_directive.py::test_inline_body_single_theme_renders_svg -v`
Expected: passed.

- [ ] **Step 6: Commit**

```bash
git add d2/sphinx/directive.py d2/sphinx/__init__.py test/test_sphinx_directive.py
git commit -m "Add d2.sphinx directive skeleton (inline body, single theme)"
```

---

## Task 5: File-path source support

**Files:**
- Modify: `d2/sphinx/directive.py`
- Modify: `test/test_sphinx_directive.py`

- [ ] **Step 1: Write failing test for file-path source**

Append to `test/test_sphinx_directive.py`:

```python
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
```

Note: `build_docs` creates `src/` and writes `index.rst` there; the test writes `shape.d2` into the same dir *before* calling `build_docs`. The helper uses `mkdir(exist_ok=True)` already? No — update the helper to tolerate pre-existing dirs. See Step 2.

- [ ] **Step 2: Make `build_docs` tolerate a pre-populated srcdir**

In `test/test_sphinx_directive.py`, change `src.mkdir()` to `src.mkdir(exist_ok=True)`.

- [ ] **Step 3: Run new test to verify it fails**

Run: `pytest test/test_sphinx_directive.py::test_file_path_source_renders_svg -v`
Expected: fails — directive currently ignores `self.arguments`.

- [ ] **Step 4: Add file-path resolution to `D2Directive.run`**

In `d2/sphinx/directive.py`, replace the body of `run()` up to the `source = ...` line with:

```python
    def run(self) -> list[dnodes.Node]:
        source, err = self._resolve_source()
        if err is not None:
            self.state.document.reporter.warning(err, line=self.lineno)
            return [d2_svg(svg=placeholder_svg(err))]

        library = self.options.get("library")
        theme = self.options.get("theme") or "light"
        # ... unchanged compile/cache/emit logic below
```

And add the helper method on `D2Directive`:

```python
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
```

- [ ] **Step 5: Run all directive tests to verify**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: both tests pass.

- [ ] **Step 6: Commit**

```bash
git add d2/sphinx/directive.py test/test_sphinx_directive.py
git commit -m "Support :file: path argument in d2 directive"
```

---

## Task 6: Dual-theme emission + `:class:` + `:align:` + `:alt:`

**Files:**
- Modify: `d2/sphinx/directive.py`
- Modify: `test/test_sphinx_directive.py`

- [ ] **Step 1: Write failing tests for dual emission**

Append to `test/test_sphinx_directive.py`:

```python
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
    # Two SVGs embedded
    assert html.count("<svg") == 2


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
    assert html.count("<svg") == 1
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: 4 new tests fail; the 2 existing ones still pass.

- [ ] **Step 3: Replace `run()` with the dual-emission version**

In `d2/sphinx/directive.py`, replace the whole `D2Directive` class with:

```python
class D2Directive(Directive):
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    has_content = True

    option_spec = {
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

        env = self.state.document.settings.env
        library = self.options.get("library") or env.app.config.d2_default_library
        theme_opt = self.options.get("theme")
        dual_default = env.app.config.d2_default_theme_dual
        if theme_opt is None and dual_default:
            variants = ["light", "dark"]
        else:
            variants = [theme_opt or "light"]

        cache_dir = Path(env.app.config.d2_cache_dir or (Path(env.app.outdir) / ".d2_cache"))

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

        container = dnodes.container(classes=["d2-container"] + extra_classes)
        if align:
            container["classes"].append(f"align-{align}")
        for variant, svg in svgs:
            wrap_classes = [f"only-{variant}"] + extra_classes
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
        # Inject aria-label on the opening <svg …> tag.
        head_end = svg.find(">")
        if head_end == -1 or not svg.startswith("<svg"):
            return svg
        return svg[:head_end] + f' aria-label="{alt}"' + svg[head_end:]

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
```

- [ ] **Step 4: Register config values in `d2/sphinx/__init__.py`**

Replace the contents of `d2/sphinx/__init__.py` with:

```python
"""Sphinx extension entry point for the ``.. d2::`` directive.

Sphinx is imported lazily inside :func:`setup` so ``import d2`` remains
free of optional dependencies.
"""

from __future__ import annotations

from typing import Any


def setup(app: Any) -> dict[str, Any]:
    from d2.sphinx.directive import D2Directive
    from d2.sphinx.nodes import d2_svg, depart_d2_svg_html, visit_d2_svg_html

    app.add_node(d2_svg, html=(visit_d2_svg_html, depart_d2_svg_html))
    app.add_directive("d2", D2Directive)

    app.add_config_value("d2_default_library", None, "env")
    app.add_config_value("d2_default_theme_dual", True, "env")
    app.add_config_value("d2_cache_dir", None, "env")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

- [ ] **Step 5: Run all directive tests to verify**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: all 6 tests pass.

- [ ] **Step 6: Commit**

```bash
git add d2/sphinx/directive.py d2/sphinx/__init__.py test/test_sphinx_directive.py
git commit -m "Emit dual light/dark SVGs by default with class and alt options"
```

---

## Task 7: File-mode output (`:inline: false`)

**Files:**
- Modify: `d2/sphinx/directive.py`
- Modify: `test/test_sphinx_directive.py`

- [ ] **Step 1: Write failing test for file-mode output**

Append to `test/test_sphinx_directive.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_sphinx_directive.py::test_inline_false_emits_img_and_writes_file -v`
Expected: fails — `:inline:` not in option_spec.

- [ ] **Step 3: Add `:inline:` option and file-mode emit**

In `d2/sphinx/directive.py`:

Add helper below the existing option validators:

```python
def _bool_option(value: str | None) -> bool:
    if value is None or value == "":
        return True
    lowered = value.strip().lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False
    raise ValueError(f"invalid :inline: {value!r}")
```

Extend `option_spec` inside `D2Directive`:

```python
    option_spec = {
        "library": _library_option,
        "theme": _theme_option,
        "alt": directives.unchanged,
        "class": directives.class_option,
        "align": lambda v: directives.choice(v, ("left", "center", "right")),
        "name": directives.unchanged,
        "inline": _bool_option,
    }
```

At the end of `run()`, branch on inline mode. Replace the final `return self._emit_inline(svgs)` with:

```python
        if self.options.get("inline", True):
            return self._emit_inline(svgs)
        return self._emit_files(svgs, source, library)
```

Add the `_emit_files` helper on `D2Directive`. This version preserves the XML declaration (file-mode SVGs stand alone) and uses the **unstripped** SVG, so we need the raw bytes before stripping. Adjust the compile loop: keep both versions per variant. Replace the compile loop in `run()` with:

```python
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
```

And update `_emit_inline` to unpack the 3-tuple (use index 1 for inline SVG):

```python
    def _emit_inline(self, svgs: list[tuple[str, str, str]]) -> list[dnodes.Node]:
        extra_classes = self.options.get("class", []) or []
        align = self.options.get("align")
        alt = self.options.get("alt")

        if len(svgs) == 1:
            node = d2_svg(svg=self._wrap_with_alt(svgs[0][1], alt))
            self._apply_wrapper_attrs(node, extra_classes, align)
            return [node]

        container = dnodes.container(classes=["d2-container"] + extra_classes)
        if align:
            container["classes"].append(f"align-{align}")
        for variant, inline_svg, _raw in svgs:
            wrap_classes = [f"only-{variant}"] + extra_classes
            inner = dnodes.container(classes=wrap_classes)
            inner += d2_svg(svg=self._wrap_with_alt(inline_svg, alt))
            container += inner
        return [container]
```

Add the `_emit_files` method:

```python
    def _emit_files(
        self,
        svgs: list[tuple[str, str, str]],
        source: str,
        library: str | None,
    ) -> list[dnodes.Node]:
        env = self.state.document.settings.env
        imagedir = Path(env.app.outdir) / env.app.builder.imagedir
        imagedir.mkdir(parents=True, exist_ok=True)

        extra_classes = self.options.get("class", []) or []
        align = self.options.get("align")
        alt = self.options.get("alt") or ""

        images: list[dnodes.Node] = []
        for variant, _inline, raw in svgs:
            key = cache.make_key(source, library, variant, d2.__version__)
            suffix = "" if variant == "light" else "-dark"
            filename = f"d2-{key[:12]}{suffix}.svg"
            (imagedir / filename).write_text(raw, encoding="utf-8")
            img = dnodes.image(
                uri=f"{env.app.builder.imagedir}/{filename}",
                alt=alt,
                classes=(
                    ([f"only-{variant}"] if len(svgs) > 1 else []) + extra_classes
                ),
            )
            if align:
                img["align"] = align
            images.append(img)

        if len(images) == 1:
            return images
        container = dnodes.container(classes=["d2-container"] + extra_classes)
        for img in images:
            container += img
        return [container]
```

- [ ] **Step 4: Run all directive tests to verify**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: all 7 tests pass.

- [ ] **Step 5: Commit**

```bash
git add d2/sphinx/directive.py test/test_sphinx_directive.py
git commit -m "Add :inline: false file-mode output for d2 directive"
```

---

## Task 8: Error-path tests and behavior

**Files:**
- Modify: `test/test_sphinx_directive.py`
- Modify: `d2/sphinx/directive.py` (only if tests reveal gaps)

- [ ] **Step 1: Write failing tests for each error branch**

Append to `test/test_sphinx_directive.py`:

```python
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
    html, warnings = build_docs(tmp_path, rst)
    # Invalid option values raise during parsing; docutils logs them as errors
    assert "invalid" in warnings.lower() or "bogus" in warnings.lower()
```

- [ ] **Step 2: Run tests to verify they pass or fail correctly**

Run: `pytest test/test_sphinx_directive.py -v`
Expected: all prior tests still pass; new error-path tests pass. If any new test fails, tweak the directive's error message to match what the test asserts, or tweak the assertion.

- [ ] **Step 3: Commit**

```bash
git add test/test_sphinx_directive.py
# Plus any directive.py adjustments that were needed
git commit -m "Add error-path tests for d2 directive"
```

---

## Task 9: Cache-hit integration test

**Files:**
- Modify: `test/test_sphinx_directive.py`

- [ ] **Step 1: Write failing test for cache persistence**

Append to `test/test_sphinx_directive.py`:

```python
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
```

Note: `build_docs` uses `freshenv=True` which rebuilds Sphinx from scratch; the cache lives under `outdir/.d2_cache` which `build_docs` does not delete between calls. The second run hits the cache.

- [ ] **Step 2: Run test**

Run: `pytest test/test_sphinx_directive.py::test_second_build_is_a_cache_hit -v`
Expected: passed.

- [ ] **Step 3: Commit**

```bash
git add test/test_sphinx_directive.py
git commit -m "Add cache-hit integration test for d2 directive"
```

---

## Task 10: Install Sphinx in the test sessions and add `sphinx_tests`

**Files:**
- Modify: `noxfile.py`

- [ ] **Step 1: Edit `tests` session to install the sphinx extra**

In `noxfile.py`, change the `tests` session body from:

```python
@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "test/", "-v", *session.posargs)
```

to:

```python
@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("pytest")
    session.install("-e", ".[sphinx]")
    session.run("pytest", "test/", "-v", *session.posargs)
```

- [ ] **Step 2: Add a `sphinx_tests` session**

Append after the existing `tests` session in `noxfile.py`:

```python
@nox.session(python=PYTHON_VERSIONS)
def sphinx_tests(session: nox.Session) -> None:
    """Run only the Sphinx directive tests."""
    session.install("pytest")
    session.install("-e", ".[sphinx]")
    session.run(
        "pytest",
        "test/test_sphinx_directive.py",
        "test/test_sphinx_cache.py",
        "test/test_sphinx_nodes.py",
        "-v",
        *session.posargs,
    )
```

- [ ] **Step 3: Run the new session locally**

Run: `nox -s sphinx_tests-3.12`
Expected: all tests pass.

- [ ] **Step 4: Run the full suite to confirm no regressions**

Run: `nox -s tests-3.12`
Expected: all tests pass — existing `test_d2.py`, the new sphinx tests, plus whatever other tests are currently present.

- [ ] **Step 5: Commit**

```bash
git add noxfile.py
git commit -m "Add sphinx extra to tests session and sphinx_tests session"
```

---

## Task 11: Enable the directive in this repo's docs

**Files:**
- Modify: `docs/conf.py`

- [ ] **Step 1: Append `"d2.sphinx"` to extensions**

In `docs/conf.py`, change:

```python
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]
```

to:

```python
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "d2.sphinx",
]
```

- [ ] **Step 2: Verify docs still build**

Run: `nox -s docs`
Expected: build succeeds; the directive is registered but no page uses it yet.

- [ ] **Step 3: Commit**

```bash
git add docs/conf.py
git commit -m "Enable d2.sphinx extension in project docs"
```

---

## Task 12: Migrate `docs/examples.rst` to the directive

**Files:**
- Modify: `docs/examples.rst`

- [ ] **Step 1: Replace one example as a smoke test**

Replace the "Basic Diagram" section block that currently reads:

```rst
.. image:: _static/example-basic.svg
   :alt: Basic diagram
   :align: center
   :class: only-light

.. image:: _static/example-basic-dark.svg
   :alt: Basic diagram
   :align: center
   :class: only-dark
```

with:

```rst
.. d2::
   :alt: Basic diagram
   :align: center

   x -> y -> z
```

- [ ] **Step 2: Verify the docs build**

Run: `nox -s docs`
Expected: succeeds; the generated `docs/_build/html/examples.html` contains two inlined `<svg>` elements wrapped in `only-light` / `only-dark` containers where the "Basic Diagram" section sits. Check by grepping:
`grep -c 'only-light' docs/_build/html/examples.html`
Expected: increments by 1 versus the pre-change build.

- [ ] **Step 3: Repeat for each remaining example**

For every other example section (Signal Chain, Nested Subsystems, RF Receiver, Dark Theme, SW Agent Pipeline, SW Workflow Comparison, SW Microservice Architecture, SW Dark Theme):

- The preceding `.. code-block:: python` block stays (it shows the Python API call).
- Strip the `with open(...)` lines inside the code block where they exist — the user can now see the rendering directly. (Optional — keep if you prefer a complete example.)
- Replace the `.. image::` pair (or single image for non-dual sections) with a single `.. d2::` directive that carries the **same D2 source** from the Python string (inline body) plus the appropriate `:library:` option. For dark-only sections (current "Dark Theme" and "SW Dark Theme"), use `:theme: dark`.

Example — Signal Chain replacement:

```rst
.. d2::
   :library: adi
   :alt: Signal chain example
   :align: center

   direction: right

   sensor: ADXL345 { class: sensor }
   amp: LT6230 { class: amplifier }
   filt: LTC1560 { class: filter-lp }
   adc: AD7606 { class: adc }
   dsp: ADSP-21489 { class: dsp-fpga }

   sensor -> amp: Analog { class: adi-signal-analog }
   amp -> filt: Amplified { class: adi-signal-analog }
   filt -> adc: Filtered { class: adi-signal-analog }
   adc -> dsp: SPI { class: adi-signal-digital }

   clk: AD9520 { class: clock }
   clk -> adc: MCLK { class: adi-signal-clock }
```

- [ ] **Step 4: Rebuild docs after each section and spot-check**

After each replacement:
Run: `nox -s docs`
Open `docs/_build/html/examples.html` and confirm the diagram renders in both light and dark modes. (Toggle via Furo's theme switch.)

- [ ] **Step 5: Commit once all sections migrate**

```bash
git add docs/examples.rst
git commit -m "Migrate examples.rst to the .. d2:: directive"
```

---

## Task 13: Audit and remove superseded files

**Files:**
- Delete (conditional): `scripts/update_example_svgs.py`, `scripts/check_svg_backgrounds.py`, `test/test_check_svg_backgrounds.py`, `test/test_sphinx_dark_examples.py`
- Delete: `docs/_static/example-*.svg` (any no longer referenced)

- [ ] **Step 1: List all remaining references to `_static/example-*.svg`**

Run: `grep -rn "example-[a-z-]*\.svg" docs/ README.md`
Record every file that still references one.

- [ ] **Step 2: Delete `_static/example-*.svg` files with no remaining references**

For each file in `docs/_static/` whose name matches `example-*.svg` and that does not appear in the grep output from Step 1:

```bash
git rm docs/_static/example-<name>.svg
```

Do NOT delete `logo.svg`, `all-components.svg`, `containers-example.svg`, `signal-chain-example.svg`, or `_static/icons/` — the spec explicitly calls these out as kept.

- [ ] **Step 3: Read the three candidate helper scripts and test files**

Open `scripts/update_example_svgs.py`, `scripts/check_svg_backgrounds.py`, `test/test_check_svg_backgrounds.py`, `test/test_sphinx_dark_examples.py`. For each, determine whether it operates on the deleted `example-*.svg` files only, or on files that are still referenced.

- [ ] **Step 4: `scripts/update_example_svgs.py` — delete**

This script regenerated the pre-rendered examples and is fully superseded. Run:

```bash
git rm scripts/update_example_svgs.py
```

- [ ] **Step 5: `scripts/check_svg_backgrounds.py` — delete iff it only touches deleted SVGs**

If Step 3 showed the script inspects files under `_static/example-*.svg` only, delete it. If it also inspects the retained SVGs (logo, all-components, etc.), keep it.

- [ ] **Step 6: `test/test_check_svg_backgrounds.py` and `test/test_sphinx_dark_examples.py` — delete iff fully superseded**

Apply the same criterion as Step 5. If a test only validated the pre-rendered example SVGs or the pre-rendered HTML output that used them, delete it. If it guards something else, keep it.

- [ ] **Step 7: Run the full test and docs build**

Run: `nox -s tests-3.12 && nox -s docs`
Expected: both succeed.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "Remove example SVGs and helpers superseded by d2 directive"
```

---

## Task 14: Update `CLAUDE.md` test listing

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update the Tests bullet**

In `CLAUDE.md`, replace the current "Tests" bullet under "Key Conventions" with one that accurately lists the post-Task-13 set of test files. For example (adjust per what Task 13 kept):

```markdown
- **Tests**: live in `test/` — compilation smoke tests in `test_d2.py`, Sphinx directive/cache/node tests in `test_sphinx_directive.py`, `test_sphinx_cache.py`, `test_sphinx_nodes.py`. Compilation tests assert `"<?xml"` appears in output; directive tests drive end-to-end Sphinx builds.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Update CLAUDE.md test listing"
```

---

## Self-Review

**Spec coverage:**

- Distribution as subpackage (`extensions = ["d2.sphinx"]`) → Task 4, 6
- Inline body + file path support → Tasks 4, 5
- Dual-theme emission with `only-light` / `only-dark` wrappers → Task 6
- `:theme:` forces single variant → Task 6
- Disk cache keyed by SHA-256 of (source, library, theme, version) → Tasks 2, 4, 6
- Two-char fanout → Task 2
- Version invalidation baked into the key → Task 2
- Inline `<svg>` default; `:inline: false` file-mode → Task 7
- Warning + placeholder on failure; works with `-W` → Tasks 3, 8
- Config values (`d2_default_library`, `d2_default_theme_dual`, `d2_cache_dir`) → Task 6
- `:alt:`, `:align:`, `:class:`, `:name:` options → Task 6
- Placeholder SVG spec → Task 3
- Unit tests for cache → Task 2
- End-to-end Sphinx build tests → Tasks 4–9
- `nox -s sphinx_tests` session → Task 10
- Docs migration: conf.py, examples.rst, file cleanup → Tasks 11–13
- CLAUDE.md test listing update → Task 14
- `[sphinx]` optional extra, `docs` extra pulls it in → Task 1

No gaps.

**Placeholder scan:** no "TBD" / "TODO" / "add error handling" placeholders; each code step shows complete code.

**Type consistency:** `d2_svg` node name, `placeholder_svg`, `make_key`, `cache_path`, `get`, `put`, `D2Directive`, `_resolve_source`, `_emit_inline`, `_emit_files`, `_strip_xml_declaration`, `_wrap_with_alt`, `_apply_wrapper_attrs`, `_library_option`, `_theme_option`, `_bool_option`, config values `d2_default_library` / `d2_default_theme_dual` / `d2_cache_dir` — all consistent across tasks.
