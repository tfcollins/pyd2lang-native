import d2

def test_d2():

    code = "x -> y"
    graph = d2.compile(code)

    print(graph)

    assert graph is not None