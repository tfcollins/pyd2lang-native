# Sphinx `.. d2::` directive — design spec

- **Date:** 2026-04-18
- **Status:** approved for planning

## Goal

Add a Sphinx directive that compiles D2 source into SVG using the native
`d2.compile()` API and embeds it in the rendered documentation. Ship the
directive as part of this package so third-party Sphinx projects can add one
extension and start authoring diagrams, and migrate this repo's own docs off
the pre-rendered `_static/*.svg` flow.

## Scope

Ships with the `pyd2lang-native` package and is also consumed by this repo's
own Sphinx build. Retires the manual `update_example_svgs.py` workflow for
example diagrams.

## Design decisions

| Decision | Choice |
|---|---|
| Distribution | Bundled subpackage `d2.sphinx`, loaded via `extensions = ["d2.sphinx"]` |
| Source | Inline D2 in the directive body **or** a file path given as the directive argument |
| Theme variants | Auto-emit both light and dark, wrapped in `only-light` / `only-dark` containers; `:theme:` overrides to a single variant |
| Code display | Render-only; callers author their own `.. code-block::` if they want the source visible |
| Caching | On-disk, keyed by SHA-256 of `(source, library, theme, d2.__version__)`; persists across builds |
| Output embedding | Inline `<svg>` by default; `:inline: false` writes to `_images/` and emits `<img>` |
| Failure mode | Sphinx warning + red-bordered placeholder SVG; build passes. Works with `-W` for CI strictness |

## Architecture

### File layout

```
d2/
├── __init__.py                   # unchanged
└── sphinx/
    ├── __init__.py               # public setup(app) — Sphinx entry point
    ├── directive.py              # D2Directive class, option parsing
    ├── cache.py                  # hash-based on-disk cache
    └── nodes.py                  # custom docutils node + HTML visitors
```

### Public surface

- String `"d2.sphinx"` appended to `extensions` in the user's `conf.py`.
- The `.. d2::` directive.

Everything under `d2.sphinx.*` is internal.

### Dependencies

- Add `[project.optional-dependencies] sphinx = ["sphinx>=6"]` in `pyproject.toml`.
- The existing `docs` extra gains `"pyd2lang-native[sphinx]"` as a self-reference
  so `pip install pyd2lang-native[docs]` continues to pull Sphinx in transitively.
- `import d2` must not import Sphinx. `d2/sphinx/__init__.py` imports Sphinx
  lazily inside `setup()`; top-level module-level imports are limited to stdlib
  and the `d2` package itself.

### `conf.py` configuration knobs

| Name | Default | Purpose |
|---|---|---|
| `d2_default_library` | `None` | Value used when a `.. d2::` call omits `:library:`. Accepts `None`, `"adi"`, `"sw"` |
| `d2_default_theme_dual` | `True` | When `False`, a directive without explicit `:theme:` emits a single variant instead of dual |
| `d2_cache_dir` | `<outdir>/.d2_cache` | Directory for the on-disk SVG cache |

## Directive

### Syntax

```rst
.. d2:: [optional-file-path]
   :library: adi | sw
   :theme: light | dark
   :inline: true | false
   :alt: Short alt text
   :align: left | center | right
   :class: extra css classes
   :name: anchor-id

   <inline D2 source — used when no path is given>
```

### Rules

- **Exactly one** of the positional file path **or** the directive content body.
  Both or neither → warning + placeholder.
- File paths resolve relative to the containing `.rst` file (same semantics as
  `literalinclude` and `figure`). Absolute paths pass through unchanged.
- `:theme:` explicitly set disables dual emission for that call (single SVG,
  no `only-light` / `only-dark` wrapper).
- Without `:theme:`, dual emission follows `d2_default_theme_dual`. When dual,
  two SVGs are emitted: one wrapped in `<div class="only-light">`, one in
  `<div class="only-dark">`. `:class:` values append to the wrapper alongside
  `only-light` / `only-dark`.
- `:alt:` is applied as an `aria-label` to both SVG wrappers and also mirrored
  onto file-mode `<img>` tags as `alt`.
- `:align:` maps to the container `<div>`'s alignment class matching Furo's
  conventions (`align-left`, `align-center`, `align-right`).

### Examples

```rst
.. d2:: diagrams/signal-chain.d2
   :library: adi
   :alt: ADI signal chain

.. d2::
   :library: sw

   client: Web App { class: sw-browser }
   api: API { class: sw-api }
   client -> api { class: sw-flow }

.. d2:: diagrams/plain.d2
   :theme: light
   :inline: false
```

## Data flow

```
parse .rst
  └─► D2Directive.run()
        │
        ├─ resolve source: inline body OR read file from relative path
        ├─ determine variants: [light, dark] if dual, else [theme]
        ├─ for each variant v:
        │    key = sha256(source + library + v + d2.__version__)
        │    svg = cache.get(key) or d2.compile(source, library=..., theme=v)
        │    cache.put(key, svg)  # on compile only
        │    strip leading <?xml ...?> declaration (for inline mode)
        ├─ build docutils node tree:
        │    if dual:   container[div.only-light[svg], div.only-dark[svg]]
        │    if single: container[svg]
        │    if inline=false: write <hash>.svg to _images, emit <img>
        └─ return node list
```

### Cache

- **Key:** `sha256(source + "\x00" + library + "\x00" + theme + "\x00" + d2.__version__)`.
  Null-byte separators prevent boundary-collision false hits.
