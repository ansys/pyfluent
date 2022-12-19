from typing import Any, Dict

from google.protobuf.json_format import MessageToDict, ParseDict
import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer
from ansys.fluent.core.services.scheme_eval import (
    Symbol,
    _convert_py_value_to_scheme_pointer,
    _convert_scheme_pointer_to_py_value,
)


@pytest.mark.parametrize(
    "py_value,json_dict",
    [
        (None, {}),
        (False, {"b": False}),
        (True, {"b": True}),
        (5, {"fixednum": "5"}),
        (5.0, {"flonum": 5.0}),
        ("abc", {"str": "abc"}),
        ((), {}),
        (("abc",), {"list": {"item": [{"str": "abc"}]}}),
        (
            ("abc", 5.0),
            {
                "pair": {
                    "car": {"str": "abc"},
                    "cdr": {"flonum": 5.0},
                }
            },
        ),
        (
            (False, 5.0, "abc"),
            {"list": {"item": [{"b": False}, {"flonum": 5.0}, {"str": "abc"}]}},
        ),
        ([], {}),
        (["abc"], {"list": {"item": [{"str": "abc"}]}}),
        (
            [False, 5.0],
            {"list": {"item": [{"b": False}, {"flonum": 5.0}]}},
        ),
        ({}, {}),
        (
            {"a": 5.0},
            {
                "list": {
                    "item": [{"pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}}],
                }
            },
        ),
        (
            {"a": 5.0, "b": 10.0},
            {
                "list": {
                    "item": [
                        {"pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}},
                        {"pair": {"car": {"str": "b"}, "cdr": {"flonum": 10.0}}},
                    ]
                }
            },
        ),
        (
            [Symbol("+"), 2.0, 3.0],
            {"list": {"item": [{"sym": "+"}, {"flonum": 2.0}, {"flonum": 3.0}]}},
        ),
    ],
)
def test_convert_py_value_to_scheme_pointer(
    py_value: Any, json_dict: Dict[str, Any]
) -> None:
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p, "23.1.0")
    assert MessageToDict(p) == json_dict


@pytest.mark.parametrize(
    "py_value,json_dict",
    [
        (None, {}),
        (False, {"b": False}),
        (True, {"b": True}),
        (5, {"fixednum": "5"}),
        (5.0, {"flonum": 5.0}),
        ("abc", {"str": "abc"}),
        (["abc"], {"list": {"item": [{"str": "abc"}]}}),
        (("abc",), {"pair": {"car": {"str": "abc"}}}),
        (
            [False, 5.0, "abc"],
            {
                "list": {"item": [{"b": False}, {"flonum": 5.0}, {"str": "abc"}]},
            },
        ),
        (None, {}),
        (
            {"a": 5.0, "b": 10.0},
            {
                "list": {
                    "item": [
                        {"pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}},
                        {"pair": {"car": {"str": "b"}, "cdr": {"flonum": 10.0}}},
                    ]
                }
            },
        ),
        (
            {"a": [5.0, False], "b": [10.0, True]},
            {
                "list": {
                    "item": [
                        {
                            "pair": {
                                "car": {"str": "a"},
                                "cdr": {
                                    "list": {
                                        "item": [{"flonum": 5.0}, {"b": False}],
                                    }
                                },
                            }
                        },
                        {
                            "pair": {
                                "car": {"str": "b"},
                                "cdr": {
                                    "list": {
                                        "item": [{"flonum": 10.0}, {"b": True}],
                                    }
                                },
                            }
                        },
                    ]
                }
            },
        ),
        (
            [["a", 5.0, False], [5, 10.0, True]],
            {
                "list": {
                    "item": [
                        {
                            "list": {
                                "item": [{"str": "a"}, {"flonum": 5.0}, {"b": False}],
                            }
                        },
                        {
                            "list": {
                                "item": [
                                    {"fixednum": 5},
                                    {"flonum": 10.0},
                                    {"b": True},
                                ],
                            }
                        },
                    ]
                }
            },
        ),
    ],
)
def test_convert_scheme_pointer_to_py_value(
    py_value: Any, json_dict: Dict[str, Any]
) -> None:
    p = SchemePointer()
    ParseDict(json_dict, p)
    val = _convert_scheme_pointer_to_py_value(p, "23.1.0")
    assert val == py_value


def test_convert_scheme_pointer_having_symbol_to_py_value() -> None:
    p = SchemePointer()
    ParseDict(
        {
            "pair": {
                "car": {"str": "abc"},
                "cdr": {"flonum": 5.0},
            }
        },
        p,
    )
    val = _convert_scheme_pointer_to_py_value(p, "23.1.0")
    assert isinstance(val, tuple)
    assert len(val) == 2
    assert val[0] == "abc"
    assert val[1] == 5.0


@pytest.mark.parametrize(
    "py_value",
    [
        None,
        False,
        True,
        5,
        5.0,
        "abc",
        ["abc"],
        [False, 5.0, "abc"],
        {"abc": 5.0},
        {"abc": 5.0, "def": [2.0, False]},
        {"a": {"b": 3.0}},
        {"a": {"b": {"c": 3.0}}},
        {"a": {"b": {"c": 3.0}, "d": 4.0}},
    ],
)
def test_two_way_conversion(py_value: Any) -> None:
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p, "23.1.0")
    val = _convert_scheme_pointer_to_py_value(p, "23.1.0")
    assert val == py_value


def test_two_way_conversion_for_symbol() -> None:
    py_value = [Symbol("+"), 2.0, 3.0]
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p, "23.1.0")
    val = _convert_scheme_pointer_to_py_value(p, "23.1.0")
    assert isinstance(val, list)
    assert isinstance(val[0], Symbol)
    assert val[0].str == "+"
    assert val[1:] == [2.0, 3.0]


def test_two_way_conversion_for_pairs() -> None:
    py_value = ("abc", 5.0)
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p, "23.1.0")
    val = _convert_scheme_pointer_to_py_value(p, "23.1.0")
    assert isinstance(val, tuple)
    assert len(val) == 2
    assert val[0] == "abc"
    assert val[1] == 5.0


@pytest.mark.dev
@pytest.mark.fluent_231
def test_long_list(new_solver_session) -> None:
    length = 10**6
    assert new_solver_session.scheme_eval.eval(
        [Symbol("+")] + list(range(length))
    ) == sum(range(length))
    assert sum(new_solver_session.scheme_eval.eval([Symbol("range"), length])) == sum(
        range(length)
    )
