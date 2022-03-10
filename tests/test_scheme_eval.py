import pytest
from google.protobuf.json_format import MessageToDict, ParseDict

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
        (("abc",), {"pair": {"car": {"str": "abc"}}}),
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
            {
                "pair": {
                    "car": {"b": False},
                    "cdr": {
                        "pair": {
                            "car": {"flonum": 5.0},
                            "cdr": {"pair": {"car": {"str": "abc"}}},
                        }
                    },
                }
            },
        ),
        ([], {}),
        (["abc"], {"pair": {"car": {"str": "abc"}}}),
        (
            [False, 5.0, "abc"],
            {
                "pair": {
                    "car": {"b": False},
                    "cdr": {
                        "pair": {
                            "car": {"flonum": 5.0},
                            "cdr": {"pair": {"car": {"str": "abc"}}},
                        }
                    },
                }
            },
        ),
        ({}, {}),
        (
            {"a": 5.0},
            {
                "pair": {
                    "car": {
                        "pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}
                    },
                }
            },
        ),
        (
            {"a": 5.0, "b": 10.0},
            {
                "pair": {
                    "car": {
                        "pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}
                    },
                    "cdr": {
                        "pair": {
                            "car": {
                                "pair": {
                                    "car": {"str": "b"},
                                    "cdr": {"flonum": 10.0},
                                }
                            }
                        }
                    },
                }
            },
        ),
        (
            [Symbol("+"), 2.0, 3.0],
            {
                "pair": {
                    "car": {"sym": "+"},
                    "cdr": {
                        "pair": {
                            "car": {"flonum": 2.0},
                            "cdr": {"pair": {"car": {"flonum": 3.0}}},
                        }
                    },
                }
            },
        ),
    ],
)
def test_convert_py_value_to_scheme_pointer(py_value, json_dict):
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p)
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
        (["abc"], {"pair": {"car": {"str": "abc"}}}),
        (
            [False, 5.0, "abc"],
            {
                "pair": {
                    "car": {"b": False},
                    "cdr": {
                        "pair": {
                            "car": {"flonum": 5.0},
                            "cdr": {"pair": {"car": {"str": "abc"}}},
                        }
                    },
                }
            },
        ),
        (None, {}),
        (
            {"a": 5.0, "b": 10.0},
            {
                "pair": {
                    "car": {
                        "pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}
                    },
                    "cdr": {
                        "pair": {
                            "car": {
                                "pair": {
                                    "car": {"str": "b"},
                                    "cdr": {"flonum": 10.0},
                                }
                            }
                        }
                    },
                }
            },
        ),
        (
            [("a", 5.0), (5, 10.0)],
            {
                "pair": {
                    "car": {
                        "pair": {"car": {"str": "a"}, "cdr": {"flonum": 5.0}}
                    },
                    "cdr": {
                        "pair": {
                            "car": {
                                "pair": {
                                    "car": {"fixednum": "5"},
                                    "cdr": {"flonum": 10.0},
                                }
                            }
                        }
                    },
                }
            },
        ),
        (
            {"a": [5.0, False], "b": [10.0, True]},
            {
                "pair": {
                    "car": {
                        "pair": {
                            "car": {"str": "a"},
                            "cdr": {
                                "pair": {
                                    "car": {"flonum": 5.0},
                                    "cdr": {"pair": {"car": {"b": False}}},
                                }
                            },
                        }
                    },
                    "cdr": {
                        "pair": {
                            "car": {
                                "pair": {
                                    "car": {"str": "b"},
                                    "cdr": {
                                        "pair": {
                                            "car": {"flonum": 10.0},
                                            "cdr": {
                                                "pair": {"car": {"b": True}}
                                            },
                                        }
                                    },
                                }
                            }
                        }
                    },
                }
            },
        ),
        (
            [["a", 5.0, False], [5, 10.0, True]],
            {
                "pair": {
                    "car": {
                        "pair": {
                            "car": {"str": "a"},
                            "cdr": {
                                "pair": {
                                    "car": {"flonum": 5.0},
                                    "cdr": {"pair": {"car": {"b": False}}},
                                }
                            },
                        }
                    },
                    "cdr": {
                        "pair": {
                            "car": {
                                "pair": {
                                    "car": {"fixednum": "5"},
                                    "cdr": {
                                        "pair": {
                                            "car": {"flonum": 10.0},
                                            "cdr": {
                                                "pair": {"car": {"b": True}}
                                            },
                                        }
                                    },
                                }
                            }
                        }
                    },
                }
            },
        ),
    ],
)
def test_convert_scheme_pointer_to_py_value(py_value, json_dict):
    p = SchemePointer()
    ParseDict(json_dict, p)
    val = _convert_scheme_pointer_to_py_value(p)
    assert val == py_value


def test_convert_scheme_pointer_having_symbol_to_py_value():
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
    val = _convert_scheme_pointer_to_py_value(p)
    assert isinstance(val, tuple)
    assert len(val) == 2
    assert val[0] == "abc"
    assert val[1] == 5.0


def test_convert_scheme_pointer_having_pair_to_py_value():
    p = SchemePointer()
    ParseDict(
        {
            "pair": {
                "car": {"sym": "+"},
                "cdr": {
                    "pair": {
                        "car": {"flonum": 2.0},
                        "cdr": {"pair": {"car": {"flonum": 3.0}}},
                    }
                },
            }
        },
        p,
    )
    val = _convert_scheme_pointer_to_py_value(p)
    assert isinstance(val, list)
    assert isinstance(val[0], Symbol)
    assert val[0].str == "+"
    assert val[1:] == [2.0, 3.0]


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
def test_two_way_conversion(py_value):
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p)
    val = _convert_scheme_pointer_to_py_value(p)
    assert val == py_value


def test_two_way_conversion_for_symbol():
    py_value = [Symbol("+"), 2.0, 3.0]
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p)
    val = _convert_scheme_pointer_to_py_value(p)
    assert isinstance(val, list)
    assert isinstance(val[0], Symbol)
    assert val[0].str == "+"
    assert val[1:] == [2.0, 3.0]


def test_two_way_conversion_for_pairs():
    py_value = ("abc", 5.0)
    p = SchemePointer()
    _convert_py_value_to_scheme_pointer(py_value, p)
    val = _convert_scheme_pointer_to_py_value(p)
    assert isinstance(val, tuple)
    assert len(val) == 2
    assert val[0] == "abc"
    assert val[1] == 5.0
