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

"""Wrapper over the text interface gRPC service of Fluent (v0 proto API)."""

from typing import Any

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v0 import datamodel_tui_pb2, datamodel_tui_pb2_grpc
from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.services._protocols import ServiceProtocol


class TextInterfaceService(ServiceProtocol):
    """Class wrapping the text interface gRPC service of Fluent (v0 proto API)."""

    def __init__(
        self,
        intercept_channel,
        metadata: list[tuple[str, str]],
    ) -> None:
        """__init__ method of TextInterfaceService class."""
        self._stub = datamodel_tui_pb2_grpc.DataModelStub(intercept_channel)
        self._metadata = metadata

    def get_attribute_value(
        self, path: str, attribute: str, include_unavailable: bool
    ) -> Any:
        """Get the attribute value."""
        request = datamodel_tui_pb2.GetAttributeValueRequest()
        request.path = path
        request.attribute = datamodel_tui_pb2.Attribute.Value(attribute.upper())
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._stub.GetAttributeValue(request, metadata=self._metadata)
        return _convert_gvalue_to_value(response.value)

    def get_state(
        self, request: datamodel_tui_pb2.GetStateRequest
    ) -> datamodel_tui_pb2.GetStateResponse:
        """GetState RPC of DataModel service."""
        return self._stub.GetState(request, metadata=self._metadata)

    def set_state(
        self, request: datamodel_tui_pb2.SetStateRequest
    ) -> datamodel_tui_pb2.SetStateResponse:
        """SetState RPC of DataModel service."""
        return self._stub.SetState(request, metadata=self._metadata)

    def execute_command(self, path: str, *args, **kwargs) -> Any:
        """Execute the command."""
        request = datamodel_tui_pb2.ExecuteCommandRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        return self._stub.ExecuteCommand(request, metadata=self._metadata)

    def execute_query(self, path: str, *args, **kwargs) -> Any:
        """Execute the query."""
        request = datamodel_tui_pb2.ExecuteQueryRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        return self._stub.ExecuteQuery(request, metadata=self._metadata)

    def get_static_info(self, path: str):
        """GetStaticInfo RPC of DataModel service."""
        request = datamodel_tui_pb2.GetStaticInfoRequest()
        request.path = path
        response = self._stub.GetStaticInfo(request, metadata=self._metadata)
        # Note: MessageToDict's parameter names are different in different protobuf versions
        return MessageToDict(response.info, True)

    def get_child_names(
        self, path: str, include_unavailable: bool = False
    ) -> list[str]:
        """Get the names of child menus."""
        attribute = datamodel_tui_pb2.Attribute.Name(
            datamodel_tui_pb2.Attribute.CHILD_NAMES
        ).lower()
        return self.get_attribute_value(path, attribute, include_unavailable)

    def get_doc_string(self, path: str, include_unavailable: bool = False) -> str:
        """Get docstring for a menu."""
        attribute = datamodel_tui_pb2.Attribute.Name(
            datamodel_tui_pb2.Attribute.HELP_STRING
        ).lower()
        return self.get_attribute_value(path, attribute, include_unavailable)


def _convert_value_to_gvalue(val: Any, gval: Variant) -> None:
    """Convert Python datatype to Value type of google/protobuf/struct.proto."""
    if isinstance(val, bool):
        gval.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gval.number_value = val
    elif isinstance(val, str):
        gval.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to list_value
        gval.list_value.values.add()
        gval.list_value.values.pop()
        for item in val:
            item_gval = gval.list_value.values.add()
            _convert_value_to_gvalue(item, item_gval)
    elif isinstance(val, dict):
        for k, v in val.items():
            _convert_value_to_gvalue(v, gval.struct_value.fields[k])


def _convert_gvalue_to_value(gval: Variant) -> Any:
    """Convert Value type of google/protobuf/struct.proto to Python datatype."""
    if gval.HasField("bool_value"):
        return gval.bool_value
    elif gval.HasField("number_value"):
        return gval.number_value
    elif gval.HasField("string_value"):
        return gval.string_value
    elif gval.HasField("list_value"):
        val = []
        for item in gval.list_value.values:
            val.append(_convert_gvalue_to_value(item))
        return val
    elif gval.HasField("struct_value"):
        val = {}
        for k, v in gval.struct_value.fields.items():
            val[k] = _convert_gvalue_to_value(v)
        return val
