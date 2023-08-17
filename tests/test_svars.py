import numpy as np
import pytest
from util.solver_workflow import (  # noqa: F401
    new_solver_session,
    new_solver_session_single_precision,
)

from ansys.fluent.core import examples


@pytest.mark.fluent_version(">=23.2")
def test_svars(new_solver_session):
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_filename)

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=10)

    svar_info = solver.svar_info
    svar_data = solver.svar_data

    zones_info = svar_info.get_zones_info()

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

    svars_info_wall_fluid = svar_info.get_svars_info(
        zone_names=["wall-elbow", "elbow-fluid"], domain_name="mixture"
    )

    assert set(svars_info_wall_fluid.svars) == {
        "SV_ADS_1",
        "SV_CENTROID",
        "SV_H",
        "SV_K",
        "SV_O",
        "SV_T",
        "SV_P",
        "SV_U",
        "SV_V",
        "SV_W",
    }

    svar_info_centroid = svars_info_wall_fluid["SV_CENTROID"]

    assert svar_info_centroid.name == "SV_CENTROID"

    assert svar_info_centroid.dimension == 3

    assert svar_info_centroid.field_type == np.float64

    sv_p_wall_fluid = svar_data.get_svar_data(
        svar_name="SV_P",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )
    assert sv_p_wall_fluid.domain == "mixture"

    assert sv_p_wall_fluid.zones == ["wall-elbow", "elbow-fluid"]

    fluid_temp = sv_p_wall_fluid["elbow-fluid"]
    assert fluid_temp.size == 17822
    assert str(fluid_temp.dtype) == "float64"

    wall_press_array = svar_data.get_array("SV_P", "wall-elbow", "mixture")
    fluid_press_array = svar_data.get_array("SV_P", "elbow-fluid", "mixture")
    wall_press_array[:] = 500
    fluid_press_array[:] = 600
    zone_names_to_svar_data = {
        "wall-elbow": wall_press_array,
        "elbow-fluid": fluid_press_array,
    }
    svar_data.set_svar_data(
        svar_name="SV_P",
        zone_names_to_svar_data=zone_names_to_svar_data,
        domain_name="mixture",
    )

    updated_sv_p_data = svar_data.get_svar_data(
        svar_name="SV_P",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )

    assert updated_sv_p_data.domain == "mixture"
    assert updated_sv_p_data.zones == ["wall-elbow", "elbow-fluid"]

    assert updated_sv_p_data["elbow-fluid"].size == 17822
    assert str(updated_sv_p_data["elbow-fluid"].dtype) == "float64"

    assert updated_sv_p_data["wall-elbow"][0] == 500.0
    assert updated_sv_p_data["elbow-fluid"][-1] == 600.0


@pytest.mark.skip("Failing on latest Fluent v241 dev version, see #1902")
@pytest.mark.fluent_version(">=23.2")
def test_svars_single_precision(new_solver_session_single_precision):
    solver = new_solver_session_single_precision
    import_filename = examples.download_file(
        "vortex_init.cas.h5", "pyfluent/examples/Steady-Vortex-VOF"
    )
    solver.file.read(file_type="case", file_name=import_filename)

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=10)

    svar_info = solver.svar_info
    svar_data = solver.svar_data

    zones_info = svar_info.get_zones_info()

    assert zones_info.domains == ["water", "air", "mixture"]

    assert set(zones_info.zones) == {
        "mrf-tank",
        "tank_top",
        "wall_tank",
        "shaft_tank",
        "shaft_mrf",
        "wall_impeller",
        "mrf",
        "interior--mrf",
        "tank",
        "interior--tank",
    }

    zone_info = zones_info["wall_tank"]

    assert zone_info.name == "wall_tank"

    assert zone_info.count == 14921

    assert zone_info.zone_id == 27

    assert zone_info.zone_type == "wall"

    svars_info_wall_fluid = svar_info.get_svars_info(
        zone_names=["wall_tank", "tank"], domain_name="mixture"
    )

    assert set(svars_info_wall_fluid.svars) == {
        "SV_ADS_0",
        "SV_ADS_1",
        "SV_CENTROID",
        "SV_DENSITY",
        "SV_K",
        "SV_O",
        "SV_P",
        "SV_U",
        "SV_V",
        "SV_W",
    }

    svar_info_centroid = svars_info_wall_fluid["SV_CENTROID"]

    assert svar_info_centroid.name == "SV_CENTROID"

    assert svar_info_centroid.dimension == 3

    assert svar_info_centroid.field_type == np.float32

    sv_p_wall_fluid = svar_data.get_svar_data(
        svar_name="SV_P",
        zone_names=["wall_tank", "tank"],
        domain_name="air",
    )
    assert sv_p_wall_fluid.domain == "air"

    assert sv_p_wall_fluid.zones == ["wall_tank", "tank"]

    fluid_temp = sv_p_wall_fluid["tank"]
    assert fluid_temp.size == 183424
    assert str(fluid_temp.dtype) == "float32"
