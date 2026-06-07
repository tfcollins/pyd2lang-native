# `clean` Diagramming Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fifth D2 component library, `clean`, with a cohesive flat Anthropic/OpenAI-inspired aesthetic (neutral tint scale + single clay accent), in light and dark themes.

**Architecture:** Three hand-styled D2 asset files (`lib/clean/clean-components.d2`, `clean-theme.d2`, `clean-theme-dark.d2`) are embedded into the Go shared library via `//go:embed` and dispatched by a new `case "clean"` in `runmeLib`. The dark theme file redefines every component class (the Go contract prepends `components(light) + theme + userCode`, so dark relies on theme overrides). Python exposes `CLEAN_COMPONENTS` / `CLEAN_THEME_CLASSES` reference lists and accepts `library="clean"`.

**Tech Stack:** Go (c-shared build via `lib/build.sh`, requires Go toolchain), Python 3.10+ (ctypes), D2 class syntax, pytest, nox.

---

## File Structure

- **Create:** `lib/clean/clean-components.d2` — 21 node component classes (light values).
- **Create:** `lib/clean/clean-theme.d2` — 11 theme classes (panels, labels, flow edges), light.
- **Create:** `lib/clean/clean-theme-dark.d2` — 11 theme classes (dark) **plus** all 21 component classes redefined for dark.
- **Modify:** `lib/d2lib.go` — three `//go:embed` vars, a `case "clean"` in `runmeLib`, and the `default` error string.
- **Modify:** `d2/__init__.py` — `CLEAN_COMPONENTS`, `CLEAN_THEME_CLASSES`, `_VALID_LIBRARIES`, `compile()` docstring.
- **Modify:** `test/test_d2.py` — smoke tests for `clean` (basic, all components, theme/flow classes, dark theme).
- **Modify:** `CLAUDE.md` — Project Overview, Architecture, Key Conventions.
- **Rebuild artifact:** `d2/resources/d2lib.so` (produced by `lib/build.sh`; not committed to source tree).

---

## Task 1: Establish baseline build and green test suite

This proves the Go toolchain works and gives a working binary so later "red" steps fail for the right reason. `d2/resources/` is not in the source tree — it is produced by the build.

**Files:**
- Build: `lib/build.sh` (existing)

- [ ] **Step 1: Verify the Go toolchain is available**

Run: `go version`
Expected: prints a Go version (e.g. `go version go1.2x ...`). If this fails, stop — the toolchain must be installed before continuing.

- [ ] **Step 2: Build the current shared library**

Run: `bash lib/build.sh`
Expected: ends with `Done.` and creates `d2/resources/d2lib.so`.

- [ ] **Step 3: Confirm the existing test suite passes**

Run: `pytest test/test_d2.py -q`
Expected: all tests PASS (this is the pre-change baseline).

- [ ] **Step 4: No commit**

This task only verifies the environment; `d2/resources/` is gitignored/untracked and there are no source changes to commit.

---

## Task 2: Create the `clean` D2 asset files

**Files:**
- Create: `lib/clean/clean-components.d2`
- Create: `lib/clean/clean-theme.d2`
- Create: `lib/clean/clean-theme-dark.d2`

- [ ] **Step 1: Create `lib/clean/clean-components.d2`**

```d2
# clean component classes — flat, hairline-bordered, neutral tint scale.
# Semantics by tint + shape: paper=compute/actor/AI/logic, slate=data,
# clay=emphasis, muted+dashed=external. No drop shadows.

classes: {
  # ── Compute / paper ──
  clean-service: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-primary: {
    style.fill: "#F7EAE2"
    style.stroke: "#BD5B3A"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#8F4023"
    style.bold: true
  }
  clean-api: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-gateway: {
    shape: hexagon
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }
  clean-function: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-cloud: {
    shape: cloud
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }

  # ── Data / slate ──
  clean-database: {
    shape: cylinder
    style.fill: "#EEF1F4"
    style.stroke: "#C3CBD4"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }
  clean-cache: {
    style.fill: "#EEF1F4"
    style.stroke: "#C3CBD4"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-storage: {
    shape: cylinder
    style.fill: "#EEF1F4"
    style.stroke: "#C3CBD4"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }
  clean-queue: {
    style.fill: "#EEF1F4"
    style.stroke: "#C3CBD4"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }

  # ── Actors ──
  clean-client: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-browser: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-mobile: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-user: {
    shape: person
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }
  clean-external: {
    style.fill: "#F4F2ED"
    style.stroke: "#DAD6CC"
    style.stroke-width: 1
    style.stroke-dash: 4
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }

  # ── AI ──
  clean-model: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-agent: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-document: {
    shape: page
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }

  # ── Logic / structure ──
  clean-decision: {
    shape: diamond
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.font-color: "#1F1E1C"
  }
  clean-process: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#1F1E1C"
  }
  clean-group: {
    style.fill: "transparent"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 12
    style.font-color: "#6B6660"
  }
}
```

