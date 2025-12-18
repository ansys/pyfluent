# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import pytest
from test_utils import pytest_approx

from ansys.fluent.core import (
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    examples,
)
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.field_data_interfaces import (
    FieldUnavailable,
)
from ansys.fluent.core.services.field_data import (
    CellElementType,
    ZoneType,
)
from ansys.fluent.core.solver import VelocityInlet, VelocityInlets, WallBoundaries

HOT_INLET_TEMPERATURE = 313.15


@pytest.mark.fluent_version(">=24.1")
def test_field_data_batches_deprecated_interface(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.mesh.check()

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

    solver.solution.monitor.residual.options.plot = False

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    iterate = solver.solution.run_calculation.iterate
    iterate.get_attr("arguments")
    iterate(iter_count=10)

    # Get field data object
    field_data = solver.fields.field_data

    batch = field_data.new_batch()

    hot_inlet_surf_id = solver.fields.field_data.get_surface_ids(["hot-inlet"])[0]
    batch.add_surfaces_request(
        surfaces=[1, hot_inlet_surf_id],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    batch.add_surfaces_request(
        surfaces=[3],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    batch.add_scalar_fields_request(
        surfaces=[1, "cold-inlet", "hot-inlet"],
        field_name="temperature",
        node_value=True,
        boundary_value=True,
    )
    batch.add_scalar_fields_request(
        surfaces=[2],
        field_name="temperature",
        node_value=True,
        boundary_value=False,
    )
    batch.add_pathlines_fields_request(
        surfaces=[1, "hot-inlet"],
        field_name="temperature",
        provide_particle_time_field=True,
    )

    data = batch.get_fields()

    assert len(data) == 4  # 2 sets of scalar data and 1 of surface and pathlines data.

    # multiple surface *names* batches
    batch2 = field_data.new_batch()
    fields_request = batch2.add_scalar_fields_request
    surface_names = field_data.surfaces.allowed_values()
    fields_request(surfaces=surface_names, field_name="temperature")
    data2 = batch2.get_fields()
    assert data2


@pytest.mark.fluent_version(">=24.1")
def test_field_data_batches(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.mesh.check()

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

    solver.solution.monitor.residual.options.plot = False

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    iterate = solver.solution.run_calculation.iterate
    iterate.get_attr("arguments")
    iterate(iter_count=10)

    # Get field data object
    field_data = solver.fields.field_data

    batch = field_data.new_batch()

    surface_request_with_faces_connectivity = SurfaceFieldDataRequest(
        surfaces=VelocityInlets(settings_source=solver),
        data_types=[SurfaceDataType.FacesConnectivity],
        flatten_connectivity=True,
    )

    surface_request_with_faces_connectivity_deprecated = SurfaceFieldDataRequest(
        surfaces=VelocityInlets(settings_source=solver),
        data_types=[SurfaceDataType.FacesConnectivity],
    )

    su1 = SurfaceFieldDataRequest(
        surfaces=[1, VelocityInlet(settings_source=solver, name="hot-inlet")],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    sux = SurfaceFieldDataRequest(
        surfaces=[1, 4],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    su2 = SurfaceFieldDataRequest(
        surfaces=[3],
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
    )
    sc1 = ScalarFieldDataRequest(
        surfaces=[1] + [item for item in VelocityInlets(settings_source=solver)],
        field_name="temperature",
        node_value=True,
        boundary_value=True,
    )
    sc2 = sc1._replace(surfaces=[2], boundary_value=False)
    vc1 = VectorFieldDataRequest(surfaces=[3, "hot-inlet"], field_name="velocity")
    pt1 = PathlinesFieldDataRequest(
        surfaces=[1, VelocityInlet(settings_source=solver, name="hot-inlet")],
        field_name="temperature",
        provide_particle_time_field=True,
    )
    pt2 = PathlinesFieldDataRequest(
        surfaces=[1, VelocityInlet(settings_source=solver, name="hot-inlet")],
        field_name="temperature",
        provide_particle_time_field=False,
    )

    batch = batch.add_requests(su1)  # adding single request.
    batch = batch.add_requests(su1)  # Duplicate and will be ignored
    batch = batch.add_requests(
        surface_request_with_faces_connectivity,
        surface_request_with_faces_connectivity_deprecated,
    )
    data = batch.add_requests(
        su2, sux, sc1, sc2, vc1, pt1  # 'sux' is duplicate and will be ignored
    ).get_response()  # adding multiple requests.

    with pytest.raises(ValueError):
        # Trying to add request with same 'field_name'.
        # TODO: This is not yet supported. Need to implement in server.
        batch.add_requests(pt2)

    assert (
        len(data) == 5
    )  # 2 sets of scalar data, 1 vector data, 1 surface data and 1 path-lines data.

    faces_connectivity_data = data.get_field_data(
        surface_request_with_faces_connectivity
    )

    faces_connectivity_data_deprecated = data.get_field_data(
        surface_request_with_faces_connectivity_deprecated
    )

    assert len(faces_connectivity_data_deprecated["cold-inlet"].connectivity) == 304
    assert len(faces_connectivity_data["cold-inlet"].connectivity) == 1788

    assert list(faces_connectivity_data_deprecated["cold-inlet"].connectivity[0]) == [
        3,
        2,
        1,
        0,
    ]
    assert list(faces_connectivity_data["cold-inlet"].connectivity[0:5]) == [
        4,
        3,
        2,
        1,
        0,
    ]

    sc1 = sc1._replace(surfaces=[1, "cold-inlet"])
    sc2 = sc1._replace(surfaces=["hot-inlet"])

    scalar_data = data.get_field_data(sc1)
    scalar_data_1 = data.get_field_data(sc2)

    sc3 = sc1._replace(surfaces=[2])
    with pytest.raises(
        KeyError
    ):  # Since for surface_id=2 data is fetched with boundary_value = False
        scalar_data_2 = data.get_field_data(sc3)

    sc3 = sc3._replace(boundary_value=False)
    scalar_data_2 = data.get_field_data(sc3)

    assert list(scalar_data) == [1, "cold-inlet"]
    assert list(scalar_data_2) == [2]

    su1 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
        surfaces=[1, 3, "hot-inlet"],
    )
    surface_data = data.get_field_data(
        su1
    )  # Even if you populate the data using surface_id you can access it via surface name.

    pt1 = PathlinesFieldDataRequest(
        surfaces=[1, "hot-inlet"],
        field_name="temperature",
        provide_particle_time_field=True,
    )
    pathlines_data = data.get_field_data(pt1)

    assert list(surface_data["hot-inlet"]._surf_data) == [
        SurfaceDataType.Vertices,
        SurfaceDataType.FacesCentroid,
    ]
    assert (
        len(scalar_data_1["hot-inlet"]) == surface_data["hot-inlet"].vertices.shape[0]
    )
    assert (
        round(float(np.average(scalar_data_1["hot-inlet"])), 2) == HOT_INLET_TEMPERATURE
    )
    assert sorted(
        list(pathlines_data["hot-inlet"]._pathlines_data_for_surface)
    ) == sorted(
        [
            "vertices",
            "lines",
            "temperature",
            "pathlines-count",
            "particle-time",
        ]
    )

    assert len(pathlines_data["hot-inlet"].particle_time) == 8811

    vector_data = data.get_field_data(vc1)
    assert list(vector_data) == [3, "hot-inlet"]


def test_field_data_attributes(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.fields.field_data

    assert [] == field_data.scalar_fields.allowed_values()

    solver.file.read(file_type="case", file_name=import_file_name)

    allowed_args_no_init = field_data.scalar_fields.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    allowed_args = sorted(field_data.scalar_fields.allowed_values())
    assert len(allowed_args) > len(allowed_args_no_init)

    assert field_data.scalar_fields.range("cell-weight") == [8.0, 24.0]

    assert field_data.surfaces.validate(["hot-inlet", "cold-inlet"])
    assert not field_data.surfaces.validate(["hot-inlet", "inlet"])


@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_3d_deprecated_interface(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.fields.field_data

    assert [] == field_data.scalar_fields.allowed_values()

    solver.file.read(file_type="case", file_name=import_file_name)

    allowed_args_no_init = field_data.scalar_fields.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["cold-inlet"]
    )

    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["cold-inlet"][120] == 101325.0

    vertices_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.Vertices], surfaces=["cold-inlet"]
    )
    assert vertices_data["cold-inlet"][SurfaceDataType.Vertices].shape == (241, 3)
    assert (
        round(float(vertices_data["cold-inlet"][SurfaceDataType.Vertices][5][0]), 2)
        == -0.2
    )

    vertices_and_faces_centroid_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
        surfaces=["hot-inlet", "cold-inlet"],
    )
    assert list(vertices_and_faces_centroid_data["cold-inlet"].keys()) == [
        SurfaceDataType.Vertices,
        SurfaceDataType.FacesCentroid,
    ]
    assert vertices_and_faces_centroid_data["hot-inlet"][
        SurfaceDataType.Vertices
    ].shape == (79, 3)
    assert list(vertices_and_faces_centroid_data.keys()) == [
        "hot-inlet",
        "cold-inlet",
    ]
    assert (
        round(
            float(
                vertices_and_faces_centroid_data["cold-inlet"][
                    SurfaceDataType.FacesCentroid
                ][5][1]
            ),
            2,
        )
        == -0.18
    )
    assert (
        round(
            float(
                vertices_and_faces_centroid_data["hot-inlet"][
                    SurfaceDataType.FacesCentroid
                ][5][1]
            ),
            2,
        )
        == -0.23
    )

    faces_normal_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesNormal], surfaces=[3, 5]
    )
    assert faces_normal_data[3][SurfaceDataType.FacesNormal].shape == (152, 3)
    assert faces_normal_data[5][SurfaceDataType.FacesNormal].shape == (2001, 3)

    faces_connectivity_data_deprecated = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesConnectivity], surfaces=["cold-inlet"]
    )
    assert list(
        faces_connectivity_data_deprecated["cold-inlet"][
            SurfaceDataType.FacesConnectivity
        ][5]
    ) == [12, 13, 17, 16]

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surfaces=["cold-inlet"]
    )

    assert velocity_vector_data["cold-inlet"].shape == (152, 3)

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity-magnitude", surfaces=["cold-inlet", "hot-inlet"]
    )

    assert path_lines_data["cold-inlet"]["vertices"].shape == (76152, 3)
    assert len(path_lines_data["cold-inlet"]["lines"]) == 76000
    assert path_lines_data["cold-inlet"]["velocity-magnitude"].shape == (76152,)

    assert path_lines_data["hot-inlet"]["vertices"].shape == (27555, 3)
    assert len(path_lines_data["hot-inlet"]["lines"]) == 27500
    assert path_lines_data["hot-inlet"]["velocity-magnitude"].shape == (27555,)

    assert list(path_lines_data["cold-inlet"]["lines"][100]) == [100, 101]


