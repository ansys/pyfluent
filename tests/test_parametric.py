###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

"""
Unit tests for parameteric study code - no framework use just for now
"""

from ansys.fluent.addons.parametric import (
    DesignPointStatus,
    DesignPoint,
    DesignPointTable,
    ParametricStudy)

def make_simple_base_design_point():
    dp = DesignPoint("base")
    dp.inputs = {"x" : 2}
    dp.outputs = {"y" : 0}
    return dp

class XTimes:
    """
    test class
    """
    def __init__(self, multiplier):
        self.multiplier = multiplier
        self.input_parameters = {"x" : 0}
        self.output_parameters = {"y" : 0}

    def __call__(self):
        return self

    def set_input_parameter(self, parameter_name: str, value):
        self.input_parameters[parameter_name] = value

    def update(self):
        self.output_parameters["y"] = \
            self.multiplier * self.input_parameters["x"]


def test_create_base_design_point():
    dp = make_simple_base_design_point()
    assert dp.name == "base"
    assert dp.inputs == {"x" : 2}
    assert dp.outputs == {"y" : 0}
    assert dp.status == DesignPointStatus.OUT_OF_DATE

def test_create_user_defined_design_point():
    dp = DesignPoint(
        "DP1",
        base_design_point=make_simple_base_design_point())
    assert dp.name == "DP1"
    assert dp.inputs == {"x" : 2}
    assert dp.outputs == {"y" : 0}
    assert dp.status == DesignPointStatus.OUT_OF_DATE

def test_start_and_end_design_point_update():
    base_dp = make_simple_base_design_point()
    dp1 = DesignPoint(
        "DP1",
        base_design_point=base_dp)
    base_dp.on_start_updating()
    assert base_dp.status == DesignPointStatus.UPDATING
    assert dp1.status == DesignPointStatus.OUT_OF_DATE
    base_dp.on_end_updating({"y" : 1})
    assert base_dp.status == DesignPointStatus.UPDATED
    assert dp1.status == DesignPointStatus.OUT_OF_DATE
    dp1.on_start_updating()
    assert base_dp.status == DesignPointStatus.UPDATED
    assert dp1.status == DesignPointStatus.UPDATING
    dp1.on_end_updating({"y" : 42})
    assert base_dp.status == DesignPointStatus.UPDATED
    assert dp1.status == DesignPointStatus.UPDATED

def test_add_remove_find_points_in_table():
    table = DesignPointTable(DesignPoint("base"))
    table.append(DesignPoint("a"))
    table.append(DesignPoint("b"))
    table.append(DesignPoint("c"))
    assert table.find_design_point("b").name == "b"
    assert table.find_design_point("base").name == "base"
    assert table.find_design_point(0).name == "base"
    assert table.find_design_point(3).name == "c"
    table.remove_design_point("a")
    table.remove_design_point(2)
    assert len(table) == 2
    assert table.find_design_point("b").name == "b"
    assert table.find_design_point("base").name == "base"
    throws = False
    try:
        table.remove_design_point(0)
    except RuntimeError:
        throws = True
    assert throws
    throws = False
    try:
        table.remove_design_point("base")
    except RuntimeError:
        throws = True
    assert throws
    assert len(table) == 2
    assert table.find_design_point("b").name == "b"
    assert table.find_design_point("base").name == "base"

def test_run_parametric_study():
    multiplier = 3
    study = ParametricStudy(
        base_design_point_name="xxx",
        launcher=XTimes(multiplier))
    inputs = [0, 3, 8, -5]
    for i in range(1, len(inputs)):
        study.add_design_point("d"+repr(i)).set_input("x", inputs[i])
    for i in range(len(inputs)):
        assert study.design_point(i).status == \
            DesignPointStatus.OUT_OF_DATE
    study.update_all()
    for i in range(len(inputs)):
        assert study.design_point(i).status == \
            DesignPointStatus.UPDATED
        assert study.design_point(i).outputs["y"] == \
            multiplier * inputs[i]

def test_run_parametric_study_and_block():
    multiplier = 3
    study = ParametricStudy(
        base_design_point_name="xxx",
        launcher=XTimes(multiplier))
    inputs = [0, 3, 8, -5]
    for i in range(1, len(inputs)):
        study.add_design_point("d"+repr(i)).set_input("x", inputs[i])
    for i in range(len(inputs)):
        if i%2:
            study.design_point(i).block_updates()
    for i in range(len(inputs)):
        status = DesignPointStatus.BLOCKED if i%2 else \
            DesignPointStatus.OUT_OF_DATE
        assert study.design_point(i).status == status
    study.update_all()
    for i in range(len(inputs)):
        status = DesignPointStatus.BLOCKED if i%2 else \
            DesignPointStatus.UPDATED
        assert study.design_point(i).status == status
        assert study.design_point(i).outputs["y"] == \
            (0 if i%2 else multiplier) * inputs[i]
    for i in range(len(inputs)):
        if i%2:
            study.update_design_point(study.design_point(i))
    for i in range(len(inputs)):
        assert study.design_point(i).status == \
            DesignPointStatus.UPDATED
        assert study.design_point(i).outputs["y"] == \
            multiplier * inputs[i]

def test_all():
    test_create_base_design_point()
    test_create_user_defined_design_point()
    test_start_and_end_design_point_update()
    test_add_remove_find_points_in_table()
    test_run_parametric_study()
    test_run_parametric_study_and_block()