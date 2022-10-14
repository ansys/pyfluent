import pytest
import weakref
from util.fixture_fluent import (  # load_static_mixer_case_2; noqa: F401
    load_static_mixer_case,
)
from ansys.fluent.core.solver import function
from ansys.fluent.core.solver.function import reduction

load_static_mixer_case_2 = load_static_mixer_case

def _test_locn_extraction(solver1, solver2):
    locns = reduction._locn_names_and_objs(["inlet1"])
    assert locns == [["inlet1", ["inlet1"]]]

    all_bcs = solver1.setup.boundary_conditions
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

    all_bcs = solver1.setup.boundary_conditions
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
    solver.setup.named_expressions["test_expr_1"].definition = "AreaAve(AbsolutePressure, ['inlet1'])"
    expr_val = solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0
    val = reduction.area_average(
        expr = "AbsolutePressure",
        locations = solver.setup.boundary_conditions.velocity_inlet
    )
    assert val == expr_val
    solver.setup.named_expressions.pop(key="test_expr_1")

def _test_min(solver1, solver2):
    vmag = solver1.setup.boundary_conditions["inlet1"].vmag.value()
    solver1.setup.boundary_conditions["inlet1"].vmag = 0.9 * vmag
    solver2.setup.boundary_conditions["inlet1"].vmag = 1.1 * vmag
    solver1.solution.initialization.hybrid_initialize()
    solver2.solution.initialization.hybrid_initialize()
    solver1.setup.named_expressions["test_expr_1"] = {}
    test_expr1 = solver1.setup.named_expressions["test_expr_1"]
    test_expr1.definition = "sqrt(VelocityMagnitude)"
    solver1.setup.named_expressions["test_expr_2"] = {}
    test_expr2 = solver1.setup.named_expressions["test_expr_2"]
    test_expr2.definition = "minimum(test_expr_2, ['outlet'])"
    expected_result = test_expr2.get_value()
    result = reduction.minimum(
        test_expr1,
        [solver1.setup.boundary_conditions["outlet"], solver2.setup.boundary_conditions["outlet"]]
        )
    assert result == expected_result
    solver1.setup.named_expressions.pop(key="test_expr_1")
    solver1.setup.named_expressions.pop(key="test_expr_2")


@pytest.mark.fluent_231
def test_reductions(load_static_mixer_case, load_static_mixer_case_2) -> None:
    solver1 = load_static_mixer_case
    solver2 = load_static_mixer_case_2
    _test_locn_extraction(solver1, solver2)
    _test_area_average(solver1)
    _test_min(solver1, solver2)