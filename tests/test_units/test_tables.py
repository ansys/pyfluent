import ansys.fluent.core.quantity as q


def test_tables():
    ut = q.UnitsTable()

    assert isinstance(ut.api_quantity_map, dict)
    assert isinstance(ut.fundamental_units, dict)
    assert isinstance(ut.derived_units, dict)
    assert isinstance(ut.multipliers, dict)
    assert isinstance(ut.unit_systems, dict)
    assert isinstance(ut.dimension_order, dict)


def test_has_multiplier():
    ut = q.UnitsTable()

    assert ut._has_multiplier("km")
    assert ut._has_multiplier("ms")
    assert ut._has_multiplier("dam")

    assert not ut._has_multiplier("kg")
    assert not ut._has_multiplier("cm")
    assert not ut._has_multiplier("m")


def test_si_map():
    ut = q.UnitsTable()

    assert ut._si_map("g") == "kg"
    assert ut._si_map("lbm") == "kg"
    assert ut._si_map("ft") == "m"
    assert ut._si_map("slugmol") == "mol"
    assert ut._si_map("degree") == "radian"


def test_filter_unit_term():
    ut = q.UnitsTable()

    assert ut.filter_unit_term("cm^-2") == ("", "cm", -2)
    assert ut.filter_unit_term("m") == ("", "m", 1)
    assert ut.filter_unit_term("K^4") == ("", "K", 4)
    assert ut.filter_unit_term("dam") == ("da", "m", 1)
    assert ut.filter_unit_term("mm") == ("m", "m", 1)


def test_si_data():
    ut = q.UnitsTable()

    u1, m1, o1 = ut.si_data(units="g")
    assert u1 == "kg"
    assert m1 == 0.001
    assert o1 == 0

    u2, m2, o2 = ut.si_data(units="lb")
    assert u2 == "kg"
    assert m2 == 0.45359237
    assert o2 == 0

    u3, m3, o3 = ut.si_data(units="ft^2")
    assert u3 == "m^2"
    assert m3 == 0.09290303999999998
    assert o3 == 0

    u4, m4, o4 = ut.si_data(units="F")
    assert u4 == "K"
    assert m4 == 0.55555555555
    assert o4 == 459.67

    u5, m5, o5 = ut.si_data(units="farad")
    assert u5 == "kg^-1 m^-2 s^4 A^2"
    assert m5 == 1
    assert o5 == 0


def test_condense():
    ut = q.UnitsTable()

    assert ut.condense("m m m m") == "m^4"
    assert ut.condense("kg ft^3 kg^-2") == "kg^-1 ft^3"
    assert ut.condense("s^2 s^-2") == ""


def test_get_type():
    ut = q.UnitsTable()

    assert ut.get_type(units="kg") == "Mass"
    assert ut.get_type(units="m") == "Length"
    assert ut.get_type(units="s") == "Time"
    assert ut.get_type(units="K") == "Temperature"
    assert ut.get_type(units="delta_K") == "Temperature Difference"
    assert ut.get_type(units="radian") == "Angle"
    assert ut.get_type(units="mol") == "Chemical Amount"
    assert ut.get_type(units="cd") == "Light"
    assert ut.get_type(units="A") == "Current"
    assert ut.get_type(units="sr") == "Solid Angle"
    assert ut.get_type(units="") == "No Type"
    assert ut.get_type(units="farad") == "Derived"
    assert ut.get_type(units="N m s") == "Composite"
    assert ut.get_type(units="C^2") == "Temperature Difference"
