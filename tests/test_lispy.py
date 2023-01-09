from ansys.fluent.core.filereader import lispy

scm_pys = (
    ("()", []),
    ("1", 1),
    ('""', '""'),
    ("(1)", [1]),
    ("(1 2)", [1, 2]),
    ("(1 . 2)", (1, 2)),
    ("(1 2 3)", [1, 2, 3]),
    ("(1 2 . 3)", [1, (2, 3)]),
    ("((1 . 2) . 3)", ((1, 2), 3)),
    ("(1 . (2 . 3))", (1, (2, 3))),
    ("((1 . 2)(3 . 4))", [(1, 2), (3, 4)]),
    ("((1 . 2) . (3 . 4))", ((1, 2), (3, 4))),
    ("((1 . 2) . 3)", ((1, 2), 3)),
    ("(x 1)", ["x", 1]),
    ('(x . "1.0 [m/s]")', ("x", '"1.0 [m/s]"')),  # should be "'1.0 [m/s]'" ?
    ("(define x 1)", ["define", "x", 1]),
    ("(define x)", ["define", "x", None]),
    ('(define "x")', []),
)


def test_read():

    for scm_py in scm_pys:
        assert lispy.parse(scm_py[0]) == scm_py[1]
