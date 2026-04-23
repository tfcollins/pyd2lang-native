import base64
import re
import warnings

import pytest

import d2


def test_d2():
    """Basic compilation still works."""
    code = "x -> y"
    graph = d2.compile(code)

    if graph and graph.startswith("<?xml"):
        print(f"D2 compilation successful - Generated SVG ({len(graph)} characters)")
    else:
        print("D2 compilation failed or returned unexpected result")

    assert graph is not None


def test_d2_adi_components():
    """ADI component classes are available when adi=True."""
    code = """
direction: right
adc1: AD7606 { class: adc }
filt1: LTC1560 { class: filter-lp }
amp1: LT6230 { class: amplifier }
dac1: AD5686 { class: dac }

amp1 -> filt1: Analog { class: adi-signal-analog }
filt1 -> adc1: Filtered { class: adi-signal-analog }
adc1 -> dac1: SPI { class: adi-signal-digital }
"""
    graph = d2.compile(code, library="adi")
    assert graph is not None
    assert "<?xml" in graph
    # SVG should contain rendered image elements for the icon-based components
    assert "image" in graph.lower()


def test_d2_adi_all_components():
    """All 21 ADI component classes render without error."""
    lines = []
    for i, comp in enumerate(d2.ADI_COMPONENTS):
        lines.append(f"c{i}: {comp} {{ class: {comp} }}")
    code = "\n".join(lines)

    graph = d2.compile(code, library="adi")
    assert graph is not None
    assert "<?xml" in graph


def test_d2_adi_dark_theme():
    """Dark theme variant works."""
    code = """
adc1: AD7606 { class: adc }
dac1: AD5686 { class: dac }
adc1 -> dac1 { class: adi-signal-digital }
"""
    graph = d2.compile(code, library="adi", theme="dark")
    assert graph is not None
    assert "<?xml" in graph


def test_d2_adi_containers():
    """ADI containers work with nested components."""
    code = """
frontend: Analog Frontend {
  class: adi-container
  amp: LNA { class: amplifier }
  adc: AD7606 { class: adc }
  amp -> adc { class: adi-signal-analog }
}
"""
    graph = d2.compile(code, library="adi")
    assert graph is not None
    assert "<?xml" in graph


def test_d2_adi_signal_types():
    """All ADI signal type classes work."""
    code = """
a: A { class: adc }
b: B { class: dac }
a -> b: analog { class: adi-signal-analog }
a -> b: digital { class: adi-signal-digital }
a -> b: clock { class: adi-signal-clock }
a -> b: power { class: adi-signal-power }
a -> b: default { class: adi-signal }
"""
    graph = d2.compile(code, library="adi")
    assert graph is not None
    assert "<?xml" in graph


def test_d2_plain_unchanged():
    """Plain compile without ADI still works (backward compat)."""
    code = "a -> b -> c"
    graph = d2.compile(code)
    assert graph is not None
    assert "<?xml" in graph
    # Should NOT contain ADI-specific elements
    assert "adi-container" not in graph.lower()


def test_d2_adi_error_handling():
    """Invalid d2 code with library='adi' raises RuntimeError."""
    code = "{{{{ invalid d2 code"
    with pytest.raises(RuntimeError, match="Error"):
        d2.compile(code, library="adi")


# ── SW blockset tests ──


def test_sw_basic_components():
    """SW component classes render correctly."""
    code = """
direction: right
agent1: Auditor { class: sw-agent }
model1: LLM { class: sw-model }
tool1: Search { class: sw-tool }
doc1: Seed { class: sw-document }

doc1 -> agent1 { class: sw-flow-data }
agent1 -> tool1 { class: sw-flow }
agent1 -> model1 { class: sw-flow }
model1 -> agent1 { class: sw-flow-feedback }
"""
    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_all_components():
    """All 32 SW component classes render without error."""
    lines = []
    for i, comp in enumerate(d2.SW_COMPONENTS):
        lines.append(f"c{i}: {comp} {{ class: {comp} }}")
    code = "\n".join(lines)

    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_dark_theme():
    """Dark theme variant works for SW blockset."""
    code = """
a: Agent { class: sw-agent }
b: Model { class: sw-model }
a -> b { class: sw-flow }
"""
    graph = d2.compile(code, library="sw", theme="dark")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_containers():
    """SW container classes work with nested components."""
    code = """
section: Auditing Loop {
  class: sw-container
  agent: Auditor { class: sw-agent }
  model: Target { class: sw-model }
  agent -> model { class: sw-flow }
}
"""
    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_flow_types():
    """All SW flow classes render without error."""
    code = """
a: A { class: sw-server }
b: B { class: sw-database }
a -> b: default { class: sw-flow }
a -> b: data { class: sw-flow-data }
a -> b: control { class: sw-flow-control }
a -> b: async { class: sw-flow-async }
a -> b: error { class: sw-flow-error }
a -> b: success { class: sw-flow-success }
a -> b: feedback { class: sw-flow-feedback }
a -> b: light { class: sw-flow-light }
"""
    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_jif_basic_components():
    """JIF component classes render correctly."""
    code = """
direction: right
adc: ADC { class: adc }
ddc: DDC { class: ddc }
framer: JESD204 Framer { class: jesd204framer }

adc -> ddc -> framer
"""
    graph = d2.compile(code, library="jif")
    assert graph is not None
    assert "<?xml" in graph


