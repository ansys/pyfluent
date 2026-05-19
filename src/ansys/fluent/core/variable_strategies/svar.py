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

"""
Provides ConversionStrategy classes for mapping VariableDescriptor to Fluent's SVAR names,
separated by field kind (scalar vs. vector).
"""


from ansys.units.variable_descriptor import (
    MappingConversionStrategy,
    VariableCatalog,
)


class FluentSVarScalarNamingStrategy(MappingConversionStrategy):
    """Maps scalar VariableDescriptor entries to Fluent SVAR scalar variable names.

    Use this strategy when requesting scalar solution variable data.
    Scalar SVARs return a single float per cell (e.g., ``SV_P`` for pressure).
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


class FluentSVarVectorNamingStrategy(MappingConversionStrategy):
    """Placeholder strategy for Fluent SVAR vector variable names.

    Fluent's SVAR service does **not** expose named vector quantities.
    Multi-component fields such as velocity are stored as individual scalar
    SVARs (``SV_U``, ``SV_V``, ``SV_W``) and must be requested one component
    at a time via :class:`FluentSVarScalarNamingStrategy`.

    Consequently ``_mapping`` is intentionally empty and :meth:`supports`
    returns ``False`` for every descriptor.  This class exists solely for
    structural parity with the field-data and expression strategy modules;
    callers should use :class:`FluentSVarScalarNamingStrategy` for all SVAR
    lookups, including velocity components.
    """

    _c = VariableCatalog

    _mapping = {}


class FluentSVarNamingStrategy(MappingConversionStrategy):
    """Combined scalar + vector strategy for Fluent SVAR variable names.

    Merges :class:`FluentSVarScalarNamingStrategy` and
    :class:`FluentSVarVectorNamingStrategy` into a single lookup.
    Retained for backwards compatibility; prefer the specific sub-strategies
    when the field kind (scalar vs. vector) is known at the call site.
    """

    _mapping = {
        **FluentSVarScalarNamingStrategy._mapping,
        **FluentSVarVectorNamingStrategy._mapping,
    }
