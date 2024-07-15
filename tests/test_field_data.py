import numpy as np
import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.services.field_data import FieldUnavailable, SurfaceDataType

HOT_INLET_TEMPERATURE = 313.15


@pytest.mark.fluent_version(">=24.1")
def test_field_data(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.tui.mesh.check()

    solver.setup.models.energy.enabled = True
    solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
    solver.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

    # Set up boundary conditions for CFD analysis
    cold_inlet = solver.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    cold_inlet.momentum.velocity = 0.4
    cold_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
    cold_inlet.turbulence.turbulent_intensity = 0.05
    cold_inlet.turbulence.hydraulic_diameter = "4 [in]"
    cold_inlet.thermal.t = 293.15

    hot_inlet = solver.setup.boundary_conditions.velocity_inlet["hot-inlet"]
    hot_inlet.momentum.velocity = 1.2
    hot_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
    hot_inlet.turbulence.hydraulic_diameter = "1 [in]"
    hot_inlet.thermal.t = HOT_INLET_TEMPERATURE

    solver.tui.solve.monitors.residual.plot("no")

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    iterate = solver.solution.run_calculation.iterate
    iterate.get_attr("arguments")
    iterate(iter_count=10)

    # Get field data object
    field_data = solver.fields.field_data

    transaction = field_data.new_transaction()

    hot_inlet_surf_id = solver.fields.field_info.get_surfaces_info()["hot-inlet"][
        "surface_id"
    ][0]
    transaction.add_surfaces_request(
        surfaces=[1, hot_inlet_surf_id],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    transaction.add_scalar_fields_request(
        surfaces=[1, hot_inlet_surf_id],
        field_name="temperature",
        node_value=True,
        boundary_value=True,
    )
    transaction.add_pathlines_fields_request(
        surfaces=[1, hot_inlet_surf_id],
        field_name="temperature",
        provide_particle_time_field=True,
    )

    data = transaction.get_fields()

    surface_data_tag = (("type", "surface-data"),)  # tuple containing surface data info
    scalar_field_tag = (
        ("type", "scalar-field"),
        ("dataLocation", 0),
        ("boundaryValues", True),
    )  # tuple containing scalar field info
    pathline_tag = (("type", "pathlines-field"), ("field", "temperature"))
    assert len(data) == 3
    assert list(data[surface_data_tag][hot_inlet_surf_id].keys()) == [
        "vertices",
        "centroid",
    ]
    assert list(data[scalar_field_tag][hot_inlet_surf_id].keys()) == ["temperature"]
    temp_inlet_data = data[scalar_field_tag][hot_inlet_surf_id]["temperature"]
    assert (
        len(temp_inlet_data)
        == len(data[surface_data_tag][hot_inlet_surf_id]["vertices"]) / 3
    )
    assert round(float(np.average(temp_inlet_data)), 2) == HOT_INLET_TEMPERATURE
    assert sorted(list(data[pathline_tag][hot_inlet_surf_id].keys())) == sorted(
        [
            "vertices",
            "lines",
            "temperature",
            "pathlines-count",
            "particle-time",
        ]
    )

    # multiple surface *names* transaction
    transaction2 = field_data.new_transaction()
    fields_request = transaction2.add_scalar_fields_request
    surface_names = fields_request.surface_names.allowed_values()
    fields_request(surfaces=surface_names, field_name="temperature")
    data2 = transaction2.get_fields()
    assert data2


def test_field_data_allowed_values(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.fields.field_data
    field_info = solver.fields.field_info
    transaction = field_data.new_transaction()
    fields_request = transaction.add_scalar_fields_request

    assert [] == field_data.get_scalar_field_data.field_name.allowed_values()

    solver.file.read(file_type="case", file_name=import_file_name)

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    expected_allowed_args = sorted(field_info.get_scalar_fields_info())
    allowed_args = field_data.get_scalar_field_data.field_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    assert len(allowed_args) > len(allowed_args_no_init)
    allowed_args = fields_request.field_name.allowed_values()
    assert expected_allowed_args == allowed_args

    expected_allowed_args = sorted(field_info.get_surfaces_info())
    allowed_args = field_data.get_scalar_field_data.surface_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = fields_request.surface_names.allowed_values()
    assert expected_allowed_args == allowed_args

    expected_allowed_args = sorted(field_info.get_surfaces_info())
    allowed_args = field_data.get_surface_data.surface_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = fields_request.surface_names.allowed_values()
    assert expected_allowed_args == allowed_args

    allowed_args = field_data.get_surface_data.surface_ids.allowed_values()
    assert len(expected_allowed_args) == len(allowed_args)
    allowed_args = fields_request.surface_ids.allowed_values()
    assert len(expected_allowed_args) == len(allowed_args)

    expected_allowed_args = sorted(field_info.get_vector_fields_info())
    allowed_args = field_data.get_vector_field_data.field_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = transaction.add_vector_fields_request.field_name.allowed_values()
    assert expected_allowed_args == allowed_args


@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_3d(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.fields.field_data

    assert [] == field_data.get_scalar_field_data.field_name.allowed_values()

    solver.file.read(file_type="case", file_name=import_file_name)

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["cold-inlet"]
    )

    assert abs_press_data.size == 241
    assert abs_press_data[120].scalar_data == 101325.0

    vertices_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.Vertices], surfaces=["cold-inlet"]
    )
    assert round(float(vertices_data[5].x), 2) == -0.2

    faces_centroid_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesCentroid], surfaces=["cold-inlet"]
    )
    assert round(float(faces_centroid_data[5].y), 2) == -0.18

    faces_connectivity_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesConnectivity], surfaces=["cold-inlet"]
    )
    assert faces_connectivity_data[5].node_count == 4
    assert (faces_connectivity_data[5].node_indices == [12, 13, 17, 16]).all()

    faces_normal_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesNormal], surfaces=["cold-inlet"]
    )
    assert faces_normal_data.size == 152
    assert faces_normal_data.surface_id == 3

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surfaces=["cold-inlet"]
    )

    assert velocity_vector_data.size == 152
    assert velocity_vector_data.scale == 1.0

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity", surfaces=["cold-inlet"]
    )

    assert path_lines_data["vertices"].size == 76152
    assert path_lines_data["lines"].size == 76000
    assert path_lines_data["velocity"].size == 76152

    assert path_lines_data["lines"][100].node_count == 2
    assert all(path_lines_data["lines"][100].node_indices == [100, 101])