- **Layout:** `<d2_cache_dir>/<first-2-hex-chars>/<full-hash>.svg`. The
  two-char fanout avoids 10k-file directories.
- **Invalidation:** bumping `d2.__version__` invalidates every entry because
  the version is part of the key. This is how embedded theme-file edits
  (baked into `lib/d2lib.so` at release time) get picked up without manual
  cache busting.
- **Eviction:** none in MVP. Cache grows monotonically until the user runs
  `rm -rf <d2_cache_dir>`. Documented behaviour.

### File-mode output (`:inline: false`)

- Uses Sphinx's `app.builder.imagedir` so assets copy to `_images/` through
  the standard pipeline.
- Filename: `d2-<first-12-hex-chars>.svg` for light, `d2-<first-12-hex-chars>-dark.svg`
  for dark. Twelve hex chars is collision-safe for any realistic diagram count.
- XML declaration is **preserved** in file-mode output (valid standalone SVG);
  it is **stripped** for inline mode (invalid inside HTML5).

## Error handling

All failures emit a Sphinx warning through
`self.state.document.reporter.warning(...)` (carries docname + line) and
render a placeholder SVG in the output. The build continues; `sphinx-build -W`
surfaces the warning as an error for CI strictness without any extra config.

| Condition | Handling |
|---|---|
| `d2.compile()` raises `RuntimeError` | Warn + placeholder |
| Both file path and inline body given | Warn + placeholder |
| Neither file path nor inline body given | Warn + placeholder |
| File path doesn't resolve / isn't readable | Warn + placeholder (message includes resolved absolute path) |
| Unknown `:library:` value | Warn + placeholder |
| Invalid `:theme:` value | Warn + placeholder |
| Invalid `:inline:` value | Warn + placeholder |

### Placeholder SVG

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="60"
     role="img" aria-label="D2 compile error">
  <rect width="100%" height="100%" fill="#fff5f5"
        stroke="#c53030" stroke-width="2"/>
  <text x="12" y="24" font-family="monospace" font-size="12"
        fill="#c53030">D2 compile error</text>
  <text x="12" y="44" font-family="monospace" font-size="11"
        fill="#742a2a">{truncated reason, ≤ 60 chars}</text>
</svg>
```

Same placeholder for both themes — the red-on-cream palette reads in light
and dark backgrounds and the visual break signals the problem clearly.

## Testing

New file: `test/test_sphinx_directive.py`.

### Unit tests

- `d2.sphinx.cache`: hash stability (same inputs → same key), put/get round-trip,
  two-char fanout, version-bump invalidation (bump `d2.__version__` in a
  `monkeypatch` and confirm cache miss).

### Directive tests (driven by `sphinx.testing.fixtures`)

- Fixture project at `test/fixtures/sphinx_directive/` with `conf.py` + `index.rst`
  exercising each directive variant: inline, file, dual-theme, forced single,
  `:inline: false`, deliberately broken.
- Assert on rendered HTML:
  - Dual-theme case contains two `<svg>` elements under `only-light` /
    `only-dark` wrappers.
  - File-mode case contains `<img src="_images/d2-…svg">` and the files
    exist under `_build/html/_images/`.
  - Broken-diagram case yields a recorded warning **and** the placeholder
    SVG text appears in the output.
  - Cache dir is populated after the first build; second build touches no
    new cache files (mtime snapshot before/after).

### Nox integration

- Add `nox -s sphinx_tests` running `pytest test/test_sphinx_directive.py`
  across the current Python matrix. Continues using `pytest`; no new tooling.

## Migration of this repo's docs

1. Append `"d2.sphinx"` to the `extensions` list in `docs/conf.py`.
2. Rewrite `docs/examples.rst`: keep the existing `.. code-block:: python`
   blocks (they teach users how to call the API) and replace each paired
   `.. image::` block with a single `.. d2::` call using the same D2 source
   inline plus `:library: adi` or `:library: sw`.
3. Delete `scripts/update_example_svgs.py` once the migration is verified.
4. Delete the 18 `docs/_static/example-*.svg` files once `examples.rst` no
   longer references them. Keep `logo.svg`, `all-components.svg`,
   `containers-example.svg`, `signal-chain-example.svg`, and `icons/` —
   they are referenced from `index.rst`, `shapes.rst`, `sw.rst`, and the
   README. Audit each keeper during implementation.
5. Revisit `scripts/check_svg_backgrounds.py`, `test/test_check_svg_backgrounds.py`,
   and `test/test_sphinx_dark_examples.py`. If they only validate the
   pre-rendered example SVGs, delete them. If they guard something else
   (e.g., the surviving icons), keep them. This decision deferred to the
   implementation phase because the answer depends on reading the scripts
   against the final kept-file list.
6. Update `CLAUDE.md`'s "Tests" line to reflect whatever test files remain
   after step 5.

## Out of scope

- Cache eviction policies (LRU, size caps).
- PNG or PDF output — SVG only.
- LaTeX / man-page builders — HTML builder only. A basic fallback that
  emits the `<img>` form for non-HTML builders can be added later; not in
  this spec.
- Anchored SVG internals (clickable nodes linking to other docs pages).
- Source-display option (`:show-source:`). Authors write a separate
  `.. code-block::` when they want the D2 source visible; this keeps the
  directive focused on a single job.
