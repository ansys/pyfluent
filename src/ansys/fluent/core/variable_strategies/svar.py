# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""
Provides a ConversionStrategy for mapping VariableDescriptor to Fluent's SVAR names.
"""


from ansys.units.variable_descriptor import (
    MappingConversionStrategy,
    VariableCatalog,
)


class FluentSVarNamingStrategy(MappingConversionStrategy):
    """This strategy handles conversion of selected VariableCatalog into Fluent's
    server-side field variable naming conventions (e.g., "SV_P" for pressure).
    """

    _c = VariableCatalog

    _mapping = {
        # pressure
        _c.PRESSURE: "SV_P",
        _c.STATIC_PRESSURE: "SV_P",
        # velocity
        _c.VELOCITY_X: "SV_U",
        _c.VELOCITY_Y: "SV_V",
        _c.VELOCITY_Z: "SV_W",
        # density
        _c.DENSITY: "SV_DENSITY",
        # temperature
        _c.SPECIFIC_ENTHALPY: "SV_H",
        _c.TEMPERATURE: "SV_T",
    }
