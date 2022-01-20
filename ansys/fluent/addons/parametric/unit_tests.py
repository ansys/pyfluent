###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

from . import ( 
    DesignPointStatus, 
    DesignPoint,
    DesignPointTable,
    ParametricStudy)

def make_simple_base_design_point():
    dp = DesignPoint("base")
    dp.inputs = {"x":2}
    dp.outputs = {"y":0}
    return dp

class NTimes:
    def __init__(self, multiplier):
        self.__multiplier = multiplier
        self.input_parameters = {'x': 0}
        self.output_parameters = {'y': 0}
    
    def __call__(self):
        return self
    
    def set_input_parameter(self, parameter_name: str, value):
        self.input_parameters[parameter_name] = value

    def initialize_with_case(self, case_file_name):
        pass
    
    def update(self):
        self.output_parameters['y'] = \
            self.__multiplier * self.input_parameters['x']


def test_create_base_design_point():
    dp = make_simple_base_design_point()
    assert(dp.name == "base")
    assert(dp.inputs == {"x":2})
    assert(dp.outputs == {"y":0})
    assert(dp.status == DesignPointStatus.OUT_OF_DATE)

def test_create_user_defined_design_point():
    dp = DesignPoint(
        "DP1",
        base_design_point=make_simple_base_design_point())
    assert(dp.name == "DP1")
    assert(dp.inputs == {"x":2})
    assert(dp.outputs == {"y":0})
    assert(dp.status == DesignPointStatus.OUT_OF_DATE)
    
def test_start_and_end_design_point_update():
    base_dp = make_simple_base_design_point()
    dp1 = DesignPoint(
        "DP1",
        base_design_point=base_dp)
    base_dp.on_start_updating()
    assert(base_dp.status == DesignPointStatus.UPDATING)
    assert(dp1.status == DesignPointStatus.OUT_OF_DATE)
    base_dp.on_end_updating({"y":1})
    assert(base_dp.status == DesignPointStatus.UPDATED)
    assert(dp1.status == DesignPointStatus.OUT_OF_DATE)
    dp1.on_start_updating()
    assert(base_dp.status == DesignPointStatus.UPDATED)
    assert(dp1.status == DesignPointStatus.UPDATING)
    dp1.on_end_updating({"y":42})
    assert(base_dp.status == DesignPointStatus.UPDATED)
    assert(dp1.status == DesignPointStatus.UPDATED)

def test_add_and_find_points_in_table():
    table = DesignPointTable(DesignPoint("base"))
    table.append(DesignPoint("a"))
    table.append(DesignPoint("b"))
    table.append(DesignPoint("c"))
    assert(table.find_design_point("b").name == "b")
    assert(table.find_design_point("base").name == "base")
    assert(table.find_design_point(0).name == "base")
    assert(table.find_design_point(3).name == "c")

def test_run_parametric_study():
    study = ParametricStudy(
        case_file_name='',
        base_design_point_name='xxx',
        launcher=NTimes(4))
    study.add_design_point("d1").set_input("x", 3)
    study.add_design_point("d2").set_input("x", 8)
    study.add_design_point("d3").set_input("x", -5)
    study.update_all()
    assert(study.design_point(0).outputs['y'] == 4 * 0)
    assert(study.design_point(1).outputs['y'] == 4 * 3)
    assert(study.design_point(2).outputs['y'] == 4 * 8)
    assert(study.design_point(3).outputs['y'] == 4 * -5)

def test_all():
    test_create_base_design_point()
    test_create_user_defined_design_point()
    test_start_and_end_design_point_update()
    test_add_and_find_points_in_table()
    test_run_parametric_study()

    

        

      


