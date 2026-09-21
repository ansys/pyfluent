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

"""Public field-data APIs.

The field-data implementation has a transport layer and a user-facing layer.
An implementation of :class:`AbstractFieldData` can use any kind of service,
such as gRPC or REST. :class:`LiveFieldData` wraps that implementation for users,
and :class:`Batch` collects requests for a single service call.
"""


from ansys.fluent.core.fields.field_data.abstract_field_data import (
    AbstractFieldData,
    BaseFieldDataSource,
    FieldDataSource,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
)
from ansys.fluent.core.fields.field_data.live_field_data import (
    LiveFieldData as FieldData,
)
from ansys.fluent.core.fields.field_data.live_field_data import Batch as FieldDataBatch

__all__ = [
    "AbstractFieldData",
    "BaseFieldDataSource",
    "FieldDataSource",
    "FieldData",
    "FieldDataBatch",
    "PathlinesFieldDataRequest",
    "ScalarFieldDataRequest",
    "SurfaceDataType",
    "SurfaceFieldDataRequest",
    "VectorFieldDataRequest",
]
