<p align="center">
  <img src="docs/_static/logo.svg" alt="pyd2lang-native" width="400">
</p>

[![Build](https://github.com/tfcollins/pyd2lang-native/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/tfcollins/pyd2lang-native/actions/workflows/build_wheels.yml)
[![Docs](https://github.com/tfcollins/pyd2lang-native/actions/workflows/docs.yml/badge.svg)](https://github.com/tfcollins/pyd2lang-native/actions/workflows/docs.yml)
[![PyPI](https://img.shields.io/pypi/v/pyd2lang-native)](https://pypi.org/project/pyd2lang-native/)
[![Python](https://img.shields.io/pypi/pyversions/pyd2lang-native)](https://pypi.org/project/pyd2lang-native/)
[![License](https://img.shields.io/github/license/tfcollins/pyd2lang-native)](https://github.com/tfcollins/pyd2lang-native/blob/main/LICENSE)

Native Python bindings for [d2lang](https://d2lang.com), the modern text-to-diagram language. Compile D2 diagram source code to SVG directly from Python — no CLI tools or subprocesses required.

Includes a built-in **Analog Devices (ADI) component library** with 64 signal chain shapes (ADCs, DACs, amplifiers, filters, PLLs, power management, RF, interfaces, and more) plus light and dark ADI-branded themes.

## Quick Start

```python
import d2

# Basic diagram
svg = d2.compile("x -> y -> z")

# ADI signal chain with branded theme
svg = d2.compile("""
  sensor: ADXL345 { class: sensor }
  amp: LT6230 { class: amplifier }
  adc: AD7606 { class: adc }
  dsp: ADSP-21489 { class: dsp-fpga }

  sensor -> amp -> adc -> dsp
""", adi=True)

# Dark theme variant
svg = d2.compile(code, adi=True, theme="dark")
```

## Installation

```bash
pip install pyd2lang-native
```

Pre-built wheels are available for Linux (x86_64, aarch64), macOS (Intel, Apple Silicon), and Windows.

## Documentation

Full documentation is available at the [project docs site](https://tfcollins.github.io/pyd2lang-native/).

## License

This project is licensed under the MPL-2.0 License. See the [LICENSE](https://github.com/tfcollins/pyd2lang-native/blob/main/LICENSE) file for details.

## Dependencies

The d2lang compiler is built as a native shared library (.so / .dll / .dylib) and bundled into platform-specific Python wheels.

- d2lang: [Project repo](https://github.com/analogdevicesinc/d2lang) and [License](https://github.com/tfcollins/pyd2lang-native/blob/main/D2_LICENSE.txt)