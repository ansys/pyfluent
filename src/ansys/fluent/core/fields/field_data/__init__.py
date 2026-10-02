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

"""Public APIs for retrieving Fluent field data and mesh data.

Use :class:`FieldData` with request models such as
:class:`ScalarFieldDataRequest`. Response and mesh models are also available
here for inspection and type annotations.
"""

from ansys.fluent.core.fields.field_data.abstract_field_data import (
    AbstractFieldData,
    BaseFieldDataSource,
    FieldBatch,
    FieldDataSource,
)
from ansys.fluent.core.fields.field_data.data_types import PathlinesData, SurfaceData
from ansys.fluent.core.fields.field_data.live_field_data import (
    Batch,
    BatchFieldData,
    LiveFieldData,
)
from ansys.fluent.core.fields.field_data.mesh import (
    CellElementType,
    Element,
    Facet,
    Mesh,
    Node,
    ZoneInfo,
    ZoneType,
)
from ansys.fluent.core.fields.field_data.requests import (
    BaseDataRequest,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
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
    "FieldBatch",
    "FieldData",
    "FieldDataBatch",
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
]

FieldData = LiveFieldData
FieldDataBatch = Batch
