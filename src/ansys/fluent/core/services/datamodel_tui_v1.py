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

"""Wrappers over TUI-based datamodel gRPC service of Fluent (v1 proto API).

This module intentionally reuses the shared menu/runtime logic from
``datamodel_tui.py`` and keeps only v1-specific proto/stub/request differences.
"""

from typing import Any

import grpc

from ansys.api.fluent.v1 import datamodel_tui_pb2 as DataModelProtoModule
from ansys.api.fluent.v1 import datamodel_tui_pb2_grpc as DataModelGrpcModule
from ansys.fluent.core.services import (
    datamodel_tui as _v0,  # v0 base: shared menu/runtime logic is reused; only v1-specific proto/stub differences are overridden below
)

Path = _v0.Path
logger = _v0.logger

_convert_value_to_gvalue = _v0._convert_value_to_gvalue
_convert_gvalue_to_value = _v0._convert_gvalue_to_value

PyMenu = _v0.PyMenu
TUIMethod = _v0.TUIMethod
TUIMenu = _v0.TUIMenu
TUICommand = _v0.TUICommand

convert_tui_menu_to_func_name = _v0.convert_tui_menu_to_func_name
convert_path_to_grpc_path = _v0.convert_path_to_grpc_path


class DatamodelServiceImpl(_v0.DatamodelServiceImpl):
    """Class wrapping the TUI-based datamodel gRPC service of Fluent (v1)."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """Initialize DatamodelServiceImpl."""
        self._channel = channel
        self._fluent_error_state = fluent_error_state
        intercept_channel = grpc.intercept_channel(
            self._channel,
            _v0.GrpcErrorInterceptor(),
            _v0.ErrorStateInterceptor(self._fluent_error_state),
            _v0.TracingInterceptor(),
            _v0.BatchInterceptor(),
        )
        self._stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self._metadata = metadata


class DatamodelService(_v0.DatamodelService):
    """Pure Python wrapper of DatamodelServiceImpl (v1)."""

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
        fluent_error_state,
        app_utilities,
        scheme_eval,
    ) -> None:
        """Initialize DatamodelService."""
        self._impl = DatamodelServiceImpl(channel, metadata, fluent_error_state)
        self._app_utilities = app_utilities
        self._scheme_eval = scheme_eval

    @staticmethod
    def _normalize_attribute_name(attribute: str) -> str:
        name = attribute.upper()
        return name if name.startswith("ATTRIBUTE_") else f"ATTRIBUTE_{name}"

    def get_attribute_value(
        self, path: str, attribute: str, include_unavailable: bool
    ) -> Any:
        """Get the attribute value."""
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.Value(
            self._normalize_attribute_name(attribute)
        )
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._impl.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def execute_query(self, path: str, *args, **kwargs) -> Any:
        """Execute the query."""
        request = DataModelProtoModule.ExecuteQueryRequest()
        request.path = path
        if args or kwargs:
            logger.debug(
                "Ignoring query args for v1 TUI ExecuteQuery; request schema has no args field."
            )
        return self._impl.execute_query(request)
