import numpy as np
import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.services.field_data import (
    ScalarFieldNameError,
    ScalarFieldUnavailable,
    SurfaceDataType,
    SurfaceNameError,
)

HOT_INLET_TEMPERATURE = 313.15


@pytest.mark.dev
@pytest.mark.fluent_232
def test_field_data(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_filename)
    solver.tui.mesh.check()

    solver.setup.models.energy.enabled = True
    solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
    solver.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

    # Set up boundary conditions for CFD analysis
    solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = 0.4
    solver.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].turb_intensity = 0.05
    solver.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_hydraulic_diam = "4 [in]"

    solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = 293.15

    solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag = 1.2
    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].turb_hydraulic_diam = "1 [in]"

    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].t = HOT_INLET_TEMPERATURE

    solver.setup.boundary_conditions.pressure_outlet["outlet"].turb_viscosity_ratio = 4

    solver.tui.solve.monitors.residual.plot("no")

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    solver.solution.run_calculation.iterate.get_attr("arguments")
    solver.solution.run_calculation.iterate(iter_count=10)

    # Get field data object
    field_data = solver.field_data

    transaction = field_data.new_transaction()

    hot_inlet_surf_id = solver.field_info.get_surfaces_info()["hot-inlet"][
        "surface_id"
    ][0]
    transaction.add_surfaces_request(
        surface_ids=[1, hot_inlet_surf_id],
        provide_vertices=True,
        provide_faces=False,
        provide_faces_centroid=True,
    )
    transaction.add_scalar_fields_request(
        surface_ids=[1, hot_inlet_surf_id],
        field_name="temperature",
        node_value=True,
        boundary_value=True,
    )
    transaction.add_pathlines_fields_request(
        surface_ids=[1, hot_inlet_surf_id],
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
    assert (
        len(data[scalar_field_tag][hot_inlet_surf_id]["temperature"])
        == len(data[surface_data_tag][hot_inlet_surf_id]["vertices"]) / 3
    )
    assert (
        round(
            float(np.average(data[scalar_field_tag][hot_inlet_surf_id]["temperature"])),
            2,
        )
        == HOT_INLET_TEMPERATURE
    )
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
    surface_names = (
        transaction2.add_scalar_fields_request.surface_names.allowed_values()
    )
    transaction2.add_scalar_fields_request(
        surface_names=surface_names, field_name="temperature"
    )
    data2 = transaction2.get_fields()
    assert data2


def test_field_data_allowed_values(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.field_data
    field_info = solver.field_info
    transaction = field_data.new_transaction()

    assert [] == field_data.get_scalar_field_data.field_name.allowed_values()

    solver.file.read(file_type="case", file_name=import_filename)

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    expected_allowed_args = sorted(field_info.get_scalar_fields_info())
    allowed_args = field_data.get_scalar_field_data.field_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    assert len(allowed_args) > len(allowed_args_no_init)
    allowed_args = transaction.add_scalar_fields_request.field_name.allowed_values()
    assert expected_allowed_args == allowed_args

    expected_allowed_args = sorted(field_info.get_surfaces_info())
    allowed_args = field_data.get_scalar_field_data.surface_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = transaction.add_scalar_fields_request.surface_names.allowed_values()
    assert expected_allowed_args == allowed_args

    expected_allowed_args = sorted(field_info.get_surfaces_info())
    allowed_args = field_data.get_surface_data.surface_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = transaction.add_scalar_fields_request.surface_names.allowed_values()
    assert expected_allowed_args == allowed_args

    allowed_args = field_data.get_surface_data.surface_ids.allowed_values()
    assert len(expected_allowed_args) == len(allowed_args)
    allowed_args = transaction.add_scalar_fields_request.surface_ids.allowed_values()
    assert len(expected_allowed_args) == len(allowed_args)

    expected_allowed_args = sorted(field_info.get_vector_fields_info())
    allowed_args = field_data.get_vector_field_data.field_name.allowed_values()
    assert expected_allowed_args and (expected_allowed_args == allowed_args)
    allowed_args = transaction.add_vector_fields_request.field_name.allowed_values()
    assert expected_allowed_args == allowed_args


@pytest.mark.dev
@pytest.mark.fluent_232
def test_field_data_objects_3d(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.field_data

    assert [] == field_data.get_scalar_field_data.field_name.allowed_values()

    solver.file.read(file_type="case", file_name=import_filename)

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surface_name="cold-inlet"
    )

    assert abs_press_data.size == 241
    assert abs_press_data[120].scalar_data == 101325.0

    vertices_data = field_data.get_surface_data(
        data_type=SurfaceDataType.Vertices, surface_name="cold-inlet"
    )
    assert round(float(vertices_data[5].x), 2) == -0.2

    faces_centroid_data = field_data.get_surface_data(
        data_type=SurfaceDataType.FacesCentroid, surface_name="cold-inlet"
    )
    assert round(float(faces_centroid_data[5].y), 2) == -0.18

    faces_connectivity_data = field_data.get_surface_data(
        data_type=SurfaceDataType.FacesConnectivity, surface_name="cold-inlet"
    )
    assert faces_connectivity_data[5].node_count == 4
    assert (faces_connectivity_data[5].node_indices == [12, 13, 17, 16]).all()

    faces_normal_data = field_data.get_surface_data(
        data_type=SurfaceDataType.FacesNormal, surface_name="cold-inlet"
    )
    assert faces_normal_data.size == 152
    assert faces_normal_data.surface_id == 3

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surface_name="cold-inlet"
    )

    assert velocity_vector_data.size == 152
    assert velocity_vector_data.scale == 1.0

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity", surface_name="cold-inlet"
    )

    assert path_lines_data["vertices"].size == 76152
    assert path_lines_data["lines"].size == 76000
    assert path_lines_data["velocity"].size == 76152

    assert path_lines_data["lines"][100].node_count == 2
    assert all(path_lines_data["lines"][100].node_indices == [100, 101])


