import pytest
from util.fixture_fluent import load_static_mixer_case  # noqa: F401

from ansys.fluent.core.services.reduction import _locn_names_and_objs

load_static_mixer_case_2 = load_static_mixer_case


def _test_locn_extraction(solver1, solver2):
    locns = _locn_names_and_objs(["inlet1"])
    assert locns == [["inlet1", ["inlet1"]]]

    all_bcs = solver1.setup.boundary_conditions
    locns = _locn_names_and_objs(all_bcs)
    assert locns == [
        ["interior--fluid", all_bcs],
        ["outlet", all_bcs],
        ["inlet1", all_bcs],
        ["inlet2", all_bcs],
        ["wall", all_bcs],
    ]

    locns = _locn_names_and_objs([all_bcs["inlet1"]])
    assert locns == [["inlet1", all_bcs["inlet1"]]]

    all_bcs = solver1.setup.boundary_conditions
    all_bcs2 = solver2.setup.boundary_conditions
    locns = _locn_names_and_objs([all_bcs, all_bcs2])
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

    assert solver.reduction.area(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
        ctxt=solver,
    )

    assert solver.reduction.area(locations=["inlet1"], ctxt=solver)


def _test_area_average(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions[
        "test_expr_1"
    ].definition = "AreaAve(AbsolutePressure, ['inlet1'])"
    expr_val = solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0
    val = solver.reduction.area_average(
        expression="AbsolutePressure",
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
    result = solver1.reduction.minimum(
        expression=test_expr1.definition(),
        locations=[
            solver1.setup.boundary_conditions["outlet"],
            solver2.setup.boundary_conditions["outlet"],
        ],
    )
    # assert result == expected_result
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
    red_val_1 = solver.reduction.count(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]]
    )
    red_val_2 = solver.reduction.count(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet2"]]
    )
    red_val_3 = solver.reduction.count(
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
    red_val_1 = solver.reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]]
    )
    red_val_2 = solver.reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet2"]]
    )
    red_val_3 = solver.reduction.centroid(
        locations=[solver.setup.boundary_conditions.velocity_inlet]
    )
    assert [red_val_1.x, red_val_1.y, red_val_1.z] == expr_val_1
    assert [red_val_2.x, red_val_2.y, red_val_2.z] == expr_val_2
    assert [red_val_3.x, red_val_3.y, red_val_3.z] == expr_val_3
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

    red_val_1 = solver1.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver1.setup.boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_2 = solver1.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver1.setup.boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_3 = solver1.reduction.area_integral(
        expression="AbsolutePressure",
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

    red_val_4 = solver2.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_5 = solver2.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_6 = solver2.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2.setup.boundary_conditions.velocity_inlet],
    )

    assert red_val_4 == expr_val_4
    assert red_val_5 == expr_val_5
    assert red_val_6 == expr_val_6

    red_val_7 = solver2.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[
            solver1.setup.boundary_conditions.velocity_inlet,
            solver2.setup.boundary_conditions.velocity_inlet,
        ],
    )

    assert red_val_7 - (expr_val_3 + expr_val_6) <= 0.000000001

    solver1.setup.named_expressions.pop(key="test_expr_1")


def _test_error_handling(solver):
    with pytest.raises(RuntimeError) as msg:
        solver.reduction.area_average(
            expression="AbsoluteVelocity",  # This is a wrong expression intentionally passed
            locations=solver.setup.boundary_conditions.velocity_inlet,
        )

    assert (
        msg.value.args[0]
        == "The last request could not be completed because there is error in server."
    )


def _test_force(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = "Force(['wall'])"
    expr_val_1 = solver.setup.named_expressions["test_expr_1"].get_value()

    red_total_force = solver.reduction.force(
        locations=[solver.setup.boundary_conditions.wall]
    )
    red_pressure_force = solver.reduction.pressure_force(locations=["wall"])
    red_viscous_force = solver.reduction.viscous_force(
        locations=[solver.setup.boundary_conditions.wall]
    )

    assert [red_total_force.x, red_total_force.y, red_total_force.z] == expr_val_1

    assert red_pressure_force.x + red_viscous_force.x == red_total_force.x

    assert red_pressure_force.y + red_viscous_force.y == red_total_force.y

    assert red_pressure_force.z + red_viscous_force.z == red_total_force.z

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

    red_moment_force = solver.reduction.moment(
        expression="Force(['wall'])", locations=[solver.setup.boundary_conditions.wall]
    )

    red_moment_location = solver.reduction.moment(
        expression="['inlet1']",
        locations=[solver.setup.boundary_conditions.wall],
    )

    assert [red_moment_force.x, red_moment_force.y, red_moment_force.z] == expr_val_1
    assert [
        red_moment_location.x,
        red_moment_location.y,
        red_moment_location.z,
    ] == expr_val_2

    solver.setup.named_expressions.pop(key="test_expr_1")


@pytest.mark.dev
@pytest.mark.fluent_232
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
