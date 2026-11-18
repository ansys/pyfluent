import copy
import json
from importlib.resources import files

import pytest
from jsonschema import Draft202012Validator

from fvm import (
    CaseValidationError,
    MovingWall,
    NoSlipWall,
    PythonFVMBackend,
    load_case_file,
    parse_case_definition,
    validate_case_document,
)

def _sample_document() -> dict[str, object]:
    with open("cases/lid_driven_cavity_re100.json", encoding="utf-8") as case_file:
        return json.load(case_file)


def test_packaged_schema_is_valid_and_sample_file_loads() -> None:
    schema_path = files("fvm").joinpath("schemas", "case-v1.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    case = load_case_file("cases/lid_driven_cavity_re100.json")

    assert case.schema_version == "1.0"
    assert case.case_id == "lid_driven_cavity_re100"
    assert case.nx == case.ny == 16
    assert case.density == 1.0
    assert case.dynamic_viscosity == 0.01
    assert case.boundary_for("north").boundary_type == "moving_wall"


def test_case_mapping_round_trips_and_maps_solver_objects() -> None:
    definition = parse_case_definition(_sample_document())
    round_tripped = parse_case_definition(definition.to_mapping())
    prepared = PythonFVMBackend().prepare(definition)

    assert round_tripped == definition
    assert prepared.mesh.nx == 16
    assert prepared.mesh.width == 1.0
    assert prepared.initial_velocity.u.values.shape == (16, 17)
    assert prepared.initial_velocity.v.values.shape == (17, 16)
    assert prepared.initial_pressure.values.shape == (16, 16)
    assert prepared.boundary_conditions.get("velocity", "west") == NoSlipWall()
    assert prepared.boundary_conditions.get("velocity", "north") == MovingWall((1.0, 0.0))
    assert prepared.solver.max_steps == 3
    assert prepared.solver.density == 1.0


def test_backend_runs_case_file_and_writes_stable_outputs(tmp_path) -> None:
    backend = PythonFVMBackend()

    run = backend.run_file(
        "cases/lid_driven_cavity_re100.json",
        output_directory=tmp_path / "backend-run",
    )

    assert run.case_id == "lid_driven_cavity_re100"
    assert not run.simulation.converged
    assert run.summary["result_format_version"] == "1.0"
    assert run.summary["reynolds_number"] == pytest.approx(100.0)
    assert run.summary["status"] == "not_converged"
    assert run.artifact_directory == tmp_path / "backend-run"
    assert (run.artifact_directory / "case.json").exists()
    assert (run.artifact_directory / "summary.json").exists()
    assert (run.artifact_directory / "fields.npz").exists()
    assert (run.artifact_directory / "history.csv").exists()
    assert json.loads((run.artifact_directory / "summary.json").read_text())["case_id"] == run.case_id


def test_backend_forwards_step_observer_for_each_projection_step() -> None:
    document = _sample_document()
    document["solver"]["max_steps"] = 2
    document["solver"]["velocity_tolerance_m_s"] = 1e-14
    observed: list[tuple[int, tuple[int, int], tuple[int, int]]] = []

    def observe(diagnostics, velocity, pressure) -> None:
        observed.append(
            (diagnostics.step, velocity.u.values.shape, pressure.values.shape)
        )

    run = PythonFVMBackend().run(document, step_observer=observe)

    assert len(observed) == run.simulation.steps
    assert [entry[0] for entry in observed] == list(range(1, run.simulation.steps + 1))
    assert all(entry[1:] == ((16, 17), (16, 16)) for entry in observed)


@pytest.mark.parametrize(
    ("mutate", "expected_path"),
    [
        (lambda case: case.pop("mesh"), "/mesh"),
        (lambda case: case.update(schema_version="2.0"), "/schema_version"),
        (lambda case: case.update(extra_setting=True), "/extra_setting"),
        (lambda case: case["physics"].update(model="compressible"), "/physics/model"),
        (lambda case: case["mesh"].update(type="unstructured"), "/mesh/type"),
        (lambda case: case["boundary_conditions"].update(west={"type": "velocity_inlet"}), "/boundary_conditions/west"),
        (lambda case: case["solver"].update(max_steps=0), "/solver/max_steps"),
    ],
)
def test_schema_rejects_missing_unknown_or_unsupported_inputs(mutate, expected_path) -> None:
    document = copy.deepcopy(_sample_document())
    mutate(document)

    with pytest.raises(CaseValidationError) as error:
        validate_case_document(document)

    assert expected_path in str(error.value)


def test_semantic_validation_rejects_incompatible_wall_and_time_step_values() -> None:
    non_tangent = copy.deepcopy(_sample_document())
    non_tangent["boundary_conditions"]["west"] = {
        "type": "moving_wall",
        "velocity_m_s": [0.1, 0.0],
    }
    with pytest.raises(CaseValidationError, match="wall-normal velocity"):
        validate_case_document(non_tangent)

    invalid_time_step = copy.deepcopy(_sample_document())
    invalid_time_step["solver"]["minimum_time_step_s"] = 0.01
    with pytest.raises(CaseValidationError, match="must not exceed"):
        validate_case_document(invalid_time_step)


def test_parser_rejects_non_finite_json_values() -> None:
    document = _sample_document()
    document["domain"]["width_m"] = float("nan")

    with pytest.raises(CaseValidationError, match="must be finite"):
        parse_case_definition(document)


def test_loader_reports_invalid_json_and_missing_files(tmp_path) -> None:
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{not json", encoding="utf-8")

    with pytest.raises(CaseValidationError, match="invalid JSON"):
        load_case_file(invalid_json)
    with pytest.raises(CaseValidationError, match="cannot read case file"):
        load_case_file(tmp_path / "missing.json")