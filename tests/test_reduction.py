import pytest
from util.fixture_fluent import (  # load_static_mixer_case_2; noqa: F401
    load_static_mixer_case,
)
from ansys.fluent.core.solver import function
from ansys.fluent.core.solver.function import reduction

load_static_mixer_case_2 = load_static_mixer_case

def _test_locn_extraction(solver, solver2):
    locns = reduction._locn_names_and_objs(["inlet1"])
    assert locns == [["inlet1", ["inlet1"]]]

    all_bcs = solver.setup.boundary_conditions
    locns = reduction._locn_names_and_objs(all_bcs)
    assert locns == [
        ['interior--fluid', all_bcs],
        ['outlet', all_bcs],
        ['inlet1', all_bcs],
        ['inlet2', all_bcs], 
        ['wall', all_bcs]
    ]

    locns = reduction._locn_names_and_objs([all_bcs['inlet1']])
    assert locns == [
        ['inlet1', all_bcs['inlet1']]
    ]

    all_bcs = solver.setup.boundary_conditions
    all_bcs2 = solver2.setup.boundary_conditions
    locns = reduction._locn_names_and_objs([all_bcs, all_bcs2])
    assert locns == [
        ['interior--fluid', all_bcs],
        ['outlet', all_bcs],
        ['inlet1', all_bcs],
        ['inlet2', all_bcs], 
        ['wall', all_bcs],
        ['interior--fluid', all_bcs2],
        ['outlet', all_bcs2],
        ['inlet1', all_bcs2],
        ['inlet2', all_bcs2], 
        ['wall', all_bcs2]
    ]

def _test_area_average(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = "AreaAverage(AbsolutePressure, ['inlet1'])"
    expr_val = 42.0 # solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0
    val = reduction.area_average(
        expr = "AbsolutePressure",
        locations = solver.setup.boundary_conditions.velocity_inlet
    )
    assert val == expr_val
    solver.setup.named_expressions.pop(key="test_expr_1")


@pytest.mark.fluent_231
def test_reductions(load_static_mixer_case, load_static_mixer_case_2) -> None:
    solver = load_static_mixer_case
    solver2 = load_static_mixer_case_2
    _test_locn_extraction(solver, solver2)
    _test_area_average(solver)