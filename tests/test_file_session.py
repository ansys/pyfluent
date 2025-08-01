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

from pathlib import Path

import pytest

from ansys.fluent.core import (
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    examples,
)
from ansys.fluent.core.file_session import (
    FileSession,
    InvalidFieldName,
    InvalidMultiPhaseFieldName,
)


def round_off_list_elements(input_list):
    for index, value in enumerate(input_list):
        input_list[index] = round(value, 6)

    return input_list


def test_field_data_multi_phase():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()

    # backward compatibility check
    assert file_session.fields.field_data == file_session.field_data

    assert Path(case_file_name).exists()
    assert Path(data_file_name).exists()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    scalar_field_data_request = ScalarFieldDataRequest(
        field_name="phase-2:SV_DENSITY",
        surfaces=[33],
    )

    sv_density = file_session.fields.field_data.get_field_data(
        scalar_field_data_request
    )

    assert sv_density[33].shape == (268,)
    assert sv_density[33][130] == 1.225
    scalar_field_data_request_1 = ScalarFieldDataRequest(
        field_name="phase-2:SV_WALL_YPLUS", surfaces=[33]
    )
    assert (
        round(
            file_session.fields.field_data.get_field_data(scalar_field_data_request_1)[
                33
            ][130],
            5,
        )
        == 0.00103
    )
    vector_data_request = VectorFieldDataRequest(
        field_name="phase-2:velocity", surfaces=[33]
    )
    vector_data_request_1 = VectorFieldDataRequest(
        field_name="phase-1:velocity", surfaces=[34]
    )
    vector_data = file_session.fields.field_data.get_field_data
    assert vector_data(vector_data_request)[33].shape == (
        268,
        3,
    )
    assert vector_data(vector_data_request_1)[34].shape == (
        2168,
        3,
    )


def test_field_data_single_phase():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()

    # backward compatibility check
    assert file_session.fields.field_data == file_session.field_data

    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    assert round_off_list_elements(
        file_session.field_data.scalar_fields.range("SV_P")
    ) == [-339.203452, 339.417934]
    assert len(file_session.field_data.scalar_fields()) == 29
    assert list(file_session.field_data.surfaces()) == [
        "wall",
        "symmetry",
        "pressure-outlet-7",
        "velocity-inlet-6",
        "velocity-inlet-5",
        "default-interior",
    ]
    sv_t_wall_request = ScalarFieldDataRequest(field_name="SV_T", surfaces=["wall"])
    sv_t_wall = file_session.fields.field_data.get_field_data(sv_t_wall_request)
    assert sv_t_wall["wall"].shape == (3630,)
    assert round(sv_t_wall["wall"][1800], 4) == 313.15

    surface_data = file_session.fields.field_data.get_field_data
    surface_data_wall_request = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices], surfaces=[3]
    )
    surface_data_wall = surface_data(surface_data_wall_request)
    assert surface_data_wall[3].shape == (3810, 3)
    assert round(surface_data_wall[3][1500][0], 5) == 0.12406
    assert round(surface_data_wall[3][1500][1], 5) == 0.09525
    assert round(surface_data_wall[3][1500][2], 5) == 0.04216

    surface_data_symmetry_request = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.FacesConnectivity],
        surfaces=["symmetry"],
        flatten_connectivity=True,
    )
    surface_data_symmetry = surface_data(surface_data_symmetry_request)
    assert len(surface_data_symmetry["symmetry"]) == 10090

    surface_data_symmetry_request_deprecated = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.FacesConnectivity],
        surfaces=["symmetry"],
    )
    surface_data_symmetry_deprecated = surface_data(
        surface_data_symmetry_request_deprecated
    )
    assert list((surface_data_symmetry_deprecated["symmetry"])[1000]) == [
        1259,
        1260,
        1227,
        1226,
    ]

    vector_data = file_session.fields.field_data.get_field_data
    vector_data_request = VectorFieldDataRequest(
        field_name="velocity", surfaces=["wall"]
    )
    assert vector_data(vector_data_request)["wall"].shape == (3630, 3)

    vector_data_symmetry_request = VectorFieldDataRequest(
        field_name="velocity", surfaces=["symmetry"]
    )
    vector_data_symmetry = vector_data(vector_data_symmetry_request)["symmetry"]
    assert vector_data_symmetry.shape == (2018, 3)
    assert round(vector_data_symmetry[1009][0], 5) == 0.0023
    assert round(vector_data_symmetry[1009][1], 5) == 1.22311


