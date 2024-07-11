"""
This local parametric study workflow test performs these steps

TODO
"""

############################################################################

from math import inf

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.utils.parametric import (
    LocalParametricStudy,
    convert_design_point_parameter_units,
)


@pytest.mark.self_hosted
def test_local_parametric_run():
    ############################################################################
    # Read the hopper/mixer case

    case_filepath = examples.download_file(
        "Static_Mixer_Parameters.cas.h5",
        "pyfluent/static_mixer",
        return_without_path=False,
    )

    local_study = LocalParametricStudy(case_filepath=case_filepath)

    for idx in range(20):
        design_point = local_study.add_design_point("dp_" + str(idx))
        design_point.input_parameters["inlet1_vel"] = float(2 + idx)

    local_study.run_in_fluent(num_servers=4)

    table = local_study.design_point_table

    assert len(table) == 21

    outlet_velocity = -inf
    inlet_velocity = 0.0

    for point in table:
        ins = convert_design_point_parameter_units(point.input_parameters)
        outs = point.output_parameters
        new_inlet_velocity = ins["inlet1_vel"]
        new_outlet_velocity = outs["outlet-vel-avg-op"]
        assert new_inlet_velocity - inlet_velocity == 1.0
        assert new_outlet_velocity > outlet_velocity
        inlet_velocity = new_inlet_velocity
        outlet_velocity = new_outlet_velocity
