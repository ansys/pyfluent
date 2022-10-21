import pytest

import ansys.fluent.core.quantity as q

DELTA = 1.0e-5


def test_value_unit_1():
    v = q.Quantity(1, "m s^-1")
    assert v.value == 1
    assert v.unit == "m s^-1"


def test_value_unit_2():
    v = q.Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.unit == "m"


def test_value_unit_3():
    v = q.Quantity(99.85, "radian")
    assert v.value == pytest.approx(99.85, DELTA)
    assert v.unit == "radian"


def test_value_unit_4():
    v = q.Quantity(5.7, "")
    assert v.value == pytest.approx(5.7, DELTA)
    assert v.unit == ""
