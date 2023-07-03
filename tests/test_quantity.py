import math

import pytest

import ansys.fluent.core.quantity as q

DELTA = 1.0e-5


def test_properties_1():
    v = q.Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.units == "m"
    assert v.si_value == 10.6
    assert v.si_units == "m"
    assert v.type == "Length"


def test_properties_2():
    v = q.Quantity(1, "ft s^-1")
    assert v.value == 1
    assert v.units == "ft s^-1"
    assert v.si_value == pytest.approx(0.30479999, DELTA)
    assert v.si_units == "m s^-1.0"
    assert v.type == "Composite"


def test_properties_3():
    v = q.Quantity(1.0, "farad")
    assert v.value == 1.0
    assert v.units == "farad"
    assert v.si_value == 1.0
    assert v.si_units == "kg^-1.0 m^-2.0 s^4.0 A^2.0"
    assert v.type == "Derived"


def test_dimensions_1():
    v = q.Quantity(1.0, "ft")
    assert v.dimensions == [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_dimensions_2():
    v = q.Quantity(1.0, "kPa")
    assert v.dimensions == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_dimensions_3():
    v = q.Quantity(1.0, "slug ft s R radian slugmol cd A sr")
    assert v.dimensions == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_to_1():
    v = q.Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.units == "ft"


def test_to_2():
    v = q.Quantity(1.0, "m")
    to = v.to("mm")
    assert to.value == 1000
    assert to.units == "mm"


def test_to_3():
    v = q.Quantity(100000.0, "Pa")
    to = v.to("kPa")
    assert to.value == 100.0
    assert to.units == "kPa"


def test_to_4():
    v = q.Quantity(1.0, "dm^3")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.units == "m^3"


def test_to_5():
    v = q.Quantity(1.0, "radian")
    to = v.to("degree")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.units == "degree"


def test_to_6():
    v = q.Quantity(1.0, "degree")
    to = v.to("radian")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.units == "radian"


def test_to_7():
    v = q.Quantity(1.0, "Pa s")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.units == "dyne cm^-2 s"


def test_to_8():
    v = q.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.units == "dyne cm^-2 s"


def test_to_9():
    v = q.Quantity(1.0, "Pa s")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.units == "slug in^-1 s^-1"


def test_to_10():
    v = q.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.units == "slug in^-1 s^-1"


def test_to_11():
    v = q.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("Pa s")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.units == "Pa s"


def test_to_12():
    v = q.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("kg m^-1 s^-1")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.units == "kg m^-1 s^-1"


def test_to_13():
    v = q.Quantity(1.0, "Hz")
    with pytest.raises(q.QuantityError) as e:
        to = v.to("radian s^-1")


def test_to_14():
    v = q.Quantity(1.0, "radian s^-1")
    with pytest.raises(q.QuantityError) as e:
        to = v.to("Hz")


def test_to_15():
    v = q.Quantity(1.0, "lbf ft^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(47.88024159, DELTA)
    assert to.units == "N m^-2"


def test_to_16():
    v = q.Quantity(1.0, "ft^-3 s^-1")
    to = v.to("m^-3 s^-1")
    assert to.value == pytest.approx(35.3146667, DELTA)
    assert to.units == "m^-3 s^-1"


def test_to_17():
    v = q.Quantity(1.0, "m^-2")
    to = v.to("cm^-2")
    assert to.value == pytest.approx(0.0001, DELTA)
    assert to.units == "cm^-2"


def test_to_18():
    v = q.Quantity(1.0, "m^2")
    to = v.to("in^2")
    assert to.value == pytest.approx(1550.0031, DELTA)
    assert to.units == "in^2"


def test_to_19():
    v = q.Quantity(1.0, "radian s^-1")
    to = v.to("degree s^-1")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.units == "degree s^-1"


def test_to_20():
    v = q.Quantity(1.0, "degree s^-1")
    to = v.to("radian s^-1")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.units == "radian s^-1"


def test_to_21():
    v = q.Quantity(1.0, "dyne cm^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(0.1, DELTA)
    assert to.units == "N m^-2"


def test_to_22():
    v = q.Quantity(1.0, "psi")
    to = v.to("Pa")
    assert to.value == pytest.approx(6894.76, DELTA)
    assert to.units == "Pa"


def test_to_23():
    v = q.Quantity(1.0, "pdl")
    to = v.to("N")
    assert to.value == pytest.approx(0.138254999, DELTA)
    assert to.units == "N"


def test_to_24():
    v = q.Quantity(1.0, "ohm cm")
    to = v.to("ohm m")
    assert to.value == pytest.approx(0.01, DELTA)
    assert to.units == "ohm m"


def test_to_25():
    v = q.Quantity(1.0, "erg")
    to = v.to("J")
    assert to.value == pytest.approx(1.0e-7, DELTA)
    assert to.units == "J"


def test_to_26():
    v = q.Quantity(1.0, "BTU")
    to = v.to("J")
    assert to.value == pytest.approx(1055.056, DELTA)
    assert to.units == "J"


def test_to_27():
    v = q.Quantity(1.0, "gal")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.00378541, DELTA)
    assert to.units == "m^3"


def test_to_28():
    v = q.Quantity(1.0, "l")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.units == "m^3"


def test_to_29():
    v = q.Quantity(1.0, "BTU lb^-1 R^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.units == "J kg^-1 K^-1"


def test_to_30():
    v = q.Quantity(1.0, "BTU lb^-1 F^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.units == "J kg^-1 K^-1"


def test_to_31():
    v = q.Quantity(1.0, "gal^-1")
    to = v.to("m^-3")
    assert to.value == pytest.approx(264.172, DELTA)
    assert to.units == "m^-3"


def test_to_32():
    v = q.Quantity(1.0, "BTU ft^-2")
    to = v.to("J m^-2")
    assert to.value == pytest.approx(11356.5713242, DELTA)
    assert to.units == "J m^-2"


def test_to_33():
    v = q.Quantity(2.0, "radian")
    with pytest.raises(TypeError) as e:
        convert = v.to(0)


def test_convert_1():
    newSys = q.UnitSystem(unit_sys="SI")
    v = q.Quantity(2.0, "ft^-2")
    convert = newSys.convert(v)
    assert convert.value == 2.0
    assert convert.units == "m^-2.0"


def test_convert_2():
    newSys = q.UnitSystem(unit_sys="CGS")
    v = q.Quantity(1.0, "mm^3")
    convert = newSys.convert(v)
    assert convert.value == 1.0
    assert convert.units == "cm^3.0"


def test_convert_3():
    newSys = q.UnitSystem(unit_sys="BT")
    v = q.Quantity(7.0, "K mol")
    convert = newSys.convert(v)
    assert convert.value == 7.0
    assert convert.units == "R slugmol"


def test_convert_4():
    v = q.Quantity(7.0, "K mol")
    with pytest.raises(ValueError) as e:
        newSys = q.UnitSystem(unit_sys="")
        newSys.convert(v)


def test_repr():
    v = q.Quantity(1.0, "m")
    assert v.__repr__() == 'Quantity (1.0, "m")'


def test_math():
    deg = q.Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = q.Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    root = q.Quantity(100.0, "")
    assert math.sqrt(root) == 10.0


def test_subtraction():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    assert float(q1 - q2) == 5.0
    assert float(q2 - q1) == -5.0
    assert float(q1) - 2.0 == 8.0
    assert 2.0 - float(q1) == -8.0
    assert float(q1) - 3 == 7.0
    assert 3 - float(q1) == -7.0


def test_pow():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    q1_sq = q1**2
    assert q1_sq.units == "m^2.0 s^-2.0"

    assert float(q1) ** 2 == 100.0
    assert float(q2) ** 2 == 25.0


def test_neg():
    q0 = q.Quantity(10.0, "m s^-1")
    q1 = -q0
    assert q1.value == -10.0


def test_neq():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y != x
    assert x != y

    assert r != 0.5
    assert 0.5 != r


def test_eq_1():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")
    q3 = q.Quantity(10.0, "m s^-1")
    q4 = q.Quantity(10.0, "")

    assert q1 != q2
    assert q1 == q3
    assert float(q1) == 10.0
    assert q4 == 10.0


def test_eq_2():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    l = q.Quantity(10.5, "cm")
    m = q.Quantity(10.5, "m")
    n = q.Quantity(10.5, "")

    assert x == l
    assert y == m
    assert r == n

    with pytest.raises(q.QuantityError) as e_info:
        assert z == x
        assert y == x
        assert r == 0.5
        assert 5.0 == x


def test_rdiv():
    q1 = q.Quantity(10.0, "m s^-1")
    q2 = q.Quantity(5.0, "m s^-1")

    assert float(q1) / float(q2) == 2.0
    assert float(q2) / float(q1) == 0.5
    assert float(q1) / 2 == 5.0
    assert 2.0 / float(q1) == 0.2


def test_power():
    qt = q.Quantity(5.0, "m^0")
    qtm = qt * 2

    assert qtm.value == 10.0
    assert qtm.units == ""


def test_ge():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y >= x
    assert 15.7 >= r
    assert r >= 7.8

    with pytest.raises(q.QuantityError) as e_info:
        assert x >= z
        assert x >= y
        assert 5.0 >= r
        assert x >= 5.0


def test_gt():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y > x
    assert 15.7 > r
    assert r > 7.8

    with pytest.raises(q.QuantityError) as e_info:
        assert x > z
        assert x > y
        assert 5.0 > r
        assert x > 5.0


def test_lt():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert x < y
    assert r < 15.7
    assert 7.8 < r

    with pytest.raises(q.QuantityError) as e_info:
        assert z < x
        assert y < x
        assert r < 0.5
        assert 5.0 < x


def test_le():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert x <= y
    assert r <= 15.7
    assert 7.8 <= r

    with pytest.raises(q.QuantityError) as e_info:
        assert z <= x
        assert y <= x
        assert r <= 0.5
        assert 5.0 <= x


def test_errors():
    e1 = q.QuantityError.EXCESSIVE_PARAMETERS()
    assert (
        e1.__str__()
        == "Quantity only accepts 1 of the following parameters: (units) or (quantity_map) or (dimensions)."
    )

    e2 = q.QuantityError.INCOMPATIBLE_DIMENSIONS("mm", "K")
    assert e2.__str__() == "`mm` and `K` have incompatible dimensions."

    e3 = q.QuantityError.INCOMPATIBLE_VALUE("radian")
    assert e3.__str__() == "`radian` is incompatible with the current quantity object."

    e4 = q.UnitSystemError.EXCESSIVE_PARAMETERS()
    assert (
        e4.__str__()
        == "UnitSystem only accepts 1 of the following parameters: (name, base_units) or (unit_sys)."
    )

    e5 = q.UnitSystemError.BASE_UNITS_LENGTH(10)
    assert (
        e5.__str__()
        == "The `base_units` argument must contain 9 units, currently there are 10."
    )

    e6 = q.UnitSystemError.UNIT_UNDEFINED("pizza")
    assert (
        e6.__str__()
        == "`pizza` is an undefined unit. To use `pizza` add it to the `fundamental_units` table within quantity_config.yaml."
    )

    e7 = q.UnitSystemError.UNIT_ORDER("Mass", 1, "Light", 7)
    assert (
        e7.__str__()
        == "Expected unit of type: `Mass` (order: 1), received unit of type: `Light` (order: 7)."
    )

    e8 = q.UnitSystemError.INVALID_UNIT_SYS("ham sandwich")
    assert e8.__str__() == "`ham sandwich` is not a supported unit system."

    e9 = q.DimensionsError.EXCESSIVE_PARAMETERS()
    assert (
        e9.__str__()
        == "Dimensions only accepts 1 of the following parameters: (units) or (dimensions)."
    )

    e10 = q.DimensionsError.EXCESSIVE_DIMENSIONS(200)
    assert (
        e10.__str__()
        == "The `dimensions` argument must contain 9 values or less, currently there are 200."
    )

    e11 = q.QuantityMapError.UNKNOWN_MAP_ITEM("Risk")
    assert e11.__str__() == "`Risk` is not a valid quantity map item."


def test_temp_1():
    k = q.Quantity(-40, "K")

    kc = k.to("C")
    assert kc.value == -313.15
    assert kc.units == "C"

    kc = k.to("R")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == "R"

    kc = k.to("F")
    assert kc.value == pytest.approx(-531.67, DELTA)
    assert kc.units == "F"


def test_temp_2():
    mk = q.Quantity(-40000.0, "mK")
    uc = mk.to("uC^1")
    assert uc.value == -40000000.0


def test_temp_3():
    k = q.Quantity(1.0, "K")

    f = k.to("F")
    r = k.to("R")
    c = k.to("C")

    assert f.value == pytest.approx(-457.87, DELTA)
    assert r.value == pytest.approx(1.8, DELTA)
    assert c.value == pytest.approx(-272.15, DELTA)


def test_temp_4():
    c = q.Quantity(1.0, "C")

    f = c.to("F")
    r = c.to("R")
    k = c.to("K")

    assert f.value == pytest.approx(33.80, DELTA)
    assert r.value == pytest.approx(493.469, DELTA)
    assert k.value == 274.15


def test_temp_5():
    r = q.Quantity(1.0, "R")

    f = r.to("F")
    c = r.to("C")
    k = r.to("K")

    assert f.value == pytest.approx(-458.6699, DELTA)
    assert c.value == pytest.approx(-272.5944, DELTA)
    assert k.value == pytest.approx(0.555556, DELTA)


def test_temp_6():
    f = q.Quantity(1.0, "F")

    c = f.to("C")
    r = f.to("R")
    k = f.to("K")

    assert c.value == pytest.approx(-17.2222, DELTA)
    assert r.value == pytest.approx(460.670, DELTA)
    assert k.value == pytest.approx(255.927, DELTA)


def test_temp_7():
    hc = q.Quantity(1.0, "J g^-1 K^-1")

    hcto1 = hc.to("kJ kg^-1 K^-1")

    assert hcto1.value == pytest.approx(1.0, DELTA)
    assert hcto1.units == "kJ kg^-1 K^-1"

    hcto2 = hc.to("J kg^-1 C^-1")

    assert hcto2.value == pytest.approx(1000.0, DELTA)
    assert hcto2.units == "J kg^-1 C^-1"

    hcto3 = hc.to("kJ kg^-1 C^-1")

    assert hcto3.value == pytest.approx(1.0, DELTA)
    assert hcto3.units == "kJ kg^-1 C^-1"

    hcto4 = hc.to("cal g^-1 C^-1")

    assert hcto4.value == pytest.approx(0.2390057, DELTA)
    assert hcto4.units == "cal g^-1 C^-1"

    hcto5 = hc.to("cal kg^-1 C^-1")

    assert hcto5.value == pytest.approx(239.0057, DELTA)
    assert hcto5.units == "cal kg^-1 C^-1"

    hcto6 = hc.to("kcal kg^-1 C^-1")

    assert hcto6.value == pytest.approx(0.2390057, DELTA)
    assert hcto6.units == "kcal kg^-1 C^-1"

    hcto7 = hc.to("BTU lb^-1 F^-1")

    assert hcto7.value == pytest.approx(0.238845, DELTA)
    assert hcto7.units == "BTU lb^-1 F^-1"


def test_temp_8():
    temp_var = q.Quantity(1.0, "kg m^-3 s^-1 K^2")

    temp_varto1 = temp_var.to("g cm^-3 s^-1 K^2")

    assert temp_varto1.value == pytest.approx(0.001, DELTA)
    assert temp_varto1.units == "g cm^-3 s^-1 K^2"

    temp_varto2 = temp_var.to("kg mm^-3 s^-1 K^2")

    assert temp_varto2.value == pytest.approx(1e-09, DELTA)
    assert temp_varto2.units == "kg mm^-3 s^-1 K^2"

    temp_varto3 = temp_var.to("kg um^-3 s^-1 K^2")

    assert temp_varto3.value == pytest.approx(9.999999999999999e-19, DELTA)
    assert temp_varto3.units == "kg um^-3 s^-1 K^2"

    temp_varto4 = temp_var.to("mg mm^-3 ms^-1 K^2")

    assert temp_varto4.value == pytest.approx(1.0000000000000002e-06, DELTA)
    assert temp_varto4.units == "mg mm^-3 ms^-1 K^2"

    temp_varto5 = temp_var.to("g cm^-3 us^-1 K^2")

    assert temp_varto5.value == pytest.approx(1e-09, DELTA)
    assert temp_varto5.units == "g cm^-3 us^-1 K^2"

    temp_varto6 = temp_var.to("pg um^-3 ms^-1 K^2")

    assert temp_varto6.value == pytest.approx(9.999999999999997e-07, DELTA)
    assert temp_varto6.units == "pg um^-3 ms^-1 K^2"


def test_temp_inverse_1():
    c = q.Quantity(2.0, "C")
    assert float(c) == 275.15

    c_inverse = q.Quantity(2.0, "C^-1")
    assert float(c_inverse) == 2.0


def test_temp_inverse_2():
    f = q.Quantity(2.0, "F")
    assert float(f) == pytest.approx(256.483311, DELTA)

    f_inverse = q.Quantity(2.0, "F^-1")
    assert float(f_inverse) == pytest.approx(3.5999999999999996, DELTA)


def test_temp_type():
    c0 = q.Quantity(1.0, "C")
    assert c0.type == "Temperature"

    c1 = q.Quantity(1.0, "J kg^-1 C^-1")
    assert c1.type == "Temperature Difference"

    c2 = q.Quantity(1.0, "kg m^-3 s^-1 K^2")
    assert c2.type == "Temperature Difference"

    c4 = q.Quantity(1.0, "F")
    assert c4.type == "Temperature"

    c6 = q.Quantity(1.0, "F^1")
    assert c6.type == "Temperature Difference"

    c7 = q.Quantity(1.0, "F^-1")
    assert c7.type == "Temperature Difference"

    c8 = q.Quantity(1.0, "F^2")
    assert c8.type == "Temperature Difference"


def test_temp_difference():
    td1 = q.Quantity(150.0, "delta_C")
    assert td1.type == "Temperature Difference"

    td2 = q.Quantity(100.0, "delta_C")
    assert td2.type == "Temperature Difference"

    td = td1 - td2
    assert td.type == "Temperature Difference"

    td_m = td * 2
    assert td_m.units == "delta_K"
    assert td_m.type == "Temperature Difference"

    t1 = q.Quantity(150.0, "C")
    assert t1.type == "Temperature"

    t2 = q.Quantity(100.0, "C")
    assert t2.type == "Temperature"

    td = t1 - t2
    assert td.type == "Temperature Difference"

    td2 = t2 - t1
    assert td2.type == "Temperature Difference"

    tc1 = q.Quantity(100.0, "C")
    td1 = q.Quantity(50.0, "C^-1")

    with pytest.raises(ValueError) as e:
        t = tc1 + td1


def test_core_temp():
    t1 = q.Quantity(1.0, "K")
    assert float(t1) == 1.0
    assert t1.type == "Temperature"

    t2 = q.Quantity(2.0, "K")
    assert float(t2) == 2.0
    assert t2.type == "Temperature"

    dt1 = t2 - t1
    assert float(dt1) == 1.0
    assert dt1.type == "Temperature Difference"

    t3 = q.Quantity(1.0, "C")
    assert float(t3) == 274.15
    assert t3.type == "Temperature"

    t4 = q.Quantity(2.0, "C")
    assert float(t4) == 275.15
    assert t4.type == "Temperature"

    dt2 = t4 - t3
    assert float(dt2) == 1.0
    assert dt2.type == "Temperature Difference"

    invt1 = q.Quantity(1.0, "K^-1")
    assert float(invt1) == 1.0
    assert invt1.type == "Temperature Difference"

    dt3 = 1.0 / invt1
    assert float(dt3) == 1.0
    assert dt1.type == dt2.type == dt3.type

    invt2 = q.Quantity(1.0, "C^-1")
    assert float(invt2) == 1.0
    assert invt2.type == "Temperature Difference"

    dt4 = 1.0 / invt2
    assert float(dt4) == 1.0
    assert dt4.type == "Temperature Difference"


def test_temp_addition():
    t1 = q.Quantity(150.0, "C")
    t2 = q.Quantity(50.0, "C")

    td = t1 - t2
    assert td.type == "Temperature Difference"
    assert float(td) == 100.0
    assert td.units == "delta_K"

    kd = q.Quantity(50.0, "delta_C")
    k = q.Quantity(50.0, "K")

    t = k + kd
    assert float(t) == 100.0
    assert t.type == "Temperature Difference"


def test_quantity_map_1():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }

    api_test = q.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == "kg^3.0 m^-1.5 s^-6.5 A^3.0 cd"


def test_quantity_map_2():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 2,
        "Epsilon Flux Coefficient": 2,
    }

    with pytest.raises(ValueError):
        api_test = q.Quantity(
            10.5, units="kg m s^-1", quantity_map=quantity_map_from_settings_API
        )


def test_quantity_map_3():
    quantity_map_from_settings_API = {
        "Temperature": 1,
        "Pressure": 1,
        "Volume": 1,
    }

    api_test = q.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == "K Pa m^3.0"


def test_unit_from_dimensions_1():
    p = q.Quantity(10.5, dimensions=[1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert p.units == "kg m^-1.0 s^-2.0"


def test_unit_from_dimensions_2():
    l = q.Quantity(10.5, dimensions=[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert l.units == "m"


def test_unit_from_dimensions_3():
    x = q.Quantity(10.5, dimensions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert x.units == ""


def test_unit_from_dimensions_4():
    test = q.Quantity(10.5, dimensions=[0, 1, -1])
    assert test.units == "m s^-1.0"
    assert test.dimensions == [0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_unit_from_dimensions_5():
    test = q.Quantity(10.5, dimensions=[0, 1.0, -2.0])
    assert test.units == "m s^-2.0"
    assert test.dimensions == [0.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def testing_dimensions():
    print(f"{'*' * 25} {testing_dimensions.__name__} {'*' * 25}")

    def dim_test(units, dim_list):
        qt = q.Quantity(10, units)
        print(f"{units} : {qt.dimensions}")
        assert qt.dimensions == dim_list

    dim_test("m", [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("m s^-1", [0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("kg m s^-2 m^-2", [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("Pa", [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("kPa", [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("Pa^2", [2.0, -2.0, -4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("daPa", [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("MPa", [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("kPa^2", [2.0, -2.0, -4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("slug in^-1 s^-1", [1.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("radian", [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    dim_test("ohm", [1.0, 2.0, -3.0, 0.0, 0.0, 0.0, 0.0, -2.0, 0.0])
    dim_test("lb cm s^-2", [1.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    print("-" * 75)


def testing_multipliers():
    print(f"{'*' * 25} {testing_multipliers.__name__} {'*' * 25}")

    def from_to(from_str, to_str):
        qt = q.Quantity(1, from_str)
        to = qt.to(to_str)
        print(f"from {qt} -> to {to}")

    from_to("mm", "cm")
    from_to("m", "ft")
    from_to("dm^3", "m^3")
    from_to("m s^-1", "cm s^-1")
    from_to("N", "dyne")
    from_to("m^2", "in^2")
    from_to("degree s^-1", "radian s^-1")
    from_to("radian s^-1", "degree s^-1")
    from_to("Pa", "lb m s^-2 ft^-2")
    from_to("lb m s^-2 ft^-2", "Pa")

    from_to("J kg^-1 K^-1", "J kg^-1 C^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 R^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 F^-1")

    from_to("K", "C")
    from_to("K", "R")
    from_to("K", "F")

    print("-" * 75)


def testing_arithmetic_operators():
    print(f"{'*' * 25} {testing_arithmetic_operators.__name__} {'*' * 25}")

    qt1 = q.Quantity(10, "m s^-1.0")
    qt2 = q.Quantity(5, "m s^-1.0")

    qt3 = qt1 * qt2

    print(f"{qt1} * {qt2} =  {qt3}")
    assert qt3.value == 50
    assert qt3.units == "m^2.0 s^-2.0"

    result = qt1 * 2
    print(f"{qt1} * {2} =  {result}")
    assert result.value == 20
    assert result.units == "m s^-1.0"

    result1 = 2 * qt1
    print(f"{2} * {qt1} =  {result1}")
    assert result1.value == 20
    assert result1.units == "m s^-1.0"

    q3 = qt1 / qt2

    print(f"{qt1} / {qt2} =  {q3}")
    assert q3.value == 2
    assert q3.units == ""

    result3 = qt1 / 2
    print(f"{qt1} / {2} =  {qt1 / 2}")
    assert result3.value == 5
    assert result3.units == "m s^-1.0"

    qa3 = qt1 + qt2

    print(f"{qt1} + {qt2} =  {qa3}")
    assert qa3.value == 15
    assert qa3.units == "m s^-1.0"

    with pytest.raises(q.QuantityError) as e:
        result5 = qt1 + 2
        print(f"{qt1} + {2} =  {result5}")

    with pytest.raises(q.QuantityError) as e:
        result6 = 2 + qt1
        print(f"{2} + {qt1} =  {result6}")

    qs3 = qt1 - qt2

    print(f"{qt1} - {qt2} =  {qs3}")
    assert qs3.value == 5
    assert qs3.units == "m s^-1.0"

    with pytest.raises(q.QuantityError) as e:
        result7 = qt1 - 2
        print(f"{qt1} - {2} =  {result7}")

    with pytest.raises(q.QuantityError) as e:
        result8 = 2 - qt1
        print(f"{2} - {qt1} =  {result8}")


def test_filtered_units():
    u = q.UnitsTable()

    assert u.filter_unit_term("cm^-2") == ("", "cm", -2)
    assert u.filter_unit_term("m") == ("", "m", 1)
    assert u.filter_unit_term("K^4") == ("", "K", 4)
    assert u.filter_unit_term("dam") == ("da", "m", 1)
    assert u.filter_unit_term("mm") == ("m", "m", 1)


def test_unit_system():
    sys = q.UnitSystem(
        name="mySys",
        base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
    )
    v = q.Quantity(10, "kg m s^2")
    v2 = sys.convert(v)

    assert sys.name == "mySys"
    assert sys.base_units == [
        "slug",
        "ft",
        "s",
        "R",
        "radian",
        "slugmol",
        "cd",
        "A",
        "sr",
    ]

    assert v2.value == 10
    assert v2.units == "slug ft s^2.0"

    si = q.UnitSystem(unit_sys="SI")
    v3 = q.Quantity(10, "ft^-2")
    v4 = si.convert(v3)

    assert si.name == "SI"
    assert si.base_units == ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"]

    assert v4.value == 10
    assert v4.units == "m^-2.0"
