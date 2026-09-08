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

"""Backward-compatible interfaces for Fluent.

This package provides legacy support for running local parametric studies and
reading or writing Fluent RP variables through :class:`LocalParametricStudy`
and :class:`RPVars`. It also contains the legacy workflow wrappers in
:mod:`ansys.fluent.core.legacy.workflow_old` and
:mod:`ansys.fluent.core.legacy.meshing_workflow_old`.
"""

from ansys.fluent.core.legacy.local_parametric_study import LocalParametricStudy
from ansys.fluent.core.legacy.rpvars import RPVars, RPVarType

__all__ = [
    "LocalParametricStudy",
    "RPVars",
    "RPVarType",
]
