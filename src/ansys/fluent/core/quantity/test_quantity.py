import math

import pytest
import quantity as q

DELTA = 1.0e-5


def test_properties_1():
    v = q.Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.unit_str == "m"
    assert v.si_value == 10.6
    assert v.si_unit_str == "m"
    assert v.type == "Length"


def test_properties_2():
    v = q.Quantity(1, "ft s^-1")
    assert v.value == 1
    assert v.unit_str == "ft s^-1"
    assert v.si_value == pytest.approx(0.30479999, DELTA)
    assert v.si_unit_str == "m s^-1.0"
    assert v.type == "Composite"


def test_properties_3():
    v = q.Quantity(1.0, "farad")
    assert v.value == 1.0
    assert v.unit_str == "farad"
    assert v.si_value == 1.0
    assert v.si_unit_str == "kg^-1.0 m^-2.0 s^4.0 A^2.0"
    assert v.type == "Derived"


def test_dimensions_4():
    v = q.Quantity(1.0, "ft")
    assert v.dimensions == [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_dimensions_5():
    v = q.Quantity(1.0, "kPa")
    assert v.dimensions == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_dimensions_6():
    v = q.Quantity(1.0, "slug ft s R radian slugmol cd A sr")
    assert v.dimensions == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_to_7():
    v = q.Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.unit_str == "ft"


def test_to_8():
    v = q.Quantity(1.0, "m")
    to = v.to("mm")
    assert to.value == 1000
    assert to.unit_str == "mm"


# def test_to_10():
#     v = q.Quantity(100000.0, "Pa")
#     to = v.to("kPa")
#     assert to.value == 100.0
#     assert to.unit_str == "kPa"


def test_to_11():
    v = q.Quantity(1.0, "dm^3")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.unit_str == "m^3"


def test_to_12():
    v = q.Quantity(1.0, "radian")
    to = v.to("degree")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.unit_str == "degree"


def test_to_13():
    v = q.Quantity(1.0, "degree")
    to = v.to("radian")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.unit_str == "radian"


def test_to_14():
    v = q.Quantity(1.0, "Pa s")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.unit_str == "dyne cm^-2 s"


def test_to_15():
    v = q.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.unit_str == "dyne cm^-2 s"


def test_to_16():
    v = q.Quantity(1.0, "Pa s")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.unit_str == "slug in^-1 s^-1"


def test_to_17():
    v = q.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.unit_str == "slug in^-1 s^-1"


def test_to_18():
    v = q.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("Pa s")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.unit_str == "Pa s"


def test_to_19():
    v = q.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("kg m^-1 s^-1")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.unit_str == "kg m^-1 s^-1"


def test_to_20():
    v = q.Quantity(1.0, "Hz")
    with pytest.raises(q.QuantityError) as e:
        to = v.to("radian s^-1")
    assert e.value.from_unit == "Hz"
    assert e.value.to_unit == "radian s^-1"


def test_to_21():
    v = q.Quantity(1.0, "radian s^-1")
    with pytest.raises(q.QuantityError) as e:
        to = v.to("Hz")
    assert e.value.from_unit == "radian s^-1"
    assert e.value.to_unit == "Hz"


def test_to_22():
    v = q.Quantity(1.0, "lbf ft^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(47.88024159, DELTA)
    assert to.unit_str == "N m^-2"


def test_to_23():
    v = q.Quantity(1.0, "ft^-3 s^-1")
    to = v.to("m^-3 s^-1")
    assert to.value == pytest.approx(35.3146667, DELTA)
    assert to.unit_str == "m^-3 s^-1"


def test_to_24():
    v = q.Quantity(1.0, "m^-2")
    to = v.to("cm^-2")
    assert to.value == pytest.approx(0.0001, DELTA)
    assert to.unit_str == "cm^-2"


def test_to_25():
    v = q.Quantity(1.0, "m^2")
    to = v.to("in^2")
    assert to.value == pytest.approx(1550.0031, DELTA)
    assert to.unit_str == "in^2"


def test_to_26():
    v = q.Quantity(1.0, "radian s^-1")
    to = v.to("degree s^-1")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.unit_str == "degree s^-1"


def test_to_27():
    v = q.Quantity(1.0, "degree s^-1")
    to = v.to("radian s^-1")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.unit_str == "radian s^-1"


def test_to_28():
    v = q.Quantity(1.0, "dyne cm^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(0.1, DELTA)
    assert to.unit_str == "N m^-2"


def test_to_29():
    v = q.Quantity(1.0, "psi")
    to = v.to("Pa")
    assert to.value == pytest.approx(6894.76, DELTA)
    assert to.unit_str == "Pa"


def test_to_30():
    v = q.Quantity(1.0, "pdl")
    to = v.to("N")
    assert to.value == pytest.approx(0.138254999, DELTA)
    assert to.unit_str == "N"


def test_to_31():
    v = q.Quantity(1.0, "ohm cm")
    to = v.to("ohm m")
    assert to.value == pytest.approx(0.01, DELTA)
    assert to.unit_str == "ohm m"


def test_to_32():
    v = q.Quantity(1.0, "erg")
    to = v.to("J")
    assert to.value == pytest.approx(1.0e-7, DELTA)
    assert to.unit_str == "J"


def test_to_33():
    v = q.Quantity(1.0, "BTU")
    to = v.to("J")
    assert to.value == pytest.approx(1055.056, DELTA)
    assert to.unit_str == "J"


def test_to_34():
    v = q.Quantity(1.0, "gal")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.00378541, DELTA)
    assert to.unit_str == "m^3"


def test_to_35():
    v = q.Quantity(1.0, "l")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.unit_str == "m^3"


# def test_to_36():
#     v = q.Quantity(1.0, "BTU lb^-1 R^-1")
#     to = v.to("J kg^-1 K^-1")
#     assert to.value == pytest.approx(4186.8161854, DELTA)
#     assert to.unit_str == "J kg^-1 K^-1"


# def test_to_37():
#     v = q.Quantity(1.0, "BTU lb^-1 F^-1")
#     to = v.to("J kg^-1 K^-1")
#     assert to.value == pytest.approx(4186.8161854, DELTA)
#     assert to.unit_str == "J kg^-1 K^-1"


# def test_to_38():
#     v = q.Quantity(1.0, "gal^-1")
#     to = v.to("m^-3")
#     assert to.value == pytest.approx(264.172, DELTA)
#     assert to.unit_str == "m^-3"


def test_to_39():
    v = q.Quantity(1.0, "BTU ft^-2")
    to = v.to("J m^-2")
    assert to.value == pytest.approx(11356.5713242, DELTA)
    assert to.unit_str == "J m^-2"


def test_convert_40():
    v = q.Quantity(2.0, "ft^-2")
    convert = v.convert("SI")
    assert convert.value == 2.0
    assert convert.unit_str == "m^-2.0"


def test_convert_41():
    v = q.Quantity(1.0, "mm^3")
    convert = v.convert("CGS")
    assert convert.value == 1.0
    assert convert.unit_str == "cm^3.0"


def test_convert_42():
    v = q.Quantity(7.0, "K mol")
    convert = v.convert("BT")
    assert convert.value == 7.0
    assert convert.unit_str == "R slugmol"


def test_math_43():
    deg = q.Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = q.Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    # root = q.Quantity(100.0, "")
    # assert math.sqrt(root) == 10.0


deg = q.Quantity(90, "degree")
print(type(deg))
print(deg, deg == 90)


def test_subtraction_44():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    assert float(q1 - q2) == 5.0
    assert float(q2 - q1) == -5.0
    assert float(q1) - 2.0 == 8.0
    assert 2.0 - float(q1) == -8.0
    assert float(q1) - 3 == 7.0
    assert 3 - float(q1) == -7.0


def test_pow_45():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    q1_sq = q1**2
    assert q1_sq.unit == "m^2 s^-2"

    assert float(q1) ** 2 == 100.0
    assert float(q2) ** 2 == 25.0


def test_eq_46():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")
    q3 = q.Quantity(10.0, "m s^-1")
    q4 = q.Quantity(10.0, "")

    assert q1 != q2
    assert q1 == q3
    assert float(q1) == 10.0
    assert q4 == 10.0


def test_rdiv_47():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    assert float(q1) / float(q2) == 2.0
    assert float(q2) / float(q1) == 0.5
    assert float(q1) / 2 == 5.0
    assert 2.0 / float(q1) == 0.2


# def test_units_table_x():
#     pass

# def test_dimensions_x():
#     pass

# def test_quantity_map():
#     pass
