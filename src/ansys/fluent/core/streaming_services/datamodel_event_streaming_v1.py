# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Provides a module for datamodel event streaming (v1 proto API)."""

from ansys.api.fluent.v1 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.services.datamodel_se_v1 import _convert_variant_to_value
from ansys.fluent.core.streaming_services.datamodel_event_streaming import (
    _BaseDatamodelEvents,
)


class DatamodelEvents(_BaseDatamodelEvents):
    """Encapsulates a datamodel events streaming service."""

    _streaming_rpc_path = (
        "/ansys.api.fluent.v1.datamodel_se.DataModelService/BeginEventStreaming"
    )

    def _make_request(self, *args, **kwargs):
        return DataModelProtoModule.BeginEventStreamingRequest(*args, **kwargs)

    def _has_created_event_response(self, response) -> bool:
        return response.HasField("created_event_response")

    def _get_created_event_child_type(self, response) -> str:
        return response.created_event_response.child_type

    def _get_created_event_child_name(self, response) -> str:
        return response.created_event_response.child_name

    def _has_attribute_changed_event_response(self, response) -> bool:
        return response.HasField("attribute_changed_event_response")

    def _get_attribute_changed_value(self, response):
        return response.attribute_changed_event_response.value

    def _has_command_attribute_changed_event_response(self, response) -> bool:
        return response.HasField("command_attribute_changed_event_response")

    def _get_command_attribute_changed_value(self, response):
        return response.command_attribute_changed_event_response.value

    def _has_modified_event_response(self, response) -> bool:
        return response.HasField("modified_event_response")

    def _get_modified_event_value(self, response):
        return response.modified_event_response.value

    def _has_affected_event_response(self, response) -> bool:
        return response.HasField("affected_event_response")

    def _has_deleted_event_response(self, response) -> bool:
        return response.HasField("deleted_event_response")

    def _has_command_executed_event_response(self, response) -> bool:
        return response.HasField("command_executed_event_response")

    def _get_command_executed_command(self, response) -> str:
        return response.command_executed_event_response.command

    def _get_command_executed_args(self, response):
        return response.command_executed_event_response.args

    def _convert_variant_to_value(self, value):
        return _convert_variant_to_value(value)
