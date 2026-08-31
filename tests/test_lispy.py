# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ansys.fluent.core.file_reader import lispy

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
    # A line nested within a multi-line buffer closes one string
    # and opens another. This results in an even quote count for that specific
    # line alone, but the cumulative buffer count remains odd.
    #
    # How the parser processes it line by line:
    # Line 1: '("string1\n'           -> Buffer quotes: 1 (Odd)  -> Keeps reading
    # Line 2: ' string2"\n "string3\n' -> Line quotes: 2 (Even)  -> Buffer quotes: 3 (Odd) -> Keeps reading
    # Line 3: ' string4")'            -> Line quotes: 1 (Odd)   -> Buffer quotes: 4 (Even) -> Finishes string
    (
        '("string1\n string2"\n "string3\n string4")',
        ['"string1\n string2"', '"string3\n string4"'],
        '("string1\n string2" "string3\n string4")',
    ),
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
        expected = scm_py[2] if len(scm_py) == 3 else scm_py[0]
        assert lispy.to_string(scm_py[1]) == expected
