from ansys.fluent.core.filereader import lispy


def test_read():
    in_outs = [
        ["1", 1],
        ["(1)", [1]],
        ["(1 2)", [1, 2]],
        ["(1 . 2)", [1, 2]],
        ["(1 2 3)", [1, 2, 3]],
        ["(1 2 . 3)", [1, [2, 3]]],
        ["((1 . 2) . 3)", [[1, 2], 3]],
        ["(1 . (2 . 3))", [1, [2, 3]]],
        ["(x 1)", ["x", 1]],
        ['(x . "1.0 [m/s]")', ["x", "1.0 [m/s]"]],  # should be "'1.0 [m/s]'" ?
        ["(define x 1)", ["define", "x", 1]],
        ["(define x)", ["define", "x", None]],
        ['(define "x")', []],
    ]

    for in_out in in_outs:
        assert lispy.parse(in_out[0]) == in_out[1]
