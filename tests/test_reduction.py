import pytest

from ansys.fluent.core.services.reduction import _locn_names_and_objs
from tests.conftest import static_mixer_case_session


def _test_locn_extraction(solver1, solver2):
    solver1_boundary_conditions = solver1.setup.boundary_conditions
    solver2_boundary_conditions = solver2.setup.boundary_conditions
    locns = _locn_names_and_objs(["inlet1"])
    assert locns == [["inlet1", ["inlet1"]]]

    all_bcs = solver1_boundary_conditions
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

    all_bcs = solver1_boundary_conditions
    all_bcs2 = solver2_boundary_conditions
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

    assert solver.fields.reduction.area(
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
        ctxt=solver,
    )

    assert solver.fields.reduction.area(locations=["inlet1"], ctxt=solver)


def _test_area_average(solver):
    solver.solution.initialization.hybrid_initialize()
    solver_named_expressions = solver.setup.named_expressions
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = (
        "AreaAve(AbsolutePressure, ['inlet1'])"
    )
    expr_val = solver_named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0
    val = solver.fields.reduction.area_average(
        expression="AbsolutePressure",
        locations=solver.setup.boundary_conditions.velocity_inlet,
    )
    assert val == expr_val
    solver_named_expressions.pop(key="test_expr_1")