- [ ] **Step 2: Create `lib/clean/clean-theme.d2`** (light theme classes)

```d2
# clean light theme — panels, labels, and flow edges.

classes: {
  clean-panel: {
    style.fill: "#FFFFFF"
    style.stroke: "#D6D3CA"
    style.stroke-width: 1
    style.border-radius: 14
    style.font-color: "#1F1E1C"
  }
  clean-band: {
    style.fill: "#EEF1F4"
    style.stroke: "#C3CBD4"
    style.stroke-width: 1
    style.border-radius: 12
    style.font-color: "#4A5662"
  }
  clean-title: {
    shape: text
    style.font-size: 22
    style.font-color: "#1F1E1C"
    style.bold: true
  }
  clean-subtitle: {
    shape: text
    style.font-size: 14
    style.font-color: "#6B6660"
  }
  clean-label: {
    shape: text
    style.font-size: 13
    style.font-color: "#1F1E1C"
    style.bold: true
  }
  clean-section-label: {
    shape: text
    style.font-size: 12
    style.font-color: "#6B6660"
    style.bold: true
  }
  clean-note: {
    shape: text
    style.font-size: 12
    style.font-color: "#6B6660"
    style.italic: true
  }
  clean-flow: {
    style.stroke: "#9C988C"
    style.stroke-width: 2
    style.font-color: "#6B6660"
    style.font-size: 12
  }
  clean-flow-primary: {
    style.stroke: "#BD5B3A"
    style.stroke-width: 2
    style.font-color: "#8F4023"
    style.font-size: 12
  }
  clean-flow-muted: {
    style.stroke: "#CFCABE"
    style.stroke-width: 1
    style.font-color: "#6B6660"
    style.font-size: 12
  }
  clean-flow-dashed: {
    style.stroke: "#9C988C"
    style.stroke-width: 2
    style.stroke-dash: 5
    style.font-color: "#6B6660"
    style.font-size: 12
  }
}
```

- [ ] **Step 3: Create `lib/clean/clean-theme-dark.d2`** (dark theme classes + all components redefined dark)

```d2
# clean dark theme — theme classes plus every component class redefined for
# dark mode. The Go contract prepends components(light) + theme + userCode, so
# dark relies on these overrides taking precedence.

classes: {
  # ── Theme classes ──
  clean-panel: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 14
    style.font-color: "#ECEAE3"
  }
  clean-band: {
    style.fill: "#232A30"
    style.stroke: "#3A4650"
    style.stroke-width: 1
    style.border-radius: 12
    style.font-color: "#AEB9C4"
  }
  clean-title: {
    shape: text
    style.font-size: 22
    style.font-color: "#ECEAE3"
    style.bold: true
  }
  clean-subtitle: {
    shape: text
    style.font-size: 14
    style.font-color: "#9A958B"
  }
  clean-label: {
    shape: text
    style.font-size: 13
    style.font-color: "#ECEAE3"
    style.bold: true
  }
  clean-section-label: {
    shape: text
    style.font-size: 12
    style.font-color: "#9A958B"
    style.bold: true
  }
  clean-note: {
    shape: text
    style.font-size: 12
    style.font-color: "#9A958B"
    style.italic: true
  }
  clean-flow: {
    style.stroke: "#6E6A60"
    style.stroke-width: 2
    style.font-color: "#9A958B"
    style.font-size: 12
  }
  clean-flow-primary: {
    style.stroke: "#D98263"
    style.stroke-width: 2
    style.font-color: "#E8A487"
    style.font-size: 12
  }
  clean-flow-muted: {
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#9A958B"
    style.font-size: 12
  }
  clean-flow-dashed: {
    style.stroke: "#6E6A60"
    style.stroke-width: 2
    style.stroke-dash: 5
    style.font-color: "#9A958B"
    style.font-size: 12
  }

  # ── Components (dark) ──
  clean-service: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-primary: {
    style.fill: "#3A2A22"
    style.stroke: "#D98263"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#E8A487"
    style.bold: true
  }
  clean-api: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-gateway: {
    shape: hexagon
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-function: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-cloud: {
    shape: cloud
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-database: {
    shape: cylinder
    style.fill: "#232A30"
    style.stroke: "#3A4650"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-cache: {
    style.fill: "#232A30"
    style.stroke: "#3A4650"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-storage: {
    shape: cylinder
    style.fill: "#232A30"
    style.stroke: "#3A4650"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-queue: {
    style.fill: "#232A30"
    style.stroke: "#3A4650"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-client: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-browser: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-mobile: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-user: {
    shape: person
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-external: {
    style.fill: "#2A2826"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.stroke-dash: 4
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-model: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-agent: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-document: {
    shape: page
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-decision: {
    shape: diamond
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.font-color: "#ECEAE3"
  }
  clean-process: {
    style.fill: "#242320"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 10
    style.font-color: "#ECEAE3"
  }
  clean-group: {
    style.fill: "transparent"
    style.stroke: "#3A3833"
    style.stroke-width: 1
    style.border-radius: 12
    style.font-color: "#9A958B"
  }
}
```

