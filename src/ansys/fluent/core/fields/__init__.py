# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Public APIs for Fluent field data, reductions, and solution variables.

The :mod:`field_data` package provides request, response, and mesh models for
retrieving data from Fluent. :class:`Reduction`, :class:`SolutionVariableInfo`,
and :class:`SolutionVariableData` provide the related post-processing APIs.
"""

from ansys.fluent.core.fields.field_data import (
    AbstractFieldData,
    BaseDataRequest,
    BaseFieldDataSource,
    Batch,
    BatchFieldData,
    CellElementType,
    Element,
    Facet,
    FieldBatch,
    FieldData,
    FieldDataBatch,
    FieldDataSource,
    LiveFieldData,
    Mesh,
    Node,
    PathlinesData,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceData,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    ZoneInfo,
    ZoneType,
)
from ansys.fluent.core.fields.reduction import Reduction
from ansys.fluent.core.fields.solution_variables import (
    SolutionVariableData,
    SolutionVariableInfo,
)

__all__ = [
    "AbstractFieldData",
    "BaseDataRequest",
    "BaseFieldDataSource",
    "Batch",
    "BatchFieldData",
    "CellElementType",
    "Element",
    "Facet",
    "FieldDataSource",
    "FieldData",
    "FieldDataBatch",
    "FieldBatch",
    "LiveFieldData",
    "Mesh",
    "Node",
    "PathlinesData",
    "PathlinesFieldDataRequest",
    "ScalarFieldDataRequest",
    "SurfaceData",
    "SurfaceDataType",
    "SurfaceFieldDataRequest",
    "VectorFieldDataRequest",
    "ZoneInfo",
    "ZoneType",
    "Reduction",
    "SolutionVariableInfo",
    "SolutionVariableData",
]
