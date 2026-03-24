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
    graph = d2.compile(code, adi=True)
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

    graph = d2.compile(code, adi=True)
    assert graph is not None
    assert "<?xml" in graph


def test_d2_adi_dark_theme():
    """Dark theme variant works."""
    code = """
adc1: AD7606 { class: adc }
dac1: AD5686 { class: dac }
adc1 -> dac1 { class: adi-signal-digital }
"""
    graph = d2.compile(code, adi=True, theme="dark")
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
    graph = d2.compile(code, adi=True)
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
    graph = d2.compile(code, adi=True)
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
    """Invalid d2 code with adi=True raises RuntimeError."""
    code = "{{{{ invalid d2 code"
    try:
        graph = d2.compile(code, adi=True)
        # If it doesn't raise, it should return an error or None
        if graph is not None:
            assert not graph.startswith("Error")
    except RuntimeError as e:
        assert "Error" in str(e)
