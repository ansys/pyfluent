import pytest

import ansys.fluent.core.quantity as q


def test_quantity_map():
    qm1_map = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }
    qm1 = q.QuantityMap(quantity_map=qm1_map)
    assert qm1.units == "kg^3 m^-1.5 s^-6.5 A^3 cd"

    qm2_map = {
        "Temperature": 1,
        "Pressure": 1,
        "Volume": 1,
    }
    qm2 = q.QuantityMap(quantity_map=qm2_map)
    assert qm2.units == "K Pa m^3"


def test_errors():
    qm_map = {"Bread": 2, "Chicken": 1, "Eggs": 7, "Milk": -4}
    with pytest.raises(q.QuantityMapError) as e_info:
        qm = q.QuantityMap(quantity_map=qm_map)


def test_error_messages():
    e1 = q.QuantityMapError.UNKNOWN_MAP_ITEM("Risk")
    assert e1.__str__() == "`Risk` is not a valid quantity map item."
