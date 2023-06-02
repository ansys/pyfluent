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


def test_setters_7():
    v = q.Quantity(7.0, "kg")
    v.value = 1.0
    v.type = "Mass"
    assert v.value == 1.0
    assert v.type == "Mass"


def test_to_8():
    v = q.Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.unit_str == "ft"


def test_to_9():
    v = q.Quantity(1.0, "m")
    to = v.to("mm")
    assert to.value == 1000
    assert to.unit_str == "mm"


def test_to_10():
    v = q.Quantity(100000.0, "Pa")
    to = v.to("kPa")
    assert to.value == 100.0
    assert to.unit_str == "kPa"


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


def test_to_36():
    v = q.Quantity(1.0, "BTU lb^-1 R^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.unit_str == "J kg^-1 K^-1"


def test_to_37():
    v = q.Quantity(1.0, "BTU lb^-1 F^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.unit_str == "J kg^-1 K^-1"


def test_to_38():
    v = q.Quantity(1.0, "gal^-1")
    to = v.to("m^-3")
    assert to.value == pytest.approx(264.172, DELTA)
    assert to.unit_str == "m^-3"


def test_to_39():
    v = q.Quantity(1.0, "BTU ft^-2")
    to = v.to("J m^-2")
    assert to.value == pytest.approx(11356.5713242, DELTA)
    assert to.unit_str == "J m^-2"


def test_to_40():
    v = q.Quantity(2.0, "radian")
    with pytest.raises(TypeError) as e:
        convert = v.to(0)


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


def test_convert_42():
    v = q.Quantity(7.0, "K mol")
    with pytest.raises(ValueError) as e:
        convert = v.convert("")


def test_repr_42():
    v = q.Quantity(1.0, "m")
    assert v.__repr__() == 'Quantity (1.0, "m")'


def test_math_43():
    deg = q.Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = q.Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    root = q.Quantity(100.0, "")
    assert math.sqrt(root) == 10.0


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
    assert q1_sq.unit_str == "m^2.0 s^-2.0"

    assert float(q1) ** 2 == 100.0
    assert float(q2) ** 2 == 25.0


def test_neg_46():
    q0 = q.Quantity(10.0, "m s^-1")
    q1 = -q0
    assert q1.value == -10.0


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


def test_power_56():
    qt = q.Quantity(5.0, "m^0")
    qtm = qt * 2

    assert qtm.value == 10.0
    assert qtm.unit_str == ""


def test_ge_57():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y >= x
    assert 15.7 >= r
    assert r >= 7.8

    with pytest.raises(ValueError) as e_info:
        assert x >= z
        assert x >= y
        assert 5.0 >= r

    with pytest.raises(TypeError) as e_info:
        assert x >= 5.0


def test_gt_59():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y > x
    assert 15.7 > r
    assert r > 7.8

    with pytest.raises(ValueError) as e_info:
        assert x > z
        assert x > y
        assert 5.0 > r

    with pytest.raises(TypeError) as e_info:
        assert x > 5.0


def test_lt_60():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert x < y
    assert r < 15.7
    assert 7.8 < r

    with pytest.raises(ValueError) as e_info:
        assert z < x
        assert y < x
        assert r < 0.5

    with pytest.raises(TypeError) as e_info:
        assert 5.0 < x


def test_le_61():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert x <= y
    assert r <= 15.7
    assert 7.8 <= r

    with pytest.raises(ValueError) as e_info:
        assert z <= x
        assert y <= x
        assert r <= 0.5

    with pytest.raises(TypeError) as e_info:
        assert 5.0 <= x


def test_eq_62():
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

    with pytest.raises(ValueError) as e_info:
        assert z == x
        assert y == x
        assert r == 0.5

    with pytest.raises(TypeError) as e_info:
        assert 5.0 == x


def test_neq_63():
    x = q.Quantity(10.5, "cm")
    y = q.Quantity(10.5, "m")
    z = q.Quantity(10.5, "g")
    r = q.Quantity(10.5, "")

    assert y != x
    assert x != y

    assert r != 0.5
    assert 0.5 != r


def test_error_64():
    err = q.QuantityError("mm", "K")
    assert err.__str__() == f"'mm' and 'K' have incompatible dimensions."


def test_tempK_48():
    k = q.Quantity(-40, "K")

    kc = k.to("C")
    assert kc.value == -313.15
    assert kc.unit_str == "C"

    kc = k.to("R")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.unit_str == "R"

    kc = k.to("F")
    assert kc.value == pytest.approx(-531.67, DELTA)
    assert kc.unit_str == "F"


def test_temp_49():
    mk = q.Quantity(-40000.0, "mK")
    uc = mk.to("uC^1")
    assert uc.value == -40000273.15


def test_temp_50():
    k = q.Quantity(1.0, "K")

    f = k.to("F")
    r = k.to("R")
    c = k.to("C")

    assert f.value == pytest.approx(-457.87, DELTA)
    assert r.value == pytest.approx(1.8, DELTA)
    assert c.value == pytest.approx(-272.15, DELTA)


def test_temp_51():
    c = q.Quantity(1.0, "C")

    f = c.to("F")
    r = c.to("R")
    k = c.to("K")

    assert f.value == pytest.approx(33.80, DELTA)
    assert r.value == pytest.approx(493.469, DELTA)
    assert k.value == 274.15


def test_temp_52():
    r = q.Quantity(1.0, "R")

    f = r.to("F")
    c = r.to("C")
    k = r.to("K")

    assert f.value == pytest.approx(-458.6699, DELTA)
    assert c.value == pytest.approx(-272.5944, DELTA)
    assert k.value == pytest.approx(0.555556, DELTA)


def test_temp_53():
    f = q.Quantity(1.0, "F")

    c = f.to("C")
    r = f.to("R")
    k = f.to("K")

    assert c.value == pytest.approx(-17.2222, DELTA)
    assert r.value == pytest.approx(460.670, DELTA)
    assert k.value == pytest.approx(255.927, DELTA)


def test_temp_54():
    hc = q.Quantity(1.0, "J g^-1 K^-1")

    hcto1 = hc.to("kJ kg^-1 K^-1")

    assert hcto1.value == pytest.approx(1.0, DELTA)
    assert hcto1.unit_str == "kJ kg^-1 K^-1"

    hcto2 = hc.to("J kg^-1 C^-1")

    assert hcto2.value == pytest.approx(1000.0, DELTA)
    assert hcto2.unit_str == "J kg^-1 C^-1"

    hcto3 = hc.to("kJ kg^-1 C^-1")

    assert hcto3.value == pytest.approx(1.0, DELTA)
    assert hcto3.unit_str == "kJ kg^-1 C^-1"

    hcto4 = hc.to("cal g^-1 C^-1")

    assert hcto4.value == pytest.approx(0.2390057, DELTA)
    assert hcto4.unit_str == "cal g^-1 C^-1"

    hcto5 = hc.to("cal kg^-1 C^-1")

    assert hcto5.value == pytest.approx(239.0057, DELTA)
    assert hcto5.unit_str == "cal kg^-1 C^-1"

    hcto6 = hc.to("kcal kg^-1 C^-1")

    assert hcto6.value == pytest.approx(0.2390057, DELTA)
    assert hcto6.unit_str == "kcal kg^-1 C^-1"

    hcto7 = hc.to("BTU lb^-1 F^-1")

    assert hcto7.value == pytest.approx(0.238845, DELTA)
    assert hcto7.unit_str == "BTU lb^-1 F^-1"


def test_temp_54():
    temp_var = q.Quantity(1.0, "kg m^-3 s^-1 K^2")

    temp_varto1 = temp_var.to("g cm^-3 s^-1 K^2")

    assert temp_varto1.value == pytest.approx(0.001, DELTA)
    assert temp_varto1.unit_str == "g cm^-3 s^-1 K^2"

    temp_varto2 = temp_var.to("kg mm^-3 s^-1 K^2")

    assert temp_varto2.value == pytest.approx(1e-09, DELTA)
    assert temp_varto2.unit_str == "kg mm^-3 s^-1 K^2"

    temp_varto3 = temp_var.to("kg um^-3 s^-1 K^2")

    assert temp_varto3.value == pytest.approx(9.999999999999999e-19, DELTA)
    assert temp_varto3.unit_str == "kg um^-3 s^-1 K^2"

    temp_varto4 = temp_var.to("mg mm^-3 ms^-1 K^2")

    assert temp_varto4.value == pytest.approx(1.0000000000000002e-06, DELTA)
    assert temp_varto4.unit_str == "mg mm^-3 ms^-1 K^2"

    temp_varto5 = temp_var.to("g cm^-3 us^-1 K^2")

    assert temp_varto5.value == pytest.approx(1e-09, DELTA)
    assert temp_varto5.unit_str == "g cm^-3 us^-1 K^2"

    temp_varto6 = temp_var.to("pg um^-3 ms^-1 K^2")

    assert temp_varto6.value == pytest.approx(9.999999999999997e-07, DELTA)
    assert temp_varto6.unit_str == "pg um^-3 ms^-1 K^2"


def test_temp_inverse_64():
    c = q.Quantity(2.0, "C")
    assert float(c) == 275.15

    c_inverse = q.Quantity(2.0, "C^-1")
    assert float(c_inverse) == 2.0


def test_temp_inverse_65():
    f = q.Quantity(2.0, "F")
    assert float(f) == pytest.approx(256.483311, DELTA)

    f_inverse = q.Quantity(2.0, "F^-1")
    assert float(f_inverse) == pytest.approx(3.5999999999999996, DELTA)


def test_temp_type_66():
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


def test_temp_difference_67():
    td1 = q.Quantity(150.0, "delta_C")
    assert td1.type == "Temperature Difference"

    td2 = q.Quantity(100.0, "delta_C")
    assert td2.type == "Temperature Difference"

    td = td1 - td2
    assert td.type == "Temperature Difference"

    td_m = td * 2
    assert td_m.unit_str == "delta_K"
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


def test_core_temp_68():
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


def test_temp_addition_69():
    t1 = q.Quantity(150.0, "C")
    t2 = q.Quantity(50.0, "C")

    td = t1 - t2
    assert td.type == "Temperature Difference"
    assert float(td) == 100.0
    assert td.unit_str == "delta_K"

    kd = q.Quantity(50.0, "delta_C")
    k = q.Quantity(50.0, "K")

    t = k + kd
    assert float(t) == 100.0
    assert t.type == "Temperature Difference"


def test_quantity_map_70():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }

    api_test = q.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.unit_str == "kg^3.0 m^-1.5 s^-6.5 A^3.0 cd"


def test_quantity_map_71():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 2,
        "Epsilon Flux Coefficient": 2,
    }

    with pytest.raises(ValueError):
        api_test = q.Quantity(
            10.5, unit_str="kg m s^-1", quantity_map=quantity_map_from_settings_API
        )