def _test_min(solver1, solver2):
    solver1.solution.initialization.hybrid_initialize()
    solver2.solution.initialization.hybrid_initialize()
    solver1_named_expr = solver1.setup.named_expressions
    solver1_named_expr["test_expr_1"] = {}
    test_expr1 = solver1_named_expr["test_expr_1"]
    test_expr1.definition = "sqrt(VelocityMagnitude)"
    solver2_named_expr = solver2.setup.named_expressions
    solver2_named_expr["test_expr_2"] = {}
    test_expr2 = solver2_named_expr["test_expr_2"]
    test_expr2.definition = "minimum(test_expr_2, ['outlet'])"
    expected_result = test_expr2.get_value()
    result = solver1.fields.reduction.minimum(
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
    solver_named_expressions = solver.setup.named_expressions
    s_velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = "Count(['inlet1'])"
    expr_val_1 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = "Count(['inlet2'])"
    expr_val_2 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = "Count(['inlet1', 'inlet2'])"
    expr_val_3 = solver_named_expressions["test_expr_1"].get_value()
    assert expr_val_3 == expr_val_1 + expr_val_2
    red_val_1 = solver.fields.reduction.count(locations=[s_velocity_inlet["inlet1"]])
    red_val_2 = solver.fields.reduction.count(locations=[s_velocity_inlet["inlet2"]])
    red_val_3 = solver.fields.reduction.count(locations=[s_velocity_inlet])
    assert red_val_1 == expr_val_1
    assert red_val_2 == expr_val_2
    assert red_val_3 == expr_val_3
    solver_named_expressions.pop(key="test_expr_1")


def _test_count_if(solver):
    solver.solution.initialization.hybrid_initialize()
    solver_named_expressions = solver.setup.named_expressions
    s_velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = (
        "CountIf(AbsolutePressure > 0[Pa], ['inlet1'])"
    )
    expr_val_1 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = (
        "CountIf(AbsolutePressure > 0[Pa], ['inlet2'])"
    )
    expr_val_2 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = (
        "CountIf(AbsolutePressure > 0[Pa], ['inlet1', 'inlet2'])"
    )
    expr_val_3 = solver_named_expressions["test_expr_1"].get_value()
    assert expr_val_3 == expr_val_1 + expr_val_2
    red_val_1 = solver.fields.reduction.count_if(
        condition="AbsolutePressure > 0[Pa]", locations=["inlet1"]
    )
    red_val_2 = solver.fields.reduction.count_if(
        condition="AbsolutePressure > 0[Pa]", locations=[s_velocity_inlet["inlet2"]]
    )
    red_val_3 = solver.fields.reduction.count_if(
        condition="AbsolutePressure > 0[Pa]", locations=[s_velocity_inlet]
    )
    assert red_val_1 == expr_val_1
    assert red_val_2 == expr_val_2
    assert red_val_3 == expr_val_3
    solver_named_expressions.pop(key="test_expr_1")


def _test_centroid(solver):
    solver.solution.initialization.hybrid_initialize()
    solver_named_expressions = solver.setup.named_expressions
    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = "Centroid(['inlet1'])"
    expr_val_1 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = "Centroid(['inlet2'])"
    expr_val_2 = solver_named_expressions["test_expr_1"].get_value()
    solver_named_expressions["test_expr_1"].definition = (
        "Centroid(['inlet1', 'inlet2'])"
    )
    expr_val_3 = solver_named_expressions["test_expr_1"].get_value()
    red_val_1 = solver.fields.reduction.centroid(locations=[velocity_inlet["inlet1"]])
    red_val_2 = solver.fields.reduction.centroid(locations=[velocity_inlet["inlet2"]])
    red_val_3 = solver.fields.reduction.centroid(locations=[velocity_inlet])
    assert [red_val_1[0], red_val_1[1], red_val_1[2]] == expr_val_1
    assert [red_val_2[0], red_val_2[1], red_val_2[2]] == expr_val_2
    assert [red_val_3[0], red_val_3[1], red_val_3[2]] == expr_val_3
    solver_named_expressions.pop(key="test_expr_1")


def _test_area_integrated_average(solver1, solver2):
    solver1.solution.initialization.hybrid_initialize()
    solver2.solution.initialization.hybrid_initialize()
    solver1_boundary_conditions = solver1.setup.boundary_conditions
    solver2_boundary_conditions = solver2.setup.boundary_conditions
    solver1_named_expr = solver1.setup.named_expressions
    solver2_named_expr = solver2.setup.named_expressions

    solver1_named_expr["test_expr_1"] = {}
    solver1_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet1'])"
    )
    expr_val_1 = solver1_named_expr["test_expr_1"].get_value()

    solver1_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet2'])"
    )
    expr_val_2 = solver1_named_expr["test_expr_1"].get_value()
    solver1_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet1', 'inlet2'])"
    )
    expr_val_3 = solver1_named_expr["test_expr_1"].get_value()

    assert expr_val_3 - (expr_val_1 + expr_val_2) <= 0.000000001

    red_val_1 = solver1.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver1_boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_2 = solver1.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver1_boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_3 = solver1.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver1_boundary_conditions.velocity_inlet],
    )

    assert red_val_1 == expr_val_1
    assert red_val_2 == expr_val_2
    assert red_val_3 == expr_val_3

    solver2_named_expr["test_expr_1"] = {}
    solver2_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet1'])"
    )
    expr_val_4 = solver2_named_expr["test_expr_1"].get_value()

    solver2_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet2'])"
    )
    expr_val_5 = solver2_named_expr["test_expr_1"].get_value()
    solver2_named_expr["test_expr_1"].definition = (
        "AreaInt(AbsolutePressure, ['inlet1', 'inlet2'])"
    )
    expr_val_6 = solver2_named_expr["test_expr_1"].get_value()

    assert expr_val_6 - (expr_val_4 + expr_val_5) <= 0.000000001

    red_val_4 = solver2.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2_boundary_conditions.velocity_inlet["inlet1"]],
    )
    red_val_5 = solver2.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2_boundary_conditions.velocity_inlet["inlet2"]],
    )
    red_val_6 = solver2.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[solver2_boundary_conditions.velocity_inlet],
    )

    assert red_val_4 == expr_val_4
    assert red_val_5 == expr_val_5
    assert red_val_6 == expr_val_6

    red_val_7 = solver2.fields.reduction.area_integral(
        expression="AbsolutePressure",
        locations=[
            solver1_boundary_conditions.velocity_inlet,
            solver2_boundary_conditions.velocity_inlet,
        ],
    )

    assert red_val_7 - (expr_val_3 + expr_val_6) <= 0.000000001

    solver1_named_expr.pop(key="test_expr_1")


def _test_error_handling(solver):
    if int(solver._version) < 241:
        with pytest.raises(RuntimeError) as msg:
            solver.fields.reduction.area_average(
                expression="AbsoluteVelocity",  # This is a wrong expression intentionally passed
                locations=solver.setup.boundary_conditions.velocity_inlet,
            )


def _test_force(solver):
    solver.solution.initialization.hybrid_initialize()
    solver_named_expressions = solver.setup.named_expressions
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = "Force(['wall'])"
    expr_val_1 = solver_named_expressions["test_expr_1"].get_value()

    red_total_force = solver.fields.reduction.force(
        locations=[solver.setup.boundary_conditions.wall]
    )
    red_pressure_force = solver.fields.reduction.pressure_force(
        locations=[solver.setup.boundary_conditions.wall]
    )
    red_viscous_force = solver.fields.reduction.viscous_force(
        locations=[solver.setup.boundary_conditions.wall]
    )

    assert [red_total_force[0], red_total_force[1], red_total_force[2]] == expr_val_1

    assert red_pressure_force[0] + red_viscous_force[0] == red_total_force[0]

    assert red_pressure_force[1] + red_viscous_force[1] == red_total_force[1]

    assert red_pressure_force[2] + red_viscous_force[2] == red_total_force[2]

    solver_named_expressions.pop(key="test_expr_1")


