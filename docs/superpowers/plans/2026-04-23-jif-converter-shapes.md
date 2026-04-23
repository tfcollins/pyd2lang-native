# JIF Converter Shapes Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render JIF `adc` and `dac` classes as common converter-outline shapes instead of parallelograms.

**Architecture:** Keep the public JIF class names unchanged. Replace only the ADC/DAC class definitions in `lib/jif/jif-components.d2` with icon-backed converter outlines; leave all other JIF styling and theme behavior intact.

**Tech Stack:** D2 class definitions embedded by Go, Python ctypes binding, pytest.

---

## Chunk 1: Converter Outline Classes

### Task 1: Add regression coverage

**Files:**
- Modify: `test/test_d2.py`
- Modify: `lib/jif/jif-components.d2`

- [ ] **Step 1: Write the failing test**

Add a JIF test that compiles ADC and DAC blocks and asserts the rendered SVG contains image-backed converter outlines.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test/test_d2.py::test_jif_adc_dac_use_converter_outline_icons -v`

Expected: FAIL because current JIF ADC/DAC classes render as parallelograms without images.

- [ ] **Step 3: Implement minimal class change**

Replace `shape: parallelogram` on `adc` and `dac` with base64 SVG `icon:` definitions using the recommended 5-sided outlines.

- [ ] **Step 4: Rebuild embedded library**

Run: `./lib/build.sh`

Expected: rebuilds `d2/resources/d2lib.so` with the updated embedded JIF definitions.

- [ ] **Step 5: Run focused tests**

Run: `python3 -m pytest test/test_d2.py::test_jif_adc_dac_use_converter_outline_icons test/test_d2.py::test_jif_basic_components test/test_d2.py::test_jif_dark_theme -v`

Expected: PASS.