@pytest.mark.dev
@pytest.mark.fluent_232
def test_field_data_objects_2d(load_disk_mesh) -> None:
    solver = load_disk_mesh

    field_data = solver.field_data

    allowed_args_no_init = field_data.get_scalar_field_data.field_name.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surface_name="velocity-inlet-2"
    )

    assert abs_press_data.size == 11
    assert abs_press_data[5].scalar_data == 101325.0

    vertices_data = field_data.get_surface_data(
        data_type=SurfaceDataType.Vertices, surface_name="interior-4"
    )
    assert round(float(vertices_data[5].x), 2) == 0.0

    faces_centroid_data = field_data.get_surface_data(
        data_type=SurfaceDataType.FacesCentroid, surface_name="velocity-inlet-2"
    )
    assert round(float(faces_centroid_data[5].y), 2) == 0.02

    faces_connectivity_data = field_data.get_surface_data(
        data_type=SurfaceDataType.FacesConnectivity, surface_name="velocity-inlet-2"
    )
    assert faces_connectivity_data[5].node_count == 2
    assert (faces_connectivity_data[5].node_indices == [5, 6]).all()

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surface_name="velocity-inlet-2"
    )

    assert velocity_vector_data.size == 10
    assert velocity_vector_data.scale == 1.0

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity", surface_name="velocity-inlet-2"
    )

    assert path_lines_data["vertices"].size == 5010
    assert path_lines_data["lines"].size == 5000
    assert path_lines_data["velocity"].size == 5010

    assert path_lines_data["lines"][100].node_count == 2
    assert all(path_lines_data["lines"][100].node_indices == [100, 101])


def test_field_data_errors(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(
            field_name="y-face-area", surface_ids=[0]
        )
    assert fne.value.field_name == "y-face-area"

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(
            field_name="partition-neighbors", surface_ids=[0]
        )
    assert fne.value.field_name == "partition-neighbors"

    solver.file.read(file_type="case", file_name=import_filename)

    with pytest.raises(ScalarFieldUnavailable) as fnu:
        solver.field_data.get_scalar_field_data(field_name="density", surface_ids=[0])
    assert fnu.value.field_name == "density"

    y_face_area = solver.field_data.get_scalar_field_data(
        field_name="y-face-area", surface_ids=[0]
    )
    assert y_face_area and isinstance(y_face_area, dict)

    partition_neighbors = solver.field_data.get_scalar_field_data(
        field_name="partition-neighbors", surface_ids=[0]
    )
    assert partition_neighbors and isinstance(partition_neighbors, dict)

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    # Get field data object
    field_data = solver.field_data

    with pytest.raises(SurfaceNameError) as sne:
        solver.field_data.get_scalar_field_data(
            field_name="density", surface_name="bob"
        )
    assert sne.value.surface_name == "bob"

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(field_name="xdensity", surface_ids=[0])
    assert fne.value.field_name == "xdensity"
