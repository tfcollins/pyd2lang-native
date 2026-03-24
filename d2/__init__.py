"""Bindings for the D2 Compiler"""

import ctypes
import os
import platform

__version__ = "0.0.4"

loc = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":
    lib_path = os.path.join(loc, "resources", "d2lib.lib")
elif platform.system() == "Linux":
    lib_path = os.path.join(loc, "resources", "d2lib.so")
else:
    lib_path = os.path.join(loc, "resources", "d2lib.dylib")

folder_path = os.path.join(loc, "resources")

if not os.path.exists(lib_path):
    if platform.system() == "Windows":
        # Try different extension
        lib_path = os.path.join(loc, "resources", "d2lib.dll")
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"Could not find {lib_path}")

library = ctypes.cdll.LoadLibrary(lib_path)

_runme = library.runme
_runme.argtypes = [ctypes.c_char_p]
_runme.restype = ctypes.c_char_p

_runme_adi = library.runmeAdi
_runme_adi.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_runme_adi.restype = ctypes.c_char_p

# ADI component class names for reference
ADI_COMPONENTS = [
    "adc",
    "dac",
    "amplifier",
    "filter-lp",
    "filter-bp",
    "filter-hp",
    "pll",
    "mixer",
    "oscillator",
    "comparator",
    "summer",
    "multiplexer",
    "switch",
    "voltage-reference",
    "voltage-regulator",
    "sensor",
    "dsp-fpga",
    "clock",
    "driver",
    "isolator",
    "attenuator",
]

# ADI theme class names for reference
ADI_THEME_CLASSES = [
    "adi-container",
    "adi-signal",
    "adi-signal-analog",
    "adi-signal-digital",
    "adi-signal-clock",
    "adi-signal-power",
    "adi-title",
    "adi-note",
]


def compile(code: str, adi: bool = False, theme: str = "light") -> str | None:
    """Compile D2 diagram code to SVG.

    Args:
        code: D2 diagram source code.
        adi: If True, include Analog Devices component library
            (ADC, DAC, amplifier, filter, PLL, mixer, etc.) and
            ADI brand theme classes.
        theme: Theme variant when adi=True. Either "light" or "dark".

    Returns:
        SVG string on success, None on failure.

    Raises:
        RuntimeError: If D2 compilation or rendering fails.
    """
    try:
        if adi:
            graph_bytes = _runme_adi(
                code.encode("utf-8"),
                theme.encode("utf-8"),
            )
        else:
            graph_bytes = _runme(code.encode("utf-8"))
        result = graph_bytes.decode("utf-8")
        if result.startswith("Error"):
            raise RuntimeError(result)
        return result
    except RuntimeError:
        raise
    except Exception as e:
        print(e)
        return None
