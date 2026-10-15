# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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


def test_named_object_create_via_setitem(mixing_elbow_case_data_session_grpc_rest):
    """A named object can be created by assigning to a new key."""
    solver = mixing_elbow_case_data_session_grpc_rest
    solver.settings.solution.report_definitions.surface["test_surface"] = {
        "surface_names": ["cold-inlet"]
    }
    assert (
        "test_surface"
        in solver.settings.solution.report_definitions.surface.get_object_names()
    )
    state = solver.settings.solution.report_definitions.surface[
        "test_surface"
    ].get_state()
    assert state is not None


def test_named_object_delete_via_delitem(mixing_elbow_case_data_session_grpc_rest):
    """A named object can be removed with ``del``."""
    solver = mixing_elbow_case_data_session_grpc_rest
    solver.settings.solution.report_definitions.surface["deleteme"] = {
        "surface_names": ["cold-inlet"]
    }
    assert (
        "deleteme"
        in solver.settings.solution.report_definitions.surface.get_object_names()
    )
    del solver.settings.solution.report_definitions.surface["deleteme"]
    assert (
        "deleteme"
        not in solver.settings.solution.report_definitions.surface.get_object_names()
    )


def test_named_object_overwrite_existing(mixing_elbow_settings_session_grpc_rest):
    """Assigning to an existing key overwrites that object's state.

    Uses ``cold-inlet``, an existing boundary condition from the case -
    velocity_inlet is a physical mesh zone and is not user-creatable.
    """
    solver = mixing_elbow_settings_session_grpc_rest
    inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "momentum": {"velocity": 1.0}
    }
    assert inlet.momentum.velocity.value() == 1.0
    solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "momentum": {"velocity": 2.0}
    }
    assert inlet.momentum.velocity.value() == 2.0


def test_named_object_rename_command(mixing_elbow_settings_session_grpc_rest):
    """``rename`` renames an existing named object."""
    solver = mixing_elbow_settings_session_grpc_rest
    solver.settings.setup.boundary_conditions.velocity_inlet.rename(
        new="renamed_inlet", old="cold-inlet"
    )
    obj_names = (
        solver.settings.setup.boundary_conditions.velocity_inlet.get_object_names()
    )
    assert "cold-inlet" not in obj_names
    assert "renamed_inlet" in obj_names


def test_named_object_make_a_copy_command(mixing_elbow_settings_session_grpc_rest):
    """``make_a_copy`` duplicates a user-creatable named object."""
    solver = mixing_elbow_settings_session_grpc_rest
    solver.settings.solution.report_definitions.surface["surface-1"] = {
        "surface_names": ["cold-inlet"]
    }
    solver.settings.solution.report_definitions.surface.make_a_copy(
        from_="surface-1", to="copy_of_surface_1"
    )
    obj_names = solver.settings.solution.report_definitions.surface.get_object_names()
    assert "copy_of_surface_1" in obj_names