@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_3d(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    field_data = solver.fields.field_data

    assert [] == field_data.scalar_fields.allowed_values()

    solver.file.read(file_type="case", file_name=import_file_name)

    allowed_args_no_init = field_data.scalar_fields.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    sc1 = ScalarFieldDataRequest(
        field_name="absolute-pressure", surfaces=["cold-inlet"]
    )
    abs_press_data = field_data.get_field_data(sc1)

    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["cold-inlet"][120] == 101325.0

    su1 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices], surfaces=["cold-inlet"]
    )
    vertices_data = field_data.get_field_data(su1)
    assert vertices_data["cold-inlet"].vertices.shape == (241, 3)
    assert round(float(vertices_data["cold-inlet"].vertices[5][0]), 2) == -0.2

    assert vertices_data["cold-inlet"].face_centroids is None

    su2 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
        surfaces=["hot-inlet", "cold-inlet"],
    )
    vertices_and_faces_centroid_data = field_data.get_field_data(su2)

    assert list(vertices_and_faces_centroid_data["cold-inlet"]._surf_data.keys()) == [
        SurfaceDataType.Vertices,
        SurfaceDataType.FacesCentroid,
    ]
    assert vertices_and_faces_centroid_data["hot-inlet"].vertices.shape == (79, 3)
    assert list(vertices_and_faces_centroid_data.keys()) == [
        "hot-inlet",
        "cold-inlet",
    ]
    assert (
        round(
            float(vertices_and_faces_centroid_data["cold-inlet"].face_centroids[5][1]),
            2,
        )
        == -0.18
    )
    assert (
        round(
            float(vertices_and_faces_centroid_data["hot-inlet"].face_centroids[5][1]),
            2,
        )
        == -0.23
    )

    su3 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.FacesNormal], surfaces=[3, 5]
    )
    faces_normal_data = field_data.get_field_data(su3)
    assert faces_normal_data[3].face_normals.shape == (152, 3)
    assert faces_normal_data[5].face_normals.shape == (2001, 3)

    su4 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.FacesConnectivity], surfaces=["cold-inlet"]
    )
    faces_connectivity_data_deprecated = field_data.get_field_data(su4)
    faces_connectivity_data = field_data.get_field_data(
        SurfaceFieldDataRequest(
            data_types=[SurfaceDataType.FacesConnectivity],
            surfaces=["cold-inlet"],
            flatten_connectivity=True,
        )
    )

    assert (
        faces_connectivity_data_deprecated["cold-inlet"].connectivity[5]
        == [12, 13, 17, 16]
    ).all()
    assert len(faces_connectivity_data["cold-inlet"].connectivity) == 894
    assert list(faces_connectivity_data_deprecated["cold-inlet"].connectivity[0]) == [
        3,
        2,
        1,
        0,
    ]
    assert list(faces_connectivity_data["cold-inlet"].connectivity[0:5]) == [
        4,
        3,
        2,
        1,
        0,
    ]

    velocity_vector_data = field_data.get_field_data(
        VectorFieldDataRequest(field_name="velocity", surfaces=["cold-inlet"])
    )
    assert velocity_vector_data["cold-inlet"].shape == (152, 3)

    path_lines_data_deprecated = field_data.get_field_data(
        PathlinesFieldDataRequest(
            field_name="velocity-magnitude", surfaces=["cold-inlet", "hot-inlet"]
        )
    )
    path_lines_data = field_data.get_field_data(
        PathlinesFieldDataRequest(
            field_name="velocity-magnitude",
            surfaces=["cold-inlet", "hot-inlet"],
            flatten_connectivity=True,
        )
    )

    assert path_lines_data["cold-inlet"].vertices.shape == (76152, 3)
    assert len(path_lines_data_deprecated["cold-inlet"].lines) == 76000
    assert path_lines_data["cold-inlet"].scalar_field.shape == (76152,)

    assert path_lines_data["hot-inlet"].vertices.shape == (27555, 3)
    assert len(path_lines_data["hot-inlet"].lines) == 82500
    assert path_lines_data["hot-inlet"].scalar_field.shape == (27555,)

    assert path_lines_data["hot-inlet"].scalar_field_name == "velocity-magnitude"

    assert list(path_lines_data["cold-inlet"].lines[:3]) == [2, 0, 1]