def test_batch_request_single_phase():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    surf_data_request = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesConnectivity],
        surfaces=[3, 5],
    )
    scalar_data_request_1 = ScalarFieldDataRequest(field_name="SV_T", surfaces=[3, 5])
    scalar_data_request_2 = ScalarFieldDataRequest(
        field_name="SV_T",
        surfaces=["wall", "symmetry"],
        node_value=False,
        boundary_value=False,
    )
    vector_data_request_1 = VectorFieldDataRequest(
        field_name="velocity", surfaces=[3, 5]
    )

    batch_1.add_requests(
        surf_data_request,
        scalar_data_request_1,
        scalar_data_request_2,
        vector_data_request_1,
    )

    data = batch_1.get_response()

    assert data

    assert len(data) == 3

    # Surfaces Data
    surface_data = data.get_field_data(surf_data_request)
    assert len(surface_data) == 2
    assert list(surface_data[3]._surf_data.keys()) == [
        SurfaceDataType.Vertices,
        SurfaceDataType.FacesConnectivity,
    ]

    # Scalar Field Data
    scalar_data = data.get_field_data(scalar_data_request_2)
    assert len(scalar_data) == 2
    assert len(scalar_data["wall"]) == 3630
    assert round(scalar_data["wall"][50], 2) == 293.15

    assert round(scalar_data["symmetry"][50], 2) == 293.15

    # Vector Field Data
    vector_data = data.get_field_data(vector_data_request_1)
    assert len(vector_data) == 2
    assert vector_data[5].shape == (100, 3)
    assert round(vector_data[5][50][0], 5) == 0.03035
    assert round(vector_data[5][50][1], 5) == 0.49224
    assert round(vector_data[5][50][2], 5) == 0.00468


def test_batch_request_multi_phase():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    scalar_field_request = ScalarFieldDataRequest(
        field_name="phase-2:SV_WALL_YPLUS",
        surfaces=[29, 30],
        node_value=False,
        boundary_value=False,
    )
    vector_field_request = VectorFieldDataRequest(
        field_name="phase-3:velocity", surfaces=[31]
    )

    batch_1.add_requests(scalar_field_request, vector_field_request)

    data = batch_1.get_response()

    assert data

    assert len(data) == 2

    # Scalar Field Data

    sc_field_data = data.get_field_data(scalar_field_request)
    assert len(sc_field_data) == 2

    # Vector Field Data
    vector_data = data.get_field_data(vector_field_request)
    assert len(vector_data) == 1
    assert vector_data[31].shape == (152, 3)


def test_error_handling_single_phase():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    with pytest.raises(NotImplementedError):
        batch_1.add_requests(
            PathlinesFieldDataRequest(field_name="SV_T", surfaces=[3, 5])
        )

    with pytest.raises(NotImplementedError):
        field_data.get_field_data(
            PathlinesFieldDataRequest(field_name="SV_T", surfaces=[3, 5])
        )


def test_error_handling_multi_phase():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()
    with pytest.raises(InvalidMultiPhaseFieldName):
        batch_1.add_requests(ScalarFieldDataRequest("SV_WALL_YPLUS", surfaces=[29, 30]))

    with pytest.raises(InvalidMultiPhaseFieldName):
        field_data.get_field_data(
            VectorFieldDataRequest(field_name="velocity", surfaces=[34])
        )[34].size

    with pytest.raises(InvalidFieldName):
        field_data.get_field_data(
            VectorFieldDataRequest(field_name="phase-1:temperature", surfaces=[34])
        )[34].size


# USING DEPRECATED FORMAT


def test_field_data_multi_phase_deprecated():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()

    # backward compatibility check
    assert file_session.fields.field_data == file_session.field_data

    assert Path(case_file_name).exists()
    assert Path(data_file_name).exists()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    sv_density = file_session.fields.field_data.get_scalar_field_data(
        field_name="phase-2:SV_DENSITY", surfaces=[33]
    )
    assert sv_density[33].shape == (268,)
    assert sv_density[33][130] == 1.225
    assert (
        round(
            file_session.fields.field_data.get_scalar_field_data(
                field_name="phase-2:SV_WALL_YPLUS", surfaces=[33]
            )[33][130],
            5,
        )
        == 0.00103
    )
    vector_data = file_session.fields.field_data.get_vector_field_data
    assert vector_data(field_name="phase-2:velocity", surfaces=[33])[33].shape == (
        268,
        3,
    )
    assert vector_data(field_name="phase-1:velocity", surfaces=[34])[34].shape == (
        2168,
        3,
    )