@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_2d(disk_case_session) -> None:
    solver = disk_case_session

    field_data = solver.fields.field_data

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["velocity-inlet-2"]
    )

    assert abs_press_data.size == 11
    assert abs_press_data[5].scalar_data == 101325.0

    vertices_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.Vertices], surfaces=["interior-4"]
    )
    assert round(float(vertices_data[5].x), 2) == 0.0

    faces_centroid_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesCentroid], surfaces=["velocity-inlet-2"]
    )
    assert round(float(faces_centroid_data[5].y), 2) == 0.02

    faces_connectivity_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesConnectivity], surfaces=["velocity-inlet-2"]
    )[5]
    assert faces_connectivity_data.node_count == 2
    assert (faces_connectivity_data.node_indices == [5, 6]).all()

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surfaces=["velocity-inlet-2"]
    )

    assert velocity_vector_data.size == 10
    assert velocity_vector_data.scale == 1.0

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity", surfaces=["velocity-inlet-2"]
    )

    assert path_lines_data["vertices"].size == 5010
    assert path_lines_data["lines"].size == 5000
    assert path_lines_data["velocity"].size == 5010

    assert path_lines_data["lines"][100].node_count == 2
    assert all(path_lines_data["lines"][100].node_indices == [100, 101])


def test_field_data_errors(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    with pytest.raises(DisallowedValuesError) as fne:
        solver.fields.field_data.get_scalar_field_data(
            field_name="y-face-area", surfaces=[0]
        )

    with pytest.raises(DisallowedValuesError) as fne:
        solver.fields.field_data.get_scalar_field_data(
            field_name="partition-neighbors", surfaces=[0]
        )

    solver.file.read(file_type="case", file_name=import_file_name)

    with pytest.raises(FieldUnavailable) as fnu:
        solver.fields.field_data.get_scalar_field_data(
            field_name="density", surfaces=[0]
        )

    y_face_area = solver.fields.field_data.get_scalar_field_data(
        field_name="y-face-area", surfaces=[0]
    )
    assert y_face_area and isinstance(y_face_area, dict)

    partition_neighbors = solver.fields.field_data.get_scalar_field_data(
        field_name="partition-neighbors", surfaces=[0]
    )
    assert partition_neighbors and isinstance(partition_neighbors, dict)

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    # Get field data object
    field_data = solver.fields.field_data

    with pytest.raises(DisallowedValuesError) as sne:
        solver.fields.field_data.get_scalar_field_data(
            field_name="density", surfaces=["bob"]
        )

    with pytest.raises(DisallowedValuesError) as fne:
        solver.fields.field_data.get_scalar_field_data(
            field_name="xdensity", surfaces=[0]
        )


@pytest.mark.fluent_version(">=23.2")
def test_field_info_validators(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.solution.initialization.hybrid_initialize()

    vector_field_1 = solver.fields.field_info.validate_vector_fields("velocity")
    assert vector_field_1 is None

    with pytest.raises(DisallowedValuesError) as vector_field_error:
        solver.fields.field_info.validate_vector_fields("relative-vel")

    scalar_field_1 = solver.fields.field_info.validate_scalar_fields("z-velocity")
    assert scalar_field_1 is None

    with pytest.raises(DisallowedValuesError) as scalar_field_error:
        solver.fields.field_info.validate_scalar_fields("z-vel")

    surface = solver.fields.field_info.validate_surfaces(["cold-inlet"])
    assert surface is None

    with pytest.raises(DisallowedValuesError) as surface_error:
        solver.fields.field_info.validate_surfaces(["out"])


@pytest.mark.skip("https://github.com/ansys/pyfluent/issues/2404")
@pytest.mark.fluent_version(">=24.2")
def test_field_data_does_not_modify_case(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file.read_case_data(file_name=case_path)
    solver.scheme_eval.scheme_eval("(%save-case-id)")
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")
    solver.fields.field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["cold-inlet"]
    )
    assert not solver.scheme_eval.scheme_eval("(case-modified?)")
