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

"""Deprecated PyFluent APIs."""

PYFLUENT_DEPRECATED_DATA = [
    # Target, Deprecated, Alternatives
    # methods
    (
        ":py:meth:`ansys.fluent.core.services.scheme_eval.SchemeEval.scheme_eval <ansys.fluent.core.services.scheme_eval.SchemeEval.scheme_eval>`",
        "0.32",
        ":py:meth:`ansys.fluent.core.services.scheme_eval.SchemeEval.eval <ansys.fluent.core.services.scheme_eval.SchemeEval.eval>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.scheme_eval <ansys.fluent.core.session.BaseSession.scheme_eval>`",
        "0.32",
        ":py:meth:`ansys.fluent.core.session.BaseSession.scheme <ansys.fluent.core.session.BaseSession.scheme>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.fluent_connection.FluentConnection.health_check <ansys.fluent.core.fluent_connection.FluentConnection.health_check>`",
        "0.32",
        "N/A",
    ),
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.health_check <ansys.fluent.core.session.BaseSession.health_check>`",
        "0.32",
        ":py:meth:`ansys.fluent.core.session.BaseSession.is_active <ansys.fluent.core.session.BaseSession.is_active>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.is_server_healthy <ansys.fluent.core.session.BaseSession.is_server_healthy>`",
        "0.38",
        ":py:meth:`ansys.fluent.core.session.BaseSession.is_active <ansys.fluent.core.session.BaseSession.is_active>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_surfaces_request <ansys.fluent.core.file_session.Transaction.add_surfaces_request>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_requests <ansys.fluent.core.file_session.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_scalar_fields_request <ansys.fluent.core.file_session.Transaction.add_scalar_fields_request>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_requests <ansys.fluent.core.file_session.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_vector_fields_request <ansys.fluent.core.file_session.Transaction.add_vector_fields_request>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.Transaction.add_requests <ansys.fluent.core.file_session.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_surface_data <ansys.fluent.core.file_session.FileFieldData.get_surface_data>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_field_data <ansys.fluent.core.file_session.FileFieldData.get_field_data>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data <ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_field_data <ansys.fluent.core.file_session.FileFieldData.get_field_data>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_vector_field_data <ansys.fluent.core.file_session.FileFieldData.get_vector_field_data>`",
        "0.25.0",
        ":py:meth:`ansys.fluent.core.file_session.FileFieldData.get_field_data <ansys.fluent.core.file_session.FileFieldData.get_field_data>`",
    ),
    # class
    (
        ":py:class:`ansys.fluent.core.services.field_data.FieldInfo <ansys.fluent.core.services.field_data.FieldInfo>`",
        "0.34.0",
        ":py:class:`ansys.fluent.core.services.field_data.FieldData <ansys.fluent.core.services.field_data.FieldData>`",
    ),
    # properties
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.field_info <ansys.fluent.core.session.BaseSession.field_info>`",
        "0.20.dev9",
        "`session.fields.field_info`",
    ),
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.field_data <ansys.fluent.core.session.BaseSession.field_data>`",
        "0.20.dev9",
        "`session.fields.field_data`",
    ),
    (
        ":py:meth:`ansys.fluent.core.session.BaseSession.field_data_streaming <ansys.fluent.core.session.BaseSession.field_data_streaming>`",
        "0.20.dev9",
        "`session.fields.field_data_streaming`",
    ),
    (
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_surfaces_request <ansys.fluent.core.services.field_data.Transaction.add_surfaces_request>`",
        "0.23.dev0",
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_requests <ansys.fluent.core.services.field_data.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_scalar_fields_request <ansys.fluent.core.services.field_data.Transaction.add_scalar_fields_request>`",
        "0.23.dev0",
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_requests <ansys.fluent.core.services.field_data.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request <ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request>`",
        "0.23.dev0",
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_requests <ansys.fluent.core.services.field_data.Transaction.add_requests>`",
    ),
    (
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request <ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request>`",
        "0.23.dev0",
        ":py:meth:`ansys.fluent.core.services.field_data.Transaction.add_requests <ansys.fluent.core.services.field_data.Transaction.add_requests>`",
    ),
    # arguments
    (
        "``timeout`` argument of :py:func:`ansys.fluent.core.launcher.fluent_container.configure_container_dict <ansys.fluent.core.launcher.fluent_container.configure_container_dict>`",
        "0.34.dev0",
        "``start_timeout`` argument of :py:func:`ansys.fluent.core.launcher.launcher.launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_surfaces_request <ansys.fluent.core.file_session.Transaction.add_surfaces_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_scalar_fields_request <ansys.fluent.core.file_session.Transaction.add_scalar_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_vector_fields_request <ansys.fluent.core.file_session.Transaction.add_vector_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_pathlines_fields_request <ansys.fluent.core.file_session.Transaction.add_pathlines_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_surfaces_request <ansys.fluent.core.file_session.Transaction.add_surfaces_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_scalar_fields_request <ansys.fluent.core.file_session.Transaction.add_scalar_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_vector_fields_request <ansys.fluent.core.file_session.Transaction.add_vector_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.Transaction.add_pathlines_fields_request <ansys.fluent.core.file_session.Transaction.add_pathlines_fields_request>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_surface_data <ansys.fluent.core.file_session.FileFieldData.get_surface_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data <ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_vector_field_data <ansys.fluent.core.file_session.FileFieldData.get_vector_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_pathlines_field_data <ansys.fluent.core.file_session.FileFieldData.get_pathlines_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_surface_data <ansys.fluent.core.file_session.FileFieldData.get_surface_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data <ansys.fluent.core.file_session.FileFieldData.get_scalar_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_vector_field_data <ansys.fluent.core.file_session.FileFieldData.get_vector_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.file_session.FileFieldData.get_pathlines_field_data <ansys.fluent.core.file_session.FileFieldData.get_pathlines_field_data>`",
        "0.25.0",
        "`surfaces`",
    ),
    (
        "The `container_mount_path` argument of :py:meth:`ansys.fluent.core.utils.file_transfer_service.ContainerFileTransferStrategy <ansys.fluent.core.utils.file_transfer_service.ContainerFileTransferStrategy>`",
        "0.23.dev1",
        "`mount_target`",
    ),
    (
        "The `host_mount_path` argument of :py:meth:`ansys.fluent.core.utils.file_transfer_service.ContainerFileTransferStrategy <ansys.fluent.core.utils.file_transfer_service.ContainerFileTransferStrategy>`",
        "0.23.dev1",
        "`mount_source`",
    ),
    (
        "The `container_mount_path` argument of :py:func:`ansys.fluent.core.launcher.fluent_container.configure_container_dict <ansys.fluent.core.launcher.fluent_container.configure_container_dict>`",
        "0.23.dev1",
        "`mount_target`",
    ),
    (
        "The `host_mount_path` argument of :py:func:`ansys.fluent.core.launcher.fluent_container.configure_container_dict <ansys.fluent.core.launcher.fluent_container.configure_container_dict>`",
        "0.23.dev1",
        "`mount_source`",
    ),
    (
        "The `show_gui` argument of :py:func:`ansys.fluent.core.launcher.launcher.launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`",
        "0.22.dev0",
        "`ui_mode`",
    ),
    (
        "The `version` argument of :py:func:`ansys.fluent.core.launcher.launcher.launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`",
        "0.22.dev0",
        "`dimension`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_surfaces_request <ansys.fluent.core.services.field_data.Transaction.add_surfaces_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`nsys.fluent.core.services.field_data.Transaction.add_scalar_fields_request <ansys.fluent.core.services.field_data.Transaction.add_scalar_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request <ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_names` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request <ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_surfaces_request <ansys.fluent.core.services.field_data.Transaction.add_surfaces_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_scalar_fields_request <ansys.fluent.core.services.field_data.Transaction.add_scalar_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request <ansys.fluent.core.services.field_data.Transaction.add_vector_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    (
        "The `surface_ids` argument of :py:meth:`ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request <ansys.fluent.core.services.field_data.Transaction.add_pathlines_fields_request>`",
        "0.23.dev0",
        "`surfaces`",
    ),
    # Environment variables
    (
        "The `PYFLUENT_USE_DOCKER_COMPOSE` environment variable",
        "0.34.0",
        "``use_docker_compose`` argument of :py:func:`ansys.fluent.core.launcher.launcher.launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`",
    ),
    (
        "The `PYFLUENT_USE_PODMAN_COMPOSE` environment variable",
        "0.34.0",
        "``use_podman_compose`` argument of :py:func:`ansys.fluent.core.launcher.launcher.launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`",
    ),
]
