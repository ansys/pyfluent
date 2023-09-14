import pytest

import ansys.fluent.core.quantity as q


def test_units():
    d1 = q.Dimensions(units="ft")
    assert d1.units == "ft"
    assert d1.dimensions == [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d2 = q.Dimensions(units="kPa")
    assert d2.units == "kPa"
    assert d2.dimensions == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d3 = q.Dimensions(units="slug^2 ft^-1 s R radian^-3 slugmol cd^4 A sr")
    assert d3.units == "slug^2 ft^-1 s R radian^-3 slugmol cd^4 A sr"
    assert d3.dimensions == [2.0, -1.0, 1.0, 1.0, -3.0, 1.0, 4.0, 1.0, 1.0]


def test_dimensions():
    d1 = q.Dimensions(dimensions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert d1.units == ""
    assert d1.dimensions == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d2 = q.Dimensions(dimensions=[0, 1.0, -2.0])
    assert d2.units == "m s^-2"
    assert d2.dimensions == [0.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d3 = q.Dimensions(dimensions=[1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert d3.units == "kg m^-1 s^-2"
    assert d3.dimensions == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_unit_sys():
    d1 = q.Dimensions(
        dimensions=[1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        unit_sys=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
    )
    assert d1.units == "slug ft^-1 s^-2"
    assert d1.dimensions == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_max_dim_len():
    max_len = q.Dimensions.max_dim_len()
    assert max_len == 9


def test_errors():
    with pytest.raises(q.DimensionsError) as e_info:
        d1 = q.Dimensions(units="m s", dimensions=[0.0, 1.0, 1.0])

    with pytest.raises(q.DimensionsError) as e_info:
        d2 = q.Dimensions(dimensions=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])


def test_error_messages():
    e1 = q.DimensionsError.EXCESSIVE_PARAMETERS()
    assert (
        e1.__str__()
        == "Dimensions only accepts 1 of the following parameters: (units) or (dimensions)."
    )

    e2 = q.DimensionsError.EXCESSIVE_DIMENSIONS(200)
    assert (
        e2.__str__()
        == "The `dimensions` argument must contain 9 values or less, currently there are 200."
    )
