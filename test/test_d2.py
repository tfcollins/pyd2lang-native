import d2

def test_d2():

    code = "x -> y"
    graph = d2.compile(code)

    # Print summary instead of full SVG
    if graph and graph.startswith('<?xml'):
        print(f"D2 compilation successful - Generated SVG ({len(graph)} characters)")
    else:
        print("D2 compilation failed or returned unexpected result")

    assert graph is not None