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

"""Helpers for selecting compatible gRPC API modules across Fluent versions."""

from enum import Enum
import importlib
from typing import Any

from ansys.fluent.core.utils.fluent_version import FluentVersion


class GrpcApiVersion(Enum):
    """Supported Fluent API package generations."""

    V0 = "v0"
    V1 = "v1"


def get_grpc_api_version(
    fluent_version: str | FluentVersion | None,
) -> GrpcApiVersion:
    """Resolve gRPC API package generation from a Fluent version.

    Parameters
    ----------
    fluent_version : str | FluentVersion | None
        Fluent version string or enum value.

    Returns
    -------
    GrpcApiVersion
        ``V1`` for Fluent 27.1 and newer, otherwise ``V0``.
    """
    if fluent_version is None:
        return GrpcApiVersion.V1
    version = (
        fluent_version
        if isinstance(fluent_version, FluentVersion)
        else FluentVersion(fluent_version)
    )
    return GrpcApiVersion.V1 if version >= FluentVersion.v271 else GrpcApiVersion.V0


def import_fluent_api_module(module_name: str, grpc_api_version: GrpcApiVersion):
    """Import a Fluent generated API module for the selected package generation."""
    return importlib.import_module(
        f"ansys.api.fluent.{grpc_api_version.value}.{module_name}"
    )


def resolve_attr_first(obj: Any, *names: str) -> Any:
    """Return the first matching attribute from ``names``.

    Raises
    ------
    AttributeError
        If none of the provided names are present.
    """
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AttributeError(f"None of these attributes exist: {names}")