def test_quantity_map_72():
    quantity_map_from_settings_API = {
        "Temperature": 1,
        "Pressure": 1,
        "Volume": 1,
    }

    api_test = q.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.unit_str == "K Pa m^3.0"


def test_unit_from_dimensions_73():
    p = q.Quantity(10.5, dimensions=[1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert p.unit_str == "kg m^-1.0 s^-2.0"


def test_unit_from_dimensions_74():
    l = q.Quantity(10.5, dimensions=[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert l.unit_str == "m"


def test_unit_from_dimensions_75():
    x = q.Quantity(10.5, dimensions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert x.unit_str == ""


def test_unit_from_dimensions_76():
    test = q.Quantity(10.5, dimensions=[0, 1, -1])
    assert test.unit_str == "m s^-1.0"
    assert test.dimensions == [0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_unit_from_dimensions_77():
    test = q.Quantity(10.5, dimensions=[0, 1.0, -2.0])
    assert test.unit_str == "m s^-2.0"
    assert test.dimensions == [0.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def testing_dimensions():
    print(f"{'*' * 25} {testing_dimensions.__name__} {'*' * 25}")

    def dim_test(unit_str, dim_list):
        qt = q.Quantity(10, unit_str)
        print(f"{unit_str} : {qt.dimensions}")
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
    assert qt3.unit_str == "m^2.0 s^-2.0"

    result = qt1 * 2
    print(f"{qt1} * {2} =  {result}")
    assert result.value == 20
    assert result.unit_str == "m s^-1.0"

    result1 = 2 * qt1
    print(f"{2} * {qt1} =  {result1}")
    assert result1.value == 20
    assert result1.unit_str == "m s^-1.0"

    q3 = qt1 / qt2

    print(f"{qt1} / {qt2} =  {q3}")
    assert q3.value == 2
    assert q3.unit_str == ""

    result3 = qt1 / 2
    print(f"{qt1} / {2} =  {qt1 / 2}")
    assert result3.value == 5
    assert result3.unit_str == "m s^-1.0"

    qa3 = qt1 + qt2

    print(f"{qt1} + {qt2} =  {qa3}")
    assert qa3.value == 15
    assert qa3.unit_str == "m s^-1.0"

    with pytest.raises(TypeError) as e:
        result5 = qt1 + 2
        print(f"{qt1} + {2} =  {result5}")

    with pytest.raises(TypeError) as e:
        result6 = 2 + qt1
        print(f"{2} + {qt1} =  {result6}")

    qs3 = qt1 - qt2

    print(f"{qt1} - {qt2} =  {qs3}")
    assert qs3.value == 5
    assert qs3.unit_str == "m s^-1.0"

    with pytest.raises(TypeError) as e:
        result7 = qt1 - 2
        print(f"{qt1} - {2} =  {result7}")

    with pytest.raises(TypeError) as e:
        result8 = 2 - qt1
        print(f"{2} - {qt1} =  {result8}")