def test_jif_adc_dac_use_converter_outline_icons():
    """JIF ADC/DAC classes render as balanced converter-outline icons."""
    code = """
direction: right
adc: ADC { class: adc }
dac: DAC { class: dac }
adc -> dac
"""
    graph = d2.compile(code, library="jif")
    assert graph is not None
    assert "<?xml" in graph
    assert "image" in graph.lower()
    encoded_icons = re.findall(r"data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)", graph)
    assert len(encoded_icons) >= 2

    decoded_icons = [base64.b64decode(icon).decode("utf-8") for icon in encoded_icons[:2]]
    assert 'points="2,2 82,2 118,40 82,78 2,78"' in decoded_icons[0]
    assert 'points="58,2 138,2 138,78 58,78 22,40"' in decoded_icons[1]


def test_jif_all_components():
    """All JIF component classes render without error."""
    lines = []
    for i, comp in enumerate(d2.JIF_COMPONENTS):
        lines.append(f"c{i}: {comp} {{ class: {comp} }}")
    code = "\n".join(lines)

    graph = d2.compile(code, library="jif")
    assert graph is not None
    assert "<?xml" in graph


def test_jif_dark_theme():
    """Dark theme variant works for JIF blockset."""
    code = """
ref: REF_IN { class: input }
pll: CPLL { class: cpll }
out: OUT0 { class: out_clock_connected }
ref -> pll -> out
"""
    graph = d2.compile(code, library="jif", theme="dark")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_petri_workflow():
    """Petri-style workflow diagram with step highlights."""
    code = """
manual: Manual eval {
  class: sw-container-cream
  s1: Formulate hypothesis { class: sw-step-white }
  s2: Design scenarios { class: sw-step-blue }
  s3: Build environments { class: sw-step-amber }
  s4: Run models { class: sw-step-green }
  s1 -> s2 -> s3 -> s4 { class: sw-flow-light }
}

automated: Petri {
  class: sw-container-cream
  s1: Formulate hypothesis { class: sw-step-white }
  s2: Design scenarios { class: sw-step-blue }
  petri: Petri { class: sw-step-amber }
  s1 -> s2 -> petri { class: sw-flow-light }
}

manual.s3 -> automated.petri { class: sw-flow }
"""
    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_sw_agent_pipeline():
    """Agent pipeline with documents, agents, model, and scoring."""
    code = """
seeds: Inputs { class: sw-container-white
  a: Instruction A { class: sw-document }
  b: Instruction B { class: sw-document }
}

loop: Auditing { class: sw-container
  agent: Auditor { class: sw-agent }
  target: Target Model { class: sw-model }
  agent -> target { class: sw-flow }
  target -> agent { class: sw-flow-feedback }
}

scoring: Scoring { class: sw-container-cream
  judge: Judge { class: sw-eval }
  s1: Score { class: sw-score }
  judge -> s1 { class: sw-flow-light }
}

seeds -> loop { class: sw-flow-data }
loop -> scoring { class: sw-flow-data }
"""
    graph = d2.compile(code, library="sw")
    assert graph is not None
    assert "<?xml" in graph


def test_library_param_adi():
    """library='adi' works identically to adi=True."""
    code = """
adc1: AD7606 { class: adc }
dac1: AD5686 { class: dac }
adc1 -> dac1 { class: adi-signal-digital }
"""
    graph = d2.compile(code, library="adi")
    assert graph is not None
    assert "<?xml" in graph
    assert "image" in graph.lower()


def test_library_param_none():
    """library=None works identically to plain compile."""
    code = "x -> y -> z"
    graph = d2.compile(code, library=None)
    assert graph is not None
    assert "<?xml" in graph


def test_adi_deprecation_warning():
    """adi=True emits DeprecationWarning."""
    code = "x -> y"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        graph = d2.compile(code, adi=True)
        assert graph is not None
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "library='adi'" in str(w[0].message)


def test_adi_library_conflict():
    """Cannot specify both adi=True and library."""
    with pytest.raises(ValueError, match="Cannot specify both"):
        d2.compile("x -> y", adi=True, library="sw")


def test_invalid_library_name():
    """Unknown library name raises ValueError."""
    with pytest.raises(ValueError, match="Unknown library"):
        d2.compile("x -> y", library="nonexistent")


def test_sw_error_handling():
    """Invalid D2 code with library='sw' raises RuntimeError."""
    code = "{{{{ invalid d2 code"
    with pytest.raises(RuntimeError, match="Error"):
        d2.compile(code, library="sw")