- [ ] **Step 4: Commit**

```bash
git add lib/clean/clean-components.d2 lib/clean/clean-theme.d2 lib/clean/clean-theme-dark.d2
git commit -m "feat(clean): add clean library D2 asset files"
```

---

## Task 3: Wire the `clean` library into the Go shared library

**Files:**
- Modify: `lib/d2lib.go` (embed vars after the datax block ~line 55; switch in `runmeLib` ~line 135; default error ~line 143)

- [ ] **Step 1: Add the three `//go:embed` vars**

After the existing `dataxComponents` embed block (the line `var dataxComponents string`), add:

```go
//go:embed clean/clean-theme.d2
var cleanThemeLight string

//go:embed clean/clean-theme-dark.d2
var cleanThemeDark string

//go:embed clean/clean-components.d2
var cleanComponents string
```

- [ ] **Step 2: Add the `clean` case to the `runmeLib` switch**

In `runmeLib`, after the `case "datax":` block and before `default:`, add:

```go
	case "clean":
		if themeMode == "dark" {
			theme = cleanThemeDark
		} else {
			theme = cleanThemeLight
		}
		components = cleanComponents
```

- [ ] **Step 3: Update the `default` error string**

Replace:

```go
		return C.CString("Error: unknown library '" + library + "', expected 'adi', 'sw', 'jif', or 'datax'")
```

with:

```go
		return C.CString("Error: unknown library '" + library + "', expected 'adi', 'sw', 'jif', 'datax', or 'clean'")
```

- [ ] **Step 4: Verify the Go source compiles**

Run: `cd lib && go build ./... && cd ..`
Expected: no output, exit code 0 (embeds resolve, switch is valid Go).

- [ ] **Step 5: Commit**

```bash
git add lib/d2lib.go
git commit -m "feat(clean): embed and dispatch clean library in d2lib.go"
```

---

## Task 4: Add Python bindings for `clean`

**Files:**
- Modify: `d2/__init__.py` (add constants after `JIF_THEME_CLASSES` ~line 268; `_VALID_LIBRARIES` line 270; docstring ~line 283-289)

- [ ] **Step 1: Add `CLEAN_COMPONENTS` and `CLEAN_THEME_CLASSES`**

Immediately after the `JIF_THEME_CLASSES = [ ... ]` block and before `_VALID_LIBRARIES`, add:

```python
CLEAN_COMPONENTS = [
    "clean-service",
    "clean-primary",
    "clean-api",
    "clean-gateway",
    "clean-function",
    "clean-cloud",
    "clean-database",
    "clean-cache",
    "clean-storage",
    "clean-queue",
    "clean-client",
    "clean-browser",
    "clean-mobile",
    "clean-user",
    "clean-external",
    "clean-model",
    "clean-agent",
    "clean-document",
    "clean-decision",
    "clean-process",
    "clean-group",
]

CLEAN_THEME_CLASSES = [
    "clean-panel",
    "clean-band",
    "clean-title",
    "clean-subtitle",
    "clean-label",
    "clean-section-label",
    "clean-note",
    "clean-flow",
    "clean-flow-primary",
    "clean-flow-muted",
    "clean-flow-dashed",
]
```

- [ ] **Step 2: Add `"clean"` to `_VALID_LIBRARIES`**

Replace:

```python
_VALID_LIBRARIES = {"adi", "sw", "jif", "datax"}
```

with:

```python
_VALID_LIBRARIES = {"adi", "sw", "jif", "datax", "clean"}
```

- [ ] **Step 3: Update the `compile()` docstring**

Replace the `library:` parameter description:

```python
        library: Component library to include. Either ``"adi"`` for
            Analog Devices signal-chain components, ``"sw"`` for
            software/AI architecture components, ``"jif"`` for
            pyadi-jif block diagrams, ``"datax"`` for ADI DataX overview
            diagrams, or ``None`` for plain D2 compilation.
```

with:

```python
        library: Component library to include. Either ``"adi"`` for
            Analog Devices signal-chain components, ``"sw"`` for
            software/AI architecture components, ``"jif"`` for
            pyadi-jif block diagrams, ``"datax"`` for ADI DataX overview
            diagrams, ``"clean"`` for the flat neutral/clay technical
            diagramming components, or ``None`` for plain D2 compilation.
```

- [ ] **Step 4: Verify the module imports and exposes the constants**

Run: `python -c "import d2; print(len(d2.CLEAN_COMPONENTS), len(d2.CLEAN_THEME_CLASSES), 'clean' in d2._VALID_LIBRARIES)"`
Expected: `21 11 True`

- [ ] **Step 5: Commit**

```bash
git add d2/__init__.py
git commit -m "feat(clean): expose CLEAN_COMPONENTS/CLEAN_THEME_CLASSES and accept library='clean'"
```

---

## Task 5: Add tests for `clean` (red against the not-yet-rebuilt binary)

The Go change from Task 3 is not in `d2/resources/d2lib.so` until Task 6 rebuilds it. With `"clean"` already in `_VALID_LIBRARIES` (Task 4), these calls pass Python validation, reach the *old* binary's `default` branch, and raise `RuntimeError` — so the tests fail meaningfully now and pass after the rebuild.

**Files:**
- Modify: `test/test_d2.py` (append at end of file)

- [ ] **Step 1: Append the `clean` tests**

```python
# ── clean library tests ──


def test_clean_basic_components():
    """clean component classes render correctly."""
    code = """
direction: right
api: API { class: clean-api }
svc: Service { class: clean-primary }
db: Postgres { class: clean-database }
user: User { class: clean-user }

user -> api { class: clean-flow }
api -> svc { class: clean-flow-primary }
svc -> db { class: clean-flow }
"""
    graph = d2.compile(code, library="clean")
    assert graph is not None
    assert "<?xml" in graph
    # clay accent fill of clean-primary appears in light output
    assert "#F7EAE2" in graph


def test_clean_all_components():
    """All clean component classes render without error."""
    lines = []
    for i, comp in enumerate(d2.CLEAN_COMPONENTS):
        lines.append(f"c{i}: {comp} {{ class: {comp} }}")
    code = "\n".join(lines)

    graph = d2.compile(code, library="clean")
    assert graph is not None
    assert "<?xml" in graph


def test_clean_theme_and_flows():
    """clean theme/panel and all flow edge classes render without error."""
    code = """
panel: System { class: clean-panel
  band: Data Plane { class: clean-band
    cache: Cache { class: clean-cache }
    q: Queue { class: clean-queue }
  }
  a: A { class: clean-service }
  b: B { class: clean-service }
  a -> b: default { class: clean-flow }
  a -> b: primary { class: clean-flow-primary }
  a -> b: muted { class: clean-flow-muted }
  a -> b: dashed { class: clean-flow-dashed }
}
"""
    graph = d2.compile(code, library="clean")
    assert graph is not None
    assert "<?xml" in graph
    # slate band tint appears in light output
    assert "#EEF1F4" in graph


def test_clean_dark_theme():
    """Dark theme variant works for the clean library."""
    code = """
api: API { class: clean-api }
svc: Service { class: clean-primary }
api -> svc { class: clean-flow-primary }
"""
    graph = d2.compile(code, library="clean", theme="dark")
    assert graph is not None
    assert "<?xml" in graph
    # clay accent fill of clean-primary in dark output
    assert "#3A2A22" in graph


def test_clean_error_handling():
    """Invalid D2 code with library='clean' raises RuntimeError."""
    code = "{{{{ invalid d2 code"
    with pytest.raises(RuntimeError, match="Error"):
        d2.compile(code, library="clean")
```

- [ ] **Step 2: Run the new tests against the current binary to confirm they fail**