@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_2d(disk_case_session) -> None:
    solver = disk_case_session

    field_data = solver.fields.field_data

    allowed_args_no_init = field_data.scalar_fields.allowed_values()
    assert len(allowed_args_no_init) != 0

    assert not field_data.is_data_valid()

    solver.solution.initialization.hybrid_initialize()

    assert field_data.is_data_valid()

    # Absolute Pressure data over the cold-inlet (surface_id=3)
    abs_press_data = field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["velocity-inlet-2"]
    )

    assert abs_press_data["velocity-inlet-2"].shape == (11,)
    assert abs_press_data["velocity-inlet-2"][5] == 101325.0

    vertices_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.Vertices], surfaces=["interior-4"]
    )
    assert round(vertices_data["interior-4"][SurfaceDataType.Vertices][5][0], 2) == 0.0

    faces_centroid_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesCentroid], surfaces=["velocity-inlet-2"]
    )
    assert (
        round(
            float(
                faces_centroid_data["velocity-inlet-2"][SurfaceDataType.FacesCentroid][
                    5
                ][1]
            ),
            2,
        )
        == 0.02
    )

    faces_connectivity_data = field_data.get_surface_data(
        data_types=[SurfaceDataType.FacesConnectivity], surfaces=["velocity-inlet-2"]
    )["velocity-inlet-2"][SurfaceDataType.FacesConnectivity]
    assert (faces_connectivity_data[5] == [5, 6]).all()

    velocity_vector_data = field_data.get_vector_field_data(
        field_name="velocity", surfaces=["velocity-inlet-2"]
    )

    assert velocity_vector_data["velocity-inlet-2"].shape == (10, 3)

    path_lines_data = field_data.get_pathlines_field_data(
        field_name="velocity-magnitude", surfaces=["velocity-inlet-2"]
    )

    assert path_lines_data["velocity-inlet-2"]["vertices"].shape == (5010, 3)
    assert len(path_lines_data["velocity-inlet-2"]["lines"]) == 5000
    assert path_lines_data["velocity-inlet-2"]["velocity-magnitude"].shape == (5010,)

    assert list(path_lines_data["velocity-inlet-2"]["lines"][100]) == [100, 101]


