# `clean` — A Cohesive Technical Diagramming Library

**Date:** 2026-06-07
**Status:** Approved design

## Overview

Add a fifth D2 component library, `clean`, to pyd2lang-native. It provides a
cohesive, calm technical-diagramming aesthetic inspired by Anthropic and OpenAI:
flat (no shadows), hairline borders, generous corner radius, a restrained
cool-neutral tint scale for category grouping, and a single Anthropic-clay
accent reserved for emphasis. Light and dark themes are both provided.

It is added alongside the existing `adi`, `sw`, `jif`, and `datax` libraries —
those are left untouched. Like `sw` and `datax`, `clean` is hand-styled (no
base64-embedded icons), so `scripts/embed_icons.py` and the `embed_check` drift
gate do not apply; the Python constants are kept in sync by hand.

## Goals

- A single, cohesive look-and-feel that reads as intentional and refined, not as
  the rainbow-of-fills approach the existing libraries use.
- Enough semantic range (tint + shape) that real architecture diagrams remain
  legible at scale.
- Full light/dark parity.
- `d2.compile(code, library="clean", theme="light"|"dark")` works end to end.

## Non-Goals

- No embedded SVG icons (this is a shape/fill class library, like `sw`/`datax`).
- No changes to existing libraries' themes or outputs.
- No new public API surface beyond the new `library="clean"` value and the
  `CLEAN_COMPONENTS` / `CLEAN_THEME_CLASSES` reference constants.

## Aesthetic Direction

Blend of Anthropic (warm/editorial) and OpenAI (neutral/clinical): a neutral
grayscale base for restraint, with one warm clay accent for emphasis and primary
flows. Encoding strategy **B**: 2–3 cool-neutral tints group categories, shape
encodes type, clay is reserved for emphasis. No drop shadows anywhere.

### Palette — Light

| Role | Value |
|---|---|
| Ink (text) | `#1F1E1C` |
| Hairline border (default) | `#D6D3CA` |
| Paper fill (compute) | `#FFFFFF` |
| Slate tint fill (data) | `#EEF1F4` |
| Slate tint border | `#C3CBD4` |
| Muted fill (external) | `#F4F2ED` |
| Muted border | `#DAD6CC` (dashed) |
| Clay accent — stroke | `#BD5B3A` |
| Clay accent — fill | `#F7EAE2` |
| Clay accent — text | `#8F4023` |
| Flow edge (default) | `#9C988C` |

### Palette — Dark

| Role | Value |
|---|---|
| Ink (text) | `#ECEAE3` |
| Paper fill (compute) | `#242320` |
| Paper border | `#3A3833` |
| Slate tint fill (data) | `#232A30` |
| Slate tint border | `#3A4650` |
| Muted border | dashed `#3A3833` |
| Clay accent — stroke | `#D98263` |
| Clay accent — fill | `#3A2A22` |
| Clay accent — text | `#E8A487` |
| Flow edge (default) | `#6E6A60` |

## Component Classes

Defined in `lib/clean/clean-components.d2`; mirrored as `d2.CLEAN_COMPONENTS`.
Semantics are conveyed by tint + shape. ~21 classes:

**Compute / paper tint**
- `clean-service` — rounded rect, paper, hairline border (default service box)
- `clean-primary` — clay emphasis fill/stroke/text (the highlighted node)
- `clean-api` — rounded rect, paper
- `clean-gateway` — hexagon, paper
- `clean-function` — rounded rect, paper
- `clean-cloud` — cloud shape, paper

**Data / slate tint**
- `clean-database` — cylinder, slate tint
- `clean-cache` — rounded rect, slate tint
- `clean-storage` — cylinder, slate tint
- `clean-queue` — rounded rect, slate tint

**Actors**
- `clean-client` — rounded rect, paper
- `clean-browser` — rounded rect, paper
- `clean-mobile` — rounded rect, paper
- `clean-user` — person shape, paper
- `clean-external` — rounded rect, muted fill, dashed border (3rd-party system)

**AI**
- `clean-model` — rounded rect, paper (subtle emphasis)
- `clean-agent` — rounded rect, paper
- `clean-document` — page shape, paper

**Logic / structure**
- `clean-decision` — diamond, paper
- `clean-process` — rounded rect, paper
- `clean-group` — transparent container, hairline border (grouping/boundary)

## Theme Classes

Defined in `lib/clean/clean-theme.d2` (light) and `clean-theme-dark.d2` (dark);
mirrored as `d2.CLEAN_THEME_CLASSES`. The theme is prepended *after* components
so it can override component styles for the dark variant (matching the existing
`runmeLib` contract: `components + "\n" + theme + "\n" + userCode`).

- `clean-panel` — container, paper, hairline, rounded
- `clean-band` — container, slate tint
- `clean-title` — text, bold, large, ink
- `clean-subtitle` — text, muted
- `clean-label` — text, ink
- `clean-section-label` — text, bold, muted, small
- `clean-note` — text, italic, muted
- `clean-flow` — default edge, warm-gray stroke
- `clean-flow-primary` — clay edge (emphasis path)
- `clean-flow-muted` — light gray, thin
- `clean-flow-dashed` — dashed warm-gray edge

## Implementation Plan (Wiring)

1. **D2 assets** — create `lib/clean/clean-components.d2`,
   `lib/clean/clean-theme.d2`, `lib/clean/clean-theme-dark.d2`.
2. **Go shared library** — in `lib/d2lib.go`:
   - Add three `//go:embed clean/clean-*.d2` vars
     (`cleanComponents`, `cleanThemeLight`, `cleanThemeDark`).
   - Add `case "clean":` to the `runmeLib` switch selecting light/dark theme +
     components.
   - Update the `default:` error string to include `'clean'`.
3. **Rebuild** the shared library via `lib/build.sh` (requires the Go
   toolchain). Note: `d2/resources/` is not present in the source tree; the
   `.so`/`.dylib`/`.dll` is produced by this build step and by CI's
   cibuildwheel matrix.
4. **Python bindings** — in `d2/__init__.py`:
   - Add `CLEAN_COMPONENTS` and `CLEAN_THEME_CLASSES` reference lists.
   - Add `"clean"` to `_VALID_LIBRARIES`.
   - Update the `compile()` docstring to mention `"clean"`.
5. **Tests** — in `test/test_d2.py`, add smoke tests for `library="clean"` in
   both light and dark themes, asserting `"<?xml"` appears in output.
6. **Docs** — add `clean` to `CLAUDE.md` (Project Overview + Architecture +
   Key Conventions), and to any Sphinx docs that enumerate the libraries.

## Error Handling

- Unknown library names already raise `ValueError` in Python (via
  `_VALID_LIBRARIES`) before reaching Go; adding `"clean"` keeps that path
  intact.
- The Go `default:` branch's error string is updated so a stale binary missing
  the `clean` case still reports a meaningful message.

## Testing Strategy

- Smoke tests confirm compilation succeeds and returns SVG for `clean`
  light + dark (mirrors existing per-library tests).
- A representative diagram exercising several component classes and a
  `clean-flow-primary` edge is compiled in both themes to catch malformed D2.
- Existing tests for `adi`/`sw`/`jif`/`datax` must remain green (no regression).

## Risks / Notes

- Requires rebuilding the Go shared library; without a rebuilt `.so` the new
  library is unreachable at runtime even though the Python constants exist.
- Tint-based grouping must stay subtle enough to read as "clean" — fills are
  near-white/near-paper, with category distinction carried primarily by shape
  and border, not saturation.
