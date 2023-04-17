from ansys.fluent.core.filereader import lispy

scm_pys = (
    ("()", []),
    ("1", 1),
    ('""', '""'),
    ("(1)", [1]),
    ("(1 2)", [1, 2]),
    ("(1 (2))", [1, [2]]),
    ("(1 . 2)", (1, 2)),
    ("(1 2 3)", [1, 2, 3]),
    # In fact, (1 2 . 3) = (1 . (2 . 3))
    ("(1 2 . 3)", (1, (2, 3)), "(1 . (2 . 3))"),
    ("(1 (2 . 3))", [1, (2, 3)]),
    ("((1 . 2) . 3)", ((1, 2), 3)),
    ("(1 . (2 . 3))", (1, (2, 3))),
    ("((1 . 2) (3 . 4))", [(1, 2), (3, 4)]),
    ("((1 . 2) (3 . 4) (5 . 6))", [(1, 2), (3, 4), (5, 6)]),
    ("((1 . 2) . (3 . 4))", ((1, 2), (3, 4))),
    ("((1 . 2) . 3)", ((1, 2), 3)),
    ("(x 1)", ["x", 1]),
    ('(x . "1.0 [m/s]")', ("x", '"1.0 [m/s]"')),
    ("(define x 1)", ["define", "x", 1]),
)

extra_scm_pys = (
    ("(define x)", ["define", "x", None]),
    ('(define "x")', []),
)


def test_scm_to_py():
    for scm_py in scm_pys + extra_scm_pys:
        assert lispy.parse(scm_py[0]) == scm_py[1]


def test_py_to_scm():
    for scm_py in scm_pys:
        expec = scm_py[2] if len(scm_py) == 3 else scm_py[0]
        assert lispy.to_string(scm_py[1]) == expec