def _test_moment(solver):
    solver.solution.initialization.hybrid_initialize()
    solver_named_expressions = solver.setup.named_expressions
    location = solver.setup.boundary_conditions.wall
    solver_named_expressions["test_expr_1"] = {}
    solver_named_expressions["test_expr_1"].definition = (
        "Moment(Force(['wall']),['wall'])"
    )
    expr_val_1 = solver_named_expressions["test_expr_1"].get_value()

    solver_named_expressions["test_expr_1"].definition = "Moment(['inlet1'],['wall'])"
    expr_val_2 = solver_named_expressions["test_expr_1"].get_value()

    red_moment_force = solver.fields.reduction.moment(
        expression="Force(['wall'])", locations=[location]
    )

    red_moment_location = solver.fields.reduction.moment(
        expression="['inlet1']", locations=[location]
    )

    assert [red_moment_force[0], red_moment_force[1], red_moment_force[2]] == expr_val_1
    assert [
        red_moment_location[0],
        red_moment_location[1],
        red_moment_location[2],
    ] == expr_val_2

    solver_named_expressions.pop(key="test_expr_1")


def _test_sum(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = (
        "Sum(AbsolutePressure, ['inlet1'], Weight=Area)"
    )
    expr_val = solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0

    val = solver.fields.reduction.sum(
        expression="AbsolutePressure",
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
        weight="Area",
    )

    assert val == expr_val
    solver.setup.named_expressions.pop(key="test_expr_1")


def _test_sum_if(solver):
    solver.solution.initialization.hybrid_initialize()
    solver.setup.named_expressions["test_expr_1"] = {}
    solver.setup.named_expressions["test_expr_1"].definition = (
        "SumIf(AbsolutePressure, AbsolutePressure > 0[Pa], ['inlet1'], Weight=Area)"
    )
    expr_val = solver.setup.named_expressions["test_expr_1"].get_value()
    assert type(expr_val) == float and expr_val != 0.0

    val = solver.fields.reduction.sum_if(
        expression="AbsolutePressure",
        condition="AbsolutePressure > 0[Pa]",
        locations=[solver.setup.boundary_conditions.velocity_inlet["inlet1"]],
        weight="Area",
    )

    assert val == expr_val
    solver.setup.named_expressions.pop(key="test_expr_1")


static_mixer_case_session2 = static_mixer_case_session


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_reductions(static_mixer_case_session, static_mixer_case_session2) -> None:
    solver1 = static_mixer_case_session
    solver2 = static_mixer_case_session2
    _test_context(solver1)
    _test_locn_extraction(solver1, solver2)
    _test_area_average(solver1)
    _test_min(solver1, solver2)
    _test_count(solver1)
    _test_count_if(solver1)
    _test_centroid(solver1)
    _test_area_integrated_average(solver1, solver2)
    _test_error_handling(solver1)
    _test_force(solver1)
    _test_moment(solver1)
    _test_sum(solver1)
    _test_sum_if(solver1)


@pytest.mark.fluent_version(">=24.2")
def test_reduction_does_not_modify_case(static_mixer_case_session):
    solver = static_mixer_case_session
    # After reading the static-mixer case in Fluent, case-modifed? flag is somehow True
    solver.scheme_eval.scheme_eval("(%save-case-id)")
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")
    solver.reduction.area_average(
        expression="AbsolutePressure",
        locations=solver.setup.boundary_conditions.velocity_inlet,
    )
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")


@pytest.mark.skip("https://github.com/ansys/pyfluent/issues/2998")
@pytest.mark.fluent_version(">=24.2")
def test_fix_for_invalid_location_inputs(static_mixer_case_session):
    solver = static_mixer_case_session
    solver.solution.initialization.hybrid_initialize()

    assert solver.fields.reduction.area(locations=["inlet1"], ctxt=solver)

    with pytest.raises(ValueError):
        assert solver.fields.reduction.area(locations=["inlet-1"], ctxt=solver)

    with pytest.raises(KeyError):
        assert solver.fields.reduction.area(
            locations=[solver.setup.boundary_conditions.velocity_inlet["inlet-1"]]
        )

    assert solver.fields.reduction.area(locations=["inlet1"])

    with pytest.raises(ValueError):
        assert solver.fields.reduction.area(locations=["inlet-1"])