def test_field_data_single_phase_deprecated():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()

    # backward compatibility check
    assert file_session.fields.field_data == file_session.field_data

    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    assert round_off_list_elements(
        file_session.field_data.scalar_fields.range("SV_P")
    ) == [-339.203452, 339.417934]
    assert len(file_session.field_data.scalar_fields()) == 29
    assert list(file_session.field_data.surfaces()) == [
        "wall",
        "symmetry",
        "pressure-outlet-7",
        "velocity-inlet-6",
        "velocity-inlet-5",
        "default-interior",
    ]
    sv_t_wall = file_session.fields.field_data.get_scalar_field_data(
        "SV_T", surfaces=["wall"]
    )
    assert sv_t_wall["wall"].shape == (3630,)
    assert round(sv_t_wall["wall"][1800], 4) == 313.15

    surface_data = file_session.fields.field_data.get_surface_data
    surface_data_wall = surface_data(
        data_types=[SurfaceDataType.Vertices], surfaces=[3]
    )
    assert surface_data_wall[3].shape == (3810, 3)
    assert round(surface_data_wall[3][1500][0], 5) == 0.12406
    assert round(surface_data_wall[3][1500][1], 5) == 0.09525
    assert round(surface_data_wall[3][1500][2], 5) == 0.04216

    surface_data_symmetry_deprecated = surface_data(
        data_types=[SurfaceDataType.FacesConnectivity],
        surfaces=["symmetry"],
    )
    assert len(surface_data_symmetry_deprecated["symmetry"]) == 2018

    surface_data_symmetry = surface_data(
        data_types=[SurfaceDataType.FacesConnectivity],
        surfaces=["symmetry"],
        flatten_connectivity=True,
    )
    assert list(surface_data_symmetry["symmetry"][:5]) == [4, 295, 294, 33, 34]

    vector_data = file_session.fields.field_data.get_vector_field_data
    assert vector_data("velocity", surfaces=["wall"])["wall"].shape == (3630, 3)

    vector_data_symmetry = vector_data("velocity", surfaces=["symmetry"])["symmetry"]
    assert vector_data_symmetry.shape == (2018, 3)
    assert round(vector_data_symmetry[1009][0], 5) == 0.0023
    assert round(vector_data_symmetry[1009][1], 5) == 1.22311


def test_data_reader_single_phase_deprecated():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    data_file = file_session._data_file
    assert data_file.case_file == "elbow1.cas.h5"
    assert data_file.get_phases() == ["phase-1"]
    assert len(data_file.get_face_variables("phase-1")) == 30
    assert len(data_file.get_cell_variables("phase-1")) == 14

    assert data_file.get_cell_variables("phase-1") == [
        "SV_BF_V",
        "SV_D",
        "SV_DENSITY",
        "SV_H",
        "SV_K",
        "SV_LORENTZ_FORCE",
        "SV_MU_LAM",
        "SV_MU_T",
        "SV_P",
        "SV_T",
        "SV_U",
        "SV_V",
        "SV_W",
        "",
    ]

    assert len(data_file.get_face_scalar_field_data("phase-1", "SV_DENSITY", 3)) == 3630


def test_data_reader_multi_phase_deprecated():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    data_file = file_session._data_file
    assert data_file.case_file == "mixing_elbow_mul_ph.cas.h5"
    assert data_file.get_phases() == [
        "phase-1",
        "phase-2",
        "phase-3",
        "phase-4",
    ]
    assert len(data_file.get_face_variables("phase-1")) == 23
    assert len(data_file.get_face_variables("phase-3")) == 13
    assert len(data_file.get_cell_variables("phase-2")) == 14

    assert data_file.get_cell_variables("phase-2") == [
        "SV_BF_V",
        "SV_DENSITY",
        "SV_DENSITY_M1",
        "SV_MU_LAM",
        "SV_MU_T",
        "SV_U",
        "SV_U_M1",
        "SV_V",
        "SV_VOF",
        "SV_VOF_M1",
        "SV_V_M1",
        "SV_W",
        "SV_W_M1",
        "",
    ]

    assert len(data_file.get_face_scalar_field_data("phase-1", "SV_DENSITY", 33)) == 268


