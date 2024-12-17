import numpy as np
import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.examples.downloads import download_file


@pytest.mark.fluent_version(">=23.2")
def test_solution_variables(new_solver_session):
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    examples.download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")

    solution_variable_info = solver.fields.solution_variable_info
    solution_variable_data = solver.fields.solution_variable_data
    assert solution_variable_info == solver.svar_info
    assert solution_variable_data == solver.svar_data

    solver.file.read_case_data(file_name=import_file_name)

    zones_info = solution_variable_info.get_zones_info()

    assert zones_info.domains == ["mixture"]

    assert set(zones_info.zones) == {
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
        "interior--elbow-fluid",
    }

    zone_info = zones_info["wall-inlet"]

    assert zone_info.name == "wall-inlet"

    assert zone_info.count == 268

    assert zone_info.zone_id == 33

    assert zone_info.zone_type == "wall"

    wall_fluid_info = solution_variable_info.get_variables_info(
        zone_names=["wall-elbow", "elbow-fluid"], domain_name="mixture"
    )

    assert set(wall_fluid_info.solution_variables) == {
        "SV_ADS_0",
        "SV_ADS_1",
        "SV_CENTROID",
        "SV_H",
        "SV_K",
        "SV_O",
        "SV_P",
        "SV_T",
        "SV_U",
        "SV_V",
        "SV_W",
    }

    solution_variable_info_centroid = wall_fluid_info["SV_CENTROID"]

    assert solution_variable_info_centroid.name == "SV_CENTROID"

    assert solution_variable_info_centroid.dimension == 3

    assert solution_variable_info_centroid.field_type == np.float64

    sv_p_wall_fluid = solution_variable_data.get_data(
        solution_variable_name="SV_P",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )
    assert sv_p_wall_fluid.domain == "mixture"

    assert sv_p_wall_fluid.zones == ["wall-elbow", "elbow-fluid"]

    fluid_temp = sv_p_wall_fluid["elbow-fluid"]
    assert fluid_temp.size == 17822
    assert str(fluid_temp.dtype) == "float64"

    wall_press_array = solution_variable_data.create_empty_array(
        "SV_P", "wall-elbow", "mixture"
    )
    fluid_press_array = solution_variable_data.create_empty_array(
        "SV_P", "elbow-fluid", "mixture"
    )
    wall_press_array[:] = 500
    fluid_press_array[:] = 600
    zone_names_to_solution_variable_data = {
        "wall-elbow": wall_press_array,
        "elbow-fluid": fluid_press_array,
    }
    solution_variable_data.set_data(
        solution_variable_name="SV_P",
        zone_names_to_solution_variable_data=zone_names_to_solution_variable_data,
        domain_name="mixture",
    )

    updated_sv_p_data = solution_variable_data.get_data(
        solution_variable_name="SV_P",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )

    assert updated_sv_p_data.domain == "mixture"
    assert updated_sv_p_data.zones == ["wall-elbow", "elbow-fluid"]

    assert updated_sv_p_data["elbow-fluid"].size == 17822
    assert str(updated_sv_p_data["elbow-fluid"].dtype) == "float64"

    assert updated_sv_p_data["wall-elbow"][0] == 500.0
    assert updated_sv_p_data["elbow-fluid"][-1] == 600.0


@pytest.mark.fluent_version(">=23.2")
def test_solution_variables_single_precision(new_solver_session_sp):
    solver = new_solver_session_sp
    import_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    examples.download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")

    solution_variable_info = solver.fields.solution_variable_info
    solution_variable_data = solver.fields.solution_variable_data
    assert solution_variable_info == solver.svar_info
    assert solution_variable_data == solver.svar_data

    solver.file.read_case_data(file_name=import_file_name)

    zones_info = solution_variable_info.get_zones_info()

    assert zones_info.domains == ["mixture"]

    assert set(zones_info.zones) == {
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
        "interior--elbow-fluid",
    }

    zone_info = zones_info["wall-elbow"]

    assert zone_info.name == "wall-elbow"

    assert zone_info.count == 2168

    assert zone_info.zone_id == 34

    assert zone_info.zone_type == "wall"

    wall_fluid_info = solution_variable_info.get_variables_info(
        zone_names=["wall-elbow", "elbow-fluid"], domain_name="mixture"
    )

    assert set(wall_fluid_info.solution_variables) == {
        "SV_ADS_0",
        "SV_ADS_1",
        "SV_CENTROID",
        "SV_H",
        "SV_K",
        "SV_O",
        "SV_P",
        "SV_T",
        "SV_U",
        "SV_V",
        "SV_W",
    }

    solution_variable_info_centroid = wall_fluid_info["SV_CENTROID"]

    assert solution_variable_info_centroid.name == "SV_CENTROID"

    assert solution_variable_info_centroid.dimension == 3

    assert solution_variable_info_centroid.field_type == np.float32

    sv_p_wall_fluid = solution_variable_data.get_data(
        solution_variable_name="SV_P",
        zone_names=["wall-elbow", "elbow-fluid"],
        domain_name="mixture",
    )
    assert sv_p_wall_fluid.domain == "mixture"

    assert sv_p_wall_fluid.zones == ["wall-elbow", "elbow-fluid"]

    fluid_temp = sv_p_wall_fluid["elbow-fluid"]
    assert fluid_temp.size == 17822
    assert str(fluid_temp.dtype) == "float32"


@pytest.mark.fluent_version(">=24.2")
def test_solution_variable_does_not_modify_case(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file.read_case_data(file_name=case_path)
    solver.scheme_eval.scheme_eval("(%save-case-id)")
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")
    solver.fields.solution_variable_data.get_data(
        solution_variable_name="SV_P",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")


@pytest.mark.fluent_version(">=25.2")
def test_solution_variable_udm_data(mixing_elbow_case_session_t4):
    solver = mixing_elbow_case_session_t4
    solver.tui.define.user_defined.user_defined_memory("2")
    solver.settings.solution.initialization.hybrid_initialize()
    solver.settings.solution.run_calculation.iterate(iter_count=1)
    udm_data = solver.fields.solution_variable_data.get_data(
        solution_variable_name="SV_UDM_I",
        domain_name="mixture",
        zone_names=["wall-elbow"],
    )["wall-elbow"]
    np.testing.assert_array_equal(udm_data, np.zeros(4336))
    udm_data[:2168] = 5
    udm_data[2168:] = 10
    solver.fields.solution_variable_data.set_data(
        solution_variable_name="SV_UDM_I",
        domain_name="mixture",
        zone_names_to_solution_variable_data={"wall-elbow": udm_data},
    )
    new_array = solver.fields.solution_variable_data.get_data(
        solution_variable_name="SV_UDM_I",
        domain_name="mixture",
        zone_names=["wall-elbow"],
    )["wall-elbow"]
    np.testing.assert_array_equal(new_array, udm_data)
