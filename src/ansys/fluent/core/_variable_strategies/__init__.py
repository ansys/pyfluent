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

"""Map PyFluent variable descriptors to Fluent variable names.

The package provides naming strategies for Fluent expressions, field-data
variables, and solution variables. These strategies translate PyFluent
``VariableDescriptor`` objects into the names expected by Fluent services and
can be selected according to the type of data being accessed.
"""

from .expr import FluentExprNamingStrategy  # noqa: F401
from .field import FluentFieldDataNamingStrategy  # noqa: F401
from .svar import FluentSVarNamingStrategy  # noqa: F401

__all__ = [
    "FluentExprNamingStrategy",
    "FluentFieldDataNamingStrategy",
    "FluentSVarNamingStrategy",
]
