import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read(
        file_name=case_path, file_type="case", lightweight_setup=True
    )
    # NOTE: Not sure why initialization is necessary here
    # solver_session.solution.initialization.hybrid_initialize()

    viscous_model = solver_session.setup.models.viscous

    assert viscous_model.model() == "k-epsilon"
    assert "inviscid" in viscous_model.model.get_attr("allowed-values")
    viscous_model.model = "inviscid"

    assert viscous_model.model() == "inviscid"


@pytest.mark.nightly
@pytest.mark.fluent_version(">=24.1")
def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)
    boundary_conditions = solver.setup.boundary_conditions
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 15}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 5}}},
    }
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity.value() == {
        "inlet2": {"momentum": {"velocity": {"value": 15}}},
        "inlet1": {"momentum": {"velocity": {"value": 5}}},
    }
    boundary_conditions.velocity_inlet["inl*"].momentum.velocity = 10
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
    }
    boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
        "inl*"
    ].momentum.velocity()
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
    }
    cell_zone_conditions = solver.setup.cell_zone_conditions
    assert cell_zone_conditions.fluid["*"].source_terms.source_terms["*mom*"]() == {
        "fluid": {
            "source_terms": {
                "source_terms": {
                    "x-momentum": [{"option": "value", "value": 1}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 3}],
                }
            }
        }
    }
    cell_zone_conditions.fluid["*"].source_terms.source_terms["*mom*"] = [
        {"option": "value", "value": 2}
    ]
    assert cell_zone_conditions.fluid["*"].source_terms.source_terms["*mom*"]() == {
        "fluid": {
            "source_terms": {
                "source_terms": {
                    "x-momentum": [{"option": "value", "value": 2}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 2}],
                }
            }
        }
    }


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_wildcard_fnmatch(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    mesh = solver.results.graphics.mesh
    mesh.create("mesh-2")
    mesh.create("mesh-a")
    mesh.create("mesh-bc")

    assert sorted(mesh["mesh-*"]()) == sorted(["mesh-1", "mesh-2", "mesh-a", "mesh-bc"])

    assert list(mesh["mesh-?c"]().keys()) == ["mesh-bc"]

    assert list(mesh["mesh-[2-5]"]().keys()) == ["mesh-2"]

    assert sorted(mesh["mesh-[!2-5]"]()) == sorted(["mesh-1", "mesh-a"])


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)

    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    assert [x for x in velocity_inlet] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*let*"]] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*1*"]] == ["inlet1"]

    test_data = []
    for k, v in velocity_inlet.items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"

    test_data = []
    for k, v in velocity_inlet["*let*"].items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"


@pytest.mark.fluent_version(">=23.1")
def test_api_upgrade(new_solver_session, capsys):
    solver = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.tui.file.read_case(case_path)
    "<solver_session>.file.read_case" in capsys.readouterr().out
