import pytest
from util.fixture_fluent import load_static_mixer_case  # noqa: F401

from ansys.fluent.core.solver.function import reduction

load_static_mixer_case_2 = load_static_mixer_case


def _test_locn_extraction(solver1, solver2):
    locns = reduction._locn_names_and_objs(["inlet1"])
    assert locns == [["inlet1", ["inlet1"]]]

    all_bcs = solver1.setup.boundary_conditions
    locns = reduction._locn_names_and_objs(all_bcs)
    assert locns == [
        ["interior--fluid", all_bcs],
        ["outlet", all_bcs],
        ["inlet1", all_bcs],
        ["inlet2", all_bcs],
        ["wall", all_bcs],
    ]

    locns = reduction._locn_names_and_objs([all_bcs["inlet1"]])
    assert locns == [["inlet1", all_bcs["inlet1"]]]

    all_bcs = solver1.setup.boundary_conditions
    all_bcs2 = solver2.setup.boundary_conditions
    locns = reduction._locn_names_and_objs([all_bcs, all_bcs2])
    assert locns == [
        ["interior--fluid", all_bcs],
        ["outlet", all_bcs],
        ["inlet1", all_bcs],
        ["inlet2", all_bcs],
        ["wall", all_bcs],
        ["interior--fluid", all_bcs2],
        ["outlet", all_bcs2],
        ["inlet1", all_bcs2],
        ["inlet2", all_bcs2],
        ["wall", all_bcs2],
    ]


def _test_context(solver):
    solver.solution.initialization.hybrid_initialize()

    assert reduction.area(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
        ctxt=solver,
    )

    assert reduction.area(locations=["inlet1"], ctxt=solver)


def _test_area_average(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaAve(AbsolutePressure, ['inlet1'])"
    expr_val = solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0
    val = reduction.area_average(
        expr="AbsolutePressure",
        locations=solver.setup.boundary_conditions.velocity_inlet,
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
        [
            solver1.setup.boundary_conditions["outlet"],
            solver2.setup.boundary_conditions["outlet"],
        ],
    )
    assert result == expected_result
    solver1.setup.named_expressions.pop(key="test_expr_1")
    solver1.setup.named_expressions.pop(key="test_expr_2")


def _test_count(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = "Count(['inlet1'])"
    expr_val_1 = solver.setup.named_expressions["test_expr_1"].get_value()
    solver.setup.named_expressions["test_expr_1"].definition = "Count(['inlet2'])"
    expr_val_2 = solver.setup.named_expressions["test_expr_1"].get_value()
    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "Count(['inlet1', 'inlet2'])"
    expr_val_3 = solver.setup.named_expressions["test_expr_1"].get_value()
    assert expr_val_3 == expr_val_1 + expr_val_2
    red_val_1 = reduction.count(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]]
    )
    red_val_2 = reduction.count(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet2"]]
    )
    red_val_3 = reduction.count(
        locations=[solver.setup.boundary_conditions.velocity_inlet]
    )
    assert red_val_1 == expr_val_1
    assert red_val_2 == expr_val_2
    assert red_val_3 == expr_val_3
    solver.setup.named_expressions.pop(key="test_expr_1")


def _test_centroid(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = "Centroid(['inlet1'])"
    expr_val_1 = solver.setup.named_expressions["test_expr_1"].get_value()
    solver.setup.named_expressions["test_expr_1"].definition = "Centroid(['inlet2'])"
    expr_val_2 = solver.setup.named_expressions["test_expr_1"].get_value()
    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "Centroid(['inlet1', 'inlet2'])"
    expr_val_3 = solver.setup.named_expressions["test_expr_1"].get_value()
    red_val_1 = reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]]
    )
    red_val_2 = reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet2"]]
    )
    red_val_3 = reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet]
    )
    assert (red_val_1 == expr_val_1).all()
    assert (red_val_2 == expr_val_2).all()
    assert (red_val_3 == expr_val_3).all()
    solver.setup.named_expressions.pop(key="test_expr_1")


def _test_area_integrated_average(solver1, solver2):
    solver1.solution.initialization.hybrid_initialize()
    solver2.solution.initialization.hybrid_initialize()

    solver1.setup.named_expressions["test_expr_1"] = {}
    solver1.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet1'])"
    expr_val_1 = solver1.setup.named_expressions["test_expr_1"].get_value()
    solver1.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet2'])"
    expr_val_2 = solver1.setup.named_expressions["test_expr_1"].get_value()
    solver1.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet1', 'inlet2'])"
    expr_val_3 = solver1.setup.named_expressions["test_expr_1"].get_value()
    assert expr_val_3 - (expr_val_1 + expr_val_2) <= 0.000000001

    red_val_1 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver1.setup.boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_2 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver1.setup.boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_3 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver1.setup.boundary_conditions.velocity_inlet],
    )

    assert red_val_1 == expr_val_1
    assert red_val_2 == expr_val_2
    assert red_val_3 == expr_val_3

    solver2.setup.named_expressions["test_expr_1"] = {}
    solver2.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet1'])"
    expr_val_4 = solver2.setup.named_expressions["test_expr_1"].get_value()
    solver2.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet2'])"
    expr_val_5 = solver2.setup.named_expressions["test_expr_1"].get_value()
    solver2.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaInt(AbsolutePressure, ['inlet1', 'inlet2'])"
    expr_val_6 = solver2.setup.named_expressions["test_expr_1"].get_value()
    assert expr_val_6 - (expr_val_4 + expr_val_5) <= 0.000000001

    red_val_4 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_5 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_6 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet],
    )

    assert red_val_4 == expr_val_4
    assert red_val_5 == expr_val_5
    assert red_val_6 == expr_val_6

    red_val_7 = reduction.area_integrated_average(
        expr="AbsolutePressure",
        locations=[
            solver1.setup.boundary_conditions.velocity_inlet,
            solver2.setup.boundary_conditions.velocity_inlet,
        ],
    )

    assert red_val_7 - (expr_val_3 + expr_val_6) <= 0.000000001

    solver1.setup.named_expressions.pop(key="test_expr_1")


def _test_error_handling(solver):
    with pytest.raises(RuntimeError) as msg:
        reduction.area_average(
            expr="AbsoluteVelocity",  # This is a wrong expression intentionally passed
            locations=solver.setup.boundary_conditions.velocity_inlet,
        )

    assert msg.value.args[0] == "Unable to evaluate expression"


def _test_force(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = "Force(['wall'])"
    expr_val_1 = solver.setup.named_expressions["test_expr_1"].get_value()

    red_total_force = reduction.force(locations=[solver.setup.boundary_conditions.wall])
    red_pressure_force = reduction.pressure_force(locations=["wall"], ctxt=solver)
    red_viscous_force = reduction.viscous_force(
        locations=[solver.setup.boundary_conditions.wall]
    )

    assert (red_total_force == expr_val_1).all()

    assert (red_pressure_force + red_viscous_force == red_total_force).all()

    solver.setup.named_expressions.pop(key="test_expr_1")


def _test_moment(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "Moment(Force(['wall']),['wall'])"
    expr_val_1 = solver.setup.named_expressions["test_expr_1"].get_value()

    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "Moment(['inlet1'],['wall'])"
    expr_val_2 = solver.setup.named_expressions["test_expr_1"].get_value()

    red_moment_force = reduction.moment(
        expr="Force(['wall'])", locations=[solver.setup.boundary_conditions.wall]
    )

    red_moment_location = reduction.moment(
        expr="['inlet1']",
        locations=[solver.setup.boundary_conditions.wall],
    )

    assert (red_moment_force == expr_val_1).all()
    assert (red_moment_location == expr_val_2).all()

    solver.setup.named_expressions.pop(key="test_expr_1")


@pytest.mark.dev
@pytest.mark.fluent_231
def test_reductions(load_static_mixer_case, load_static_mixer_case_2) -> None:
    solver1 = load_static_mixer_case
    solver2 = load_static_mixer_case_2
    _test_context(solver1)
    _test_locn_extraction(solver1, solver2)
    _test_area_average(solver1)
    _test_min(solver1, solver2)
    _test_count(solver1)
    _test_centroid(solver1)
    _test_area_integrated_average(solver1, solver2)
    _test_error_handling(solver1)
    _test_force(solver1)
    _test_moment(solver1)
