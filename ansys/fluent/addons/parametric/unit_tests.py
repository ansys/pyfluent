###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

from . import ( 
    DesignPointStatus, 
    DesignPoint,
    DesignPointTable)

def make_simple_base_design_point():
    dp = DesignPoint("base")
    dp.inputs = {"x":2}
    dp.outputs = {"y":0}
    return dp

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


def test_all():
    test_create_base_design_point()
    test_create_user_defined_design_point()
    

        

      


