import numpy as np
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples


def test_svars(new_solver_session):
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_filename)

    svar_info = solver.svar_info
    svar_data = solver.svar_data

    zones_info = svar_info.get_zones_info()

    assert zones_info.domains == ["mixture"]

    assert zones_info.zones == [
        "symmetry-xyplane",
        "hot-inlet",
        "cold-inlet",
        "outlet",
        "wall-inlet",
        "wall-elbow",
        "elbow-fluid",
        "interior--elbow-fluid",
    ]

    zone_info = zones_info["wall-inlet"]

    assert zone_info.name == "wall-inlet"

    assert zone_info.count == 268

    assert zone_info.zone_id == 33

    assert zone_info.zone_type == "wall"

    svars_info_wall_fluid = svar_info.get_svars_info(
        zone_names=["wall-elbow", "elbow-fluid"], domain_name="mixture"
    )

    assert svars_info_wall_fluid.svars == ["SV_CENTROID"]

    svar_info_centroid = svars_info_wall_fluid["SV_CENTROID"]

    assert svar_info_centroid.name == "SV_CENTROID"

    assert svar_info_centroid.dimension == 3

    assert svar_info_centroid.field_type == np.float64

    sv_t_wall_fluid = svar_data.get_svar_data(
        svar_name="SV_CENTROID",
        zone_names=["elbow-fluid", "wall-elbow"],
        domain_name="mixture",
    )
    assert sv_t_wall_fluid.domain == "mixture"

    assert sv_t_wall_fluid.zones == ["wall-elbow", "elbow-fluid"]

    fluid_temp = sv_t_wall_fluid["elbow-fluid"]
    assert fluid_temp.size == 53466
    assert fluid_temp.dtype == float

    wall_temp_array = svar_data.get_array("SV_CENTROID", "wall-elbow", "mixture")
    fluid_temp_array = svar_data.get_array("SV_CENTROID", "elbow-fluid", "mixture")
    wall_temp_array[:] = 500
    fluid_temp_array[:] = 600
    zone_names_to_svar_data = {
        "wall-elbow": wall_temp_array,
        "elbow-fluid": fluid_temp_array,
    }
    svar_data.set_svar_data(
        svar_name="SV_CENTROID",
        zone_names_to_svar_data=zone_names_to_svar_data,
        domain_name="mixture",
    )