def test_field_data_errors(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    with pytest.raises(DisallowedValuesError):
        solver.fields.field_data.get_scalar_field_data(
            field_name="y-face-area", surfaces=[0]
        )

    with pytest.raises(DisallowedValuesError):
        solver.fields.field_data.get_scalar_field_data(
            field_name="partition-neighbors", surfaces=[0]
        )

    solver.file.read(file_type="case", file_name=import_file_name)

    with pytest.raises(FieldUnavailable):
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
    assert solver.fields.field_data

    with pytest.raises(DisallowedValuesError):
        solver.fields.field_data.get_scalar_field_data(
            field_name="density", surfaces=["bob"]
        )

    with pytest.raises(DisallowedValuesError):
        solver.fields.field_data.get_scalar_field_data(
            field_name="xdensity", surfaces=[0]
        )


@pytest.mark.skip("https://github.com/ansys/pyfluent/issues/2404")
@pytest.mark.fluent_version(">=24.2")
def test_field_data_does_not_modify_case(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file.read_case_data(file_name=case_path)
    solver.scheme.eval("(%save-case-id)")
    assert not solver.scheme.eval("(case-modified?)")
    solver.fields.field_data.get_scalar_field_data(
        field_name="absolute-pressure", surfaces=["cold-inlet"]
    )
    assert not solver.scheme.eval("(case-modified?)")


@pytest.mark.fluent_version(">=24.1")
def test_field_data_streaming_in_meshing_mode(new_meshing_session):
    meshing = new_meshing_session
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )

    mesh_data = {}

    def plot_mesh(index, field_name, data):
        if data is not None:
            if index in mesh_data:
                mesh_data[index].update({field_name: data})
            else:
                mesh_data[index] = {field_name: data}

    meshing.fields.field_data_streaming.register_callback(plot_mesh)
    meshing.fields.field_data_streaming.start(provideBytesStream=True, chunkSize=1024)

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    meshing.workflow.TaskObject["Import Geometry"].Arguments = {
        "FileName": import_file_name,
        "LengthUnit": "in",
    }
    meshing.workflow.TaskObject["Import Geometry"].Execute()

    assert len(mesh_data[5]["vertices"]) == 66
    assert len(mesh_data[5]["faces"]) == 80

    assert list(mesh_data[12].keys()) == ["vertices", "faces"]


@pytest.mark.fluent_version(">=25.2")
def test_mesh_data_2d_standard(disk_case_session):
    solver = disk_case_session
    zones_info = solver.fields.field_data.get_zones_info()
    cell_zone_names = [z.name for z in zones_info if z.zone_type == ZoneType.CELL]
    face_zone_names = [z.name for z in zones_info if z.zone_type == ZoneType.FACE]
    assert cell_zone_names == ["fluid-7"]
    assert face_zone_names == [
        "velocity-inlet-2",
        "pressure-outlet-3",
        "interior-4",
        "axis-5",
        "wall-6",
    ]
    mesh = solver.fields.field_data.get_mesh(zone="fluid-7")
    assert len(mesh.nodes) == 6351
    assert len(mesh.elements) == 6192
    assert mesh.elements[0].element_type == CellElementType.QUADRILATERAL
    assert len(mesh.elements[0].node_indices) == 4
    assert min(mesh.nodes, key=lambda x: x.x).x == pytest_approx(0.0)
    assert max(mesh.nodes, key=lambda x: x.x).x == pytest_approx(0.06202)
    assert min(mesh.nodes, key=lambda x: x.y).y == pytest_approx(0.0)
    assert max(mesh.nodes, key=lambda x: x.y).y == pytest_approx(0.443)
    assert min(mesh.nodes, key=lambda x: x.z).z == pytest_approx(0.0)
    assert max(mesh.nodes, key=lambda x: x.z).z == pytest_approx(0.0)


@pytest.mark.fluent_version(">=25.2")
def test_mesh_data_3d_poly(static_mixer_case_session):
    solver = static_mixer_case_session
    zones_info = solver.fields.field_data.get_zones_info()
    cell_zone_names = [z.name for z in zones_info if z.zone_type == ZoneType.CELL]
    face_zone_names = [z.name for z in zones_info if z.zone_type == ZoneType.FACE]
    assert cell_zone_names == ["fluid"]
    assert face_zone_names == ["inlet1", "inlet2", "outlet", "wall", "interior--fluid"]
    mesh = solver.fields.field_data.get_mesh(zone="fluid")
    assert len(mesh.nodes) == 82247
    assert len(mesh.elements) == 22771
    assert mesh.elements[0].element_type == CellElementType.POLYHEDRON
    assert len(mesh.elements[0].node_indices) == 0
    assert len(mesh.elements[0].facets) == 9
    assert len(mesh.elements[0].facets[0].node_indices) == 4
    assert min(mesh.nodes, key=lambda x: x.x).x == pytest_approx(-1.999075e-03)
    assert max(mesh.nodes, key=lambda x: x.x).x == pytest_approx(1.999125e-03)
    assert min(mesh.nodes, key=lambda x: x.y).y == pytest_approx(-3.000000e-03)
    assert max(mesh.nodes, key=lambda x: x.y).y == pytest_approx(3.000000e-03)
    assert min(mesh.nodes, key=lambda x: x.z).z == pytest_approx(-2.000000e-03)
    assert max(mesh.nodes, key=lambda x: x.z).z == pytest_approx(2.500000e-03)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_3d_with_location_objects(new_solver_session) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    field_data = solver.fields.field_data
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.solution.initialization.hybrid_initialize()
    assert field_data.is_data_valid()

    # Check different iterations with location objects

    scalar_object_from_surface_list = ScalarFieldDataRequest(
        field_name="absolute-pressure", surfaces=["hot-inlet", "cold-inlet"]
    )
    abs_press_data = field_data.get_field_data(scalar_object_from_surface_list)
    assert list(abs_press_data) == ["hot-inlet", "cold-inlet"]
    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["cold-inlet"][120] == 101325.0
    assert abs_press_data["hot-inlet"].shape == (79,)

    scalar_object_from_surface_objects = ScalarFieldDataRequest(
        field_name="absolute-pressure",
        surfaces=solver.setup.boundary_conditions.velocity_inlet,
    )
    abs_press_data = field_data.get_field_data(scalar_object_from_surface_objects)
    assert list(abs_press_data) == ["hot-inlet", "cold-inlet"]
    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["cold-inlet"][120] == 101325.0
    assert abs_press_data["hot-inlet"].shape == (79,)

    scalar_object_from_surface_objects = ScalarFieldDataRequest(
        field_name="absolute-pressure",
        surfaces=[
            solver.setup.boundary_conditions.velocity_inlet["hot-inlet"],
            solver.setup.boundary_conditions.velocity_inlet["cold-inlet"],
        ],
    )
    abs_press_data = field_data.get_field_data(scalar_object_from_surface_objects)
    assert list(abs_press_data) == ["hot-inlet", "cold-inlet"]
    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["cold-inlet"][120] == 101325.0
    assert abs_press_data["hot-inlet"].shape == (79,)

    # For multiple surface objects
    scalar_object_from_surface_objects = ScalarFieldDataRequest(
        field_name="absolute-pressure",
        surfaces=VelocityInlets(settings_source=solver)
        + WallBoundaries(settings_source=solver),
    )
    abs_press_data = field_data.get_field_data(scalar_object_from_surface_objects)
    assert list(abs_press_data) == [
        "hot-inlet",
        "cold-inlet",
        "wall-inlet",
        "wall-elbow",
    ]
    assert abs_press_data["cold-inlet"].shape == (241,)
    assert abs_press_data["hot-inlet"].shape == (79,)
    assert abs_press_data["wall-inlet"].shape == (538,)
    assert abs_press_data["wall-elbow"].shape == (4339,)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_field_data_objects_3d_with_location_objects_overall(
    new_solver_session,
) -> None:
    solver = new_solver_session
    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    field_data = solver.fields.field_data
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.solution.initialization.hybrid_initialize()
    assert field_data.is_data_valid()

    su1 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices],
        surfaces=[VelocityInlet(settings_source=solver, name="cold-inlet")],
    )
    vertices_data = field_data.get_field_data(su1)
    assert vertices_data["cold-inlet"].vertices.shape == (241, 3)
    assert round(float(vertices_data["cold-inlet"].vertices[5][0]), 2) == -0.2

    assert vertices_data["cold-inlet"].face_centroids is None

    su2 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
        surfaces=VelocityInlets(settings_source=solver),
    )
    vertices_and_faces_centroid_data = field_data.get_field_data(su2)

    assert list(vertices_and_faces_centroid_data["cold-inlet"]._surf_data.keys()) == [
        SurfaceDataType.Vertices,
        SurfaceDataType.FacesCentroid,
    ]
    assert vertices_and_faces_centroid_data["hot-inlet"].vertices.shape == (79, 3)
    assert list(vertices_and_faces_centroid_data.keys()) == [
        "cold-inlet",
        "hot-inlet",
    ]
    assert (
        round(
            float(vertices_and_faces_centroid_data["cold-inlet"].face_centroids[5][1]),
            2,
        )
        == -0.18
    )
    assert (
        round(
            float(vertices_and_faces_centroid_data["hot-inlet"].face_centroids[5][1]),
            2,
        )
        == -0.23
    )

    su4 = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.FacesConnectivity],
        surfaces=[VelocityInlet(settings_source=solver, name="cold-inlet")],
    )
    faces_connectivity_data = field_data.get_field_data(su4)
    assert (
        faces_connectivity_data["cold-inlet"].connectivity[5] == [12, 13, 17, 16]
    ).all()

    velocity_vector_data = field_data.get_field_data(
        VectorFieldDataRequest(
            field_name="velocity",
            surfaces=[VelocityInlet(settings_source=solver, name="cold-inlet")],
        )
    )
    assert velocity_vector_data["cold-inlet"].shape == (152, 3)

    path_lines_data = field_data.get_field_data(
        PathlinesFieldDataRequest(
            field_name="velocity-magnitude",
            surfaces=VelocityInlets(settings_source=solver),
        )
    )

    assert path_lines_data["cold-inlet"].vertices.shape == (76152, 3)
    assert len(path_lines_data["cold-inlet"].lines) == 76000
    assert path_lines_data["cold-inlet"].scalar_field.shape == (76152,)

    assert path_lines_data["hot-inlet"].vertices.shape == (27555, 3)
    assert len(path_lines_data["hot-inlet"].lines) == 27500
    assert path_lines_data["hot-inlet"].scalar_field.shape == (27555,)

    assert path_lines_data["hot-inlet"].scalar_field_name == "velocity-magnitude"

    assert list(path_lines_data["cold-inlet"].lines[100]) == [100, 101]