def test_batch_request_single_phase_deprecated():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    batch_1.add_surfaces_request(surfaces=[3, 5])

    batch_1.add_scalar_fields_request("SV_T", surfaces=[3, 5])
    batch_1.add_scalar_fields_request("SV_T", surfaces=["wall", "symmetry"])

    batch_1.add_vector_fields_request("velocity", surfaces=[3, 5])

    data = batch_1.get_fields()

    assert data

    assert len(data) == 3

    # Surfaces Data
    surface_data = data()[(("type", "surface-data"),)]
    assert len(surface_data) == 2
    assert list(surface_data[3].keys()) == ["faces", "vertices"]

    # Scalar Field Data
    scalar_field_tag = (
        ("type", "scalar-field"),
        ("dataLocation", 1),
        ("boundaryValues", False),
    )
    scalar_data = data()[scalar_field_tag]
    assert len(scalar_data) == 3
    assert len(scalar_data[5]["SV_T"]) == 100
    assert round(scalar_data[5]["SV_T"][50], 2) == 295.43

    surf_id = file_session.field_data.surfaces()["symmetry"]["surface_id"][0]
    assert round(scalar_data[surf_id]["SV_T"][50], 2) == 293.15

    # Vector Field Data
    vector_data = data()[(("type", "vector-field"),)]
    assert len(vector_data) == 2
    assert len(vector_data[5]["velocity"]) == 300
    assert round(vector_data[5]["velocity"][150], 5) == 0.03035
    assert round(vector_data[5]["velocity"][151], 5) == 0.49224
    assert round(vector_data[5]["velocity"][152], 5) == 0.00468


def test_batch_request_multi_phase_deprecated():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession(case_file_name, data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    batch_1.add_scalar_fields_request("phase-2:SV_WALL_YPLUS", surfaces=[29, 30])

    batch_1.add_vector_fields_request("phase-3:velocity", surfaces=[31])

    data = batch_1.get_fields()

    assert data

    assert len(data) == 2

    # Scalar Field Data
    scalar_field_tag = (
        ("type", "scalar-field"),
        ("dataLocation", 1),
        ("boundaryValues", False),
    )

    assert len(data()[scalar_field_tag]) == 2

    # Vector Field Data
    vector_data = data()[(("type", "vector-field"),)]
    assert len(vector_data) == 1
    assert len(vector_data[31]["phase-3:velocity"]) == 456


def test_error_handling_single_phase_deprecated():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()

    with pytest.raises(NotImplementedError):
        batch_1.add_pathlines_fields_request("SV_T", surfaces=[3, 5])

    with pytest.raises(NotImplementedError):
        field_data.get_pathlines_field_data("SV_T", surfaces=[3, 5])


def test_error_handling_multi_phase_deprecated():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    file_session = FileSession()
    file_session.read_case(case_file_name)
    file_session.read_data(data_file_name)

    field_data = file_session.fields.field_data

    batch_1 = field_data.new_batch()
    with pytest.raises(InvalidMultiPhaseFieldName):
        batch_1.add_scalar_fields_request("SV_WALL_YPLUS", surfaces=[29, 30])

    with pytest.raises(InvalidMultiPhaseFieldName):
        field_data.get_vector_field_data("velocity", surfaces=[34])[34].size

    with pytest.raises(InvalidFieldName):
        field_data.get_vector_field_data("phase-1:temperature", surfaces=[34])[34].size


def test_faces_connectivity_behaviour():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )
    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )
    file_session = FileSession(case_file_name, data_file_name)
    batch = file_session.fields.field_data.new_batch()
    vertices_and_faces_connectivity_request = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesConnectivity],
        surfaces=[3, 4],
    )
    data = batch.add_requests(vertices_and_faces_connectivity_request).get_response()
    assert data.get_field_data(vertices_and_faces_connectivity_request)[
        3
    ].vertices.shape == (3810, 3)
    assert (
        len(
            data.get_field_data(vertices_and_faces_connectivity_request)[4].connectivity
        )
        == 2018
    )
    del batch

    batch = file_session.fields.field_data.new_batch()
    vertices_and_faces_connectivity_request = SurfaceFieldDataRequest(
        data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesConnectivity],
        surfaces=[3, 4],
        flatten_connectivity=True,
    )
    data = batch.add_requests(vertices_and_faces_connectivity_request).get_response()
    assert data.get_field_data(vertices_and_faces_connectivity_request)[
        3
    ].vertices.shape == (3810, 3)
    assert data.get_field_data(vertices_and_faces_connectivity_request)[
        4
    ].connectivity.shape == (10090,)