Run: `pytest test/test_d2.py -q -k clean`
Expected: FAIL. `test_clean_basic_components`, `test_clean_all_components`, `test_clean_theme_and_flows`, `test_clean_dark_theme` fail because the old binary returns `Error: unknown library 'clean'` (raised as `RuntimeError`, so the success-path assertions never run). `test_clean_error_handling` may already pass (it expects a RuntimeError) — that is fine.

- [ ] **Step 3: Commit the tests**

```bash
git add test/test_d2.py
git commit -m "test(clean): add smoke tests for clean library (red pre-rebuild)"
```

---

## Task 6: Rebuild the shared library and confirm green

**Files:**
- Build: `lib/build.sh`

- [ ] **Step 1: Rebuild the shared library with the `clean` case embedded**

Run: `bash lib/build.sh`
Expected: ends with `Done.`; `d2/resources/d2lib.so` is updated.

- [ ] **Step 2: Run the `clean` tests — now green**

Run: `pytest test/test_d2.py -q -k clean`
Expected: all 5 `clean` tests PASS.

- [ ] **Step 3: Run the full suite to confirm no regressions**

Run: `pytest test/test_d2.py -q`
Expected: all tests PASS (existing libraries unaffected).

- [ ] **Step 4: No commit**

The rebuilt `d2/resources/d2lib.so` is not tracked in source; nothing to commit here.

---

## Task 7: Update documentation

**Files:**
- Modify: `CLAUDE.md` (Project Overview line ~9; Architecture diagram lines ~35-58; Key Conventions, after the DataX bullet)

- [ ] **Step 1: Update the Project Overview sentence**

Replace:

```
Includes ADI signal-chain, SW software/AI, JIF, and DataX overview libraries with light/dark themes.
```

with:

```
Includes ADI signal-chain, SW software/AI, JIF, DataX overview, and clean (flat neutral/clay technical) libraries with light/dark themes.
```

- [ ] **Step 2: Update the Architecture section**

In the `compile(...)` signature line, replace `"adi"|"sw"|"jif"|"datax"|None` with `"adi"|"sw"|"jif"|"datax"|"clean"|None`.

After the `lib/datax/` line in the directory tree, add:

```
lib/clean/             clean assets: clean-components.d2 (21 classes), clean-theme.d2, clean-theme-dark.d2
```

- [ ] **Step 3: Add a Key Conventions bullet**

After the existing `- **DataX components**: ...` bullet, add:

```
- **clean components**: defined as hand-styled flat D2 classes in `lib/clean/` (neutral tint scale + single clay accent, no shadows, no embedded icons), exposed as `d2.CLEAN_COMPONENTS` and `d2.CLEAN_THEME_CLASSES`. The dark theme file (`clean-theme-dark.d2`) redefines every component class for dark mode. Edit the D2 files directly and keep the Python constants in sync by hand.
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(clean): document the clean library in CLAUDE.md"
```

---

## Task 8: Final quality gate

**Files:**
- All changed files

- [ ] **Step 1: Lint and formatting check**

Run: `nox -s lint && nox -s fmt_check`
Expected: both pass (only `d2/__init__.py` and `test/test_d2.py` are Python; D2/Go files are not linted by ruff).

- [ ] **Step 2: Full test run across the change**

Run: `pytest test/test_d2.py -q`
Expected: all PASS.

- [ ] **Step 3: Confirm the working tree is clean**

Run: `git status --short`
Expected: no uncommitted tracked changes (only the untracked, gitignored `d2/resources/` artifact, if shown).

---

## Self-Review Notes

- **Spec coverage:** palette (Task 2 D2 files), 21 components (Task 2/4), 11 theme classes (Task 2/4), Go wiring + error string (Task 3), rebuild dependency (Tasks 1/6), Python constants + `_VALID_LIBRARIES` + docstring (Task 4), tests light+dark (Tasks 5/6), docs (Task 7). All spec sections map to a task.
- **Naming consistency:** class names match exactly between `clean-components.d2`, `clean-theme-dark.d2` overrides, and `CLEAN_COMPONENTS` (21) / `CLEAN_THEME_CLASSES` (11).
- **Dark-override contract:** verified against `datax-theme-dark.d2`, which likewise redefines all component classes; `clean-theme-dark.d2` does the same.
- **Hex-assertion choices:** tests assert library-specific fills (`#F7EAE2`, `#EEF1F4`, `#3A2A22`) rather than generic `#FFFFFF` to avoid false positives, mirroring the datax tests' approach.
