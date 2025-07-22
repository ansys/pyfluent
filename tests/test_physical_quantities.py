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

"""
Tests for `PhysicalQuantity` objects.
"""

import pytest

import ansys.fluent.core as pf  # noqa: F401
from ansys.fluent.core import (
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    examples,
)
from ansys.fluent.core.file_session import FileSession
from ansys.units.variable_descriptor import VariableCatalog


def round_off_list_elements(input_list):
    """
    A function to round off list elements.
    """
    for index, value in enumerate(input_list):
        input_list[index] = round(value, 6)

    return input_list


@pytest.mark.fluent_version(">=24.1")
@pytest.mark.developer_only
def test_use_variable_catalog(new_solver_session) -> None:
    """
    A test of `PhysicalQuantity` objects.
    """
    solver = new_solver_session
    settings = solver.settings

    case_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    settings.file.read(file_type="case", file_name=case_name)

    settings.solution.initialization.hybrid_initialize()

    fields = solver.fields

    temperature = VariableCatalog.TEMPERATURE
    locations = ["hot-inlet"]

    temperature_field_data = fields.field_data.get_field_data(
        ScalarFieldDataRequest(
            field_name=VariableCatalog.TEMPERATURE, surfaces=locations
        )
    )
    assert round(temperature_field_data[locations[0]][0]) == 305

    temperature_min = fields.reduction.minimum(
        expression=temperature, locations=locations
    )
    assert round(temperature_min) == 313

    temperature_solution_data = fields.solution_variable_data.get_data(
        variable_name=temperature, zone_names=locations
    )
    assert round(temperature_solution_data[locations[0]][0]) == 313

    report_defs = settings.solution.report_definitions
    report_defs.surface["yyy"] = {}
    surface = report_defs.surface["yyy"]
    surface.report_type = "surface-areaavg"
    surface.field = temperature
    surface.surface_names = locations

    result = report_defs.compute(report_defs=["yyy"])
    assert round(result[0]["yyy"][0]) == 313


@pytest.mark.developer_only
def test_use_variable_catalog_offline():
    """
    A test of `PhysicalQuantity` objects for offline data.
    """
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
        file_session.field_data.scalar_fields.range(VariableCatalog.PRESSURE)
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
    sv_t_wall_request = ScalarFieldDataRequest(
        field_name=VariableCatalog.TEMPERATURE, surfaces=["wall"]
    )
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
    assert list(surface_data_symmetry_deprecated["symmetry"][1000]) == [
        1259,
        1260,
        1227,
        1226,
    ]

    vector_data = file_session.fields.field_data.get_field_data
    vector_data_request = VectorFieldDataRequest(
        field_name=VariableCatalog.VELOCITY, surfaces=["wall"]
    )
    assert vector_data(vector_data_request)["wall"].shape == (3630, 3)

    vector_data_symmetry_request = VectorFieldDataRequest(
        field_name=VariableCatalog.VELOCITY, surfaces=["symmetry"]
    )
    vector_data_symmetry = vector_data(vector_data_symmetry_request)["symmetry"]
    assert vector_data_symmetry.shape == (2018, 3)
    assert round(vector_data_symmetry[1009][0], 5) == 0.0023
    assert round(vector_data_symmetry[1009][1], 5) == 1.22311


def test_quantity_dimensions_subscription():
    from ansys.units.variable_descriptor import VariableCatalog as vc

    vel = vc.VELOCITY
    assert vel.name == "velocity"
    assert vel.dimension["TIME"] == -1.0
    assert vel.dimension["LENGTH"] == 1.0
