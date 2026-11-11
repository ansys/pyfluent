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

"""Solver-agnostic value types for the settings/object state tree.

These aliases describe the values that flow in and out of a settings backend
(scalars, lists, vectors, and nested group/list states). They live in the
platform layer so the transport and service contracts can reference them
without depending on Fluent's object framework (``flobject``). ``flobject``
re-exports these names for backward compatibility.
"""

from typing import NewType, Union

RealType = NewType("real", float | str)  # constant or expression
RealListType = list[RealType]
RealVectorType = tuple[RealType, RealType, RealType]
IntListType = list[int]
StringListType = list[str]
BoolListType = list[bool]
PrimitiveStateType = Union[
    str,
    RealType,
    int,
    bool,
    RealListType,
    IntListType,
    StringListType,
    BoolListType,
]
DictStateType = dict[str, "StateType"]
ListStateType = list["StateType"]
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]
