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
Unit tests for the scalar/vector segregation in variable_strategies
(field, expr, and svar modules).

Covers:
- Correct to_string output for known scalar and vector descriptors
- to_string raises ValueError for descriptors not in a sub-strategy
- to_string passthrough for raw strings and None (MappingConversionStrategy contract)
- supports() correctness for each sub-strategy and the combined class
- to_variable_descriptor round-trips and returns None for unknown strings
- Strict segregation: scalar keys absent from vector mapping and vice versa
- Combined (backward-compat) classes are the union of their sub-strategies
- SVarVectorNamingStrategy is intentionally empty (no Fluent vector SVARs yet)
"""

import pytest

from ansys.fluent.core.variable_strategies import (
    FluentExprNamingStrategy,
    FluentExprScalarNamingStrategy,
    FluentExprVectorNamingStrategy,
    FluentFieldDataNamingStrategy,
    FluentFieldDataScalarNamingStrategy,
    FluentFieldDataVectorNamingStrategy,
    FluentSVarNamingStrategy,
    FluentSVarScalarNamingStrategy,
    FluentSVarVectorNamingStrategy,
)
from ansys.units.variable_descriptor import VariableCatalog

_vc = VariableCatalog


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def field_scalar():
    return FluentFieldDataScalarNamingStrategy()


@pytest.fixture
def field_vector():
    return FluentFieldDataVectorNamingStrategy()


@pytest.fixture
def field_combined():
    return FluentFieldDataNamingStrategy()


@pytest.fixture
def expr_scalar():
    return FluentExprScalarNamingStrategy()


@pytest.fixture
def expr_vector():
    return FluentExprVectorNamingStrategy()


@pytest.fixture
def expr_combined():
    return FluentExprNamingStrategy()


@pytest.fixture
def svar_scalar():
    return FluentSVarScalarNamingStrategy()


@pytest.fixture
def svar_vector():
    return FluentSVarVectorNamingStrategy()


@pytest.fixture
def svar_combined():
    return FluentSVarNamingStrategy()


# ---------------------------------------------------------------------------
# MappingConversionStrategy contract (string / None passthrough)
# These tests apply to every strategy class uniformly.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "strategy_fixture",
    [
        "field_scalar",
        "field_vector",
        "field_combined",
        "expr_scalar",
        "expr_vector",
        "expr_combined",
        "svar_scalar",
        "svar_vector",
        "svar_combined",
    ],
)
def test_to_string_passthrough_for_plain_string(strategy_fixture, request):
    """to_string returns the input unchanged when given a plain string."""
    strategy = request.getfixturevalue(strategy_fixture)
    assert strategy.to_string("my-custom-field") == "my-custom-field"
    assert strategy.to_string("pressure") == "pressure"


@pytest.mark.parametrize(
    "strategy_fixture",
    [
        "field_scalar",
        "field_vector",
        "field_combined",
        "expr_scalar",
        "expr_vector",
        "expr_combined",
        "svar_scalar",
        "svar_vector",
        "svar_combined",
    ],
)
def test_to_string_passthrough_for_none(strategy_fixture, request):
    """to_string returns None when given None."""
    strategy = request.getfixturevalue(strategy_fixture)
    assert strategy.to_string(None) is None


# ---------------------------------------------------------------------------
# Field data — scalar strategy
# ---------------------------------------------------------------------------


class TestFluentFieldDataScalarNamingStrategy:
    def test_pressure(self, field_scalar):
        assert field_scalar.to_string(_vc.PRESSURE) == "pressure"

    def test_static_pressure_alias(self, field_scalar):
        assert field_scalar.to_string(_vc.STATIC_PRESSURE) == "pressure"

    def test_temperature(self, field_scalar):
        assert field_scalar.to_string(_vc.TEMPERATURE) == "temperature"

    def test_velocity_x_component(self, field_scalar):
        assert field_scalar.to_string(_vc.VELOCITY_X) == "x-velocity"

    def test_velocity_y_component(self, field_scalar):
        assert field_scalar.to_string(_vc.VELOCITY_Y) == "y-velocity"

    def test_velocity_z_component(self, field_scalar):
        assert field_scalar.to_string(_vc.VELOCITY_Z) == "z-velocity"

    def test_wall_y_plus(self, field_scalar):
        assert field_scalar.to_string(_vc.WALL_Y_PLUS) == "y-plus"

    def test_cell_volume(self, field_scalar):
        assert field_scalar.to_string(_vc.mesh.CELL_VOLUME) == "cell-volume"

    def test_vector_velocity_not_supported(self, field_scalar):
        """Whole-vector VELOCITY must not be in the scalar strategy."""
        assert not field_scalar.supports(_vc.VELOCITY)
        with pytest.raises(ValueError):
            field_scalar.to_string(_vc.VELOCITY)

    def test_vector_vorticity_not_supported(self, field_scalar):
        assert not field_scalar.supports(_vc.VORTICITY)
        with pytest.raises(ValueError):
            field_scalar.to_string(_vc.VORTICITY)

    def test_vector_mesh_velocity_not_supported(self, field_scalar):
        assert not field_scalar.supports(_vc.MESH_VELOCITY)
        with pytest.raises(ValueError):
            field_scalar.to_string(_vc.MESH_VELOCITY)

    def test_vector_wall_shear_stress_not_supported(self, field_scalar):
        assert not field_scalar.supports(_vc.WALL_SHEAR_STRESS)
        with pytest.raises(ValueError):
            field_scalar.to_string(_vc.WALL_SHEAR_STRESS)


# ---------------------------------------------------------------------------
# Field data — vector strategy
# ---------------------------------------------------------------------------


class TestFluentFieldDataVectorNamingStrategy:
    def test_velocity(self, field_vector):
        assert field_vector.to_string(_vc.VELOCITY) == "velocity"

    def test_mesh_velocity(self, field_vector):
        assert field_vector.to_string(_vc.MESH_VELOCITY) == "mesh-velocity"

    def test_vorticity(self, field_vector):
        assert field_vector.to_string(_vc.VORTICITY) == "vorticity"

    def test_wall_shear_stress(self, field_vector):
        assert field_vector.to_string(_vc.WALL_SHEAR_STRESS) == "wall-shear"

    def test_pressure_not_supported(self, field_vector):
        """Scalar PRESSURE must not be in the vector strategy."""
        assert not field_vector.supports(_vc.PRESSURE)
        with pytest.raises(ValueError):
            field_vector.to_string(_vc.PRESSURE)

    def test_velocity_x_component_not_supported(self, field_vector):
        """Component VELOCITY_X must not be in the vector strategy."""
        assert not field_vector.supports(_vc.VELOCITY_X)
        with pytest.raises(ValueError):
            field_vector.to_string(_vc.VELOCITY_X)


# ---------------------------------------------------------------------------
# Field data — combined (backward-compat) strategy
# ---------------------------------------------------------------------------


class TestFluentFieldDataNamingStrategy:
    def test_combined_contains_scalar_entries(self, field_combined):
        assert field_combined.to_string(_vc.PRESSURE) == "pressure"
        assert field_combined.to_string(_vc.TEMPERATURE) == "temperature"
        assert field_combined.to_string(_vc.VELOCITY_X) == "x-velocity"

    def test_combined_contains_vector_entries(self, field_combined):
        assert field_combined.to_string(_vc.VELOCITY) == "velocity"
        assert field_combined.to_string(_vc.VORTICITY) == "vorticity"
        assert field_combined.to_string(_vc.WALL_SHEAR_STRESS) == "wall-shear"

    def test_combined_mapping_is_superset(self):
        """Combined _mapping must contain every key from both sub-strategies."""
        combined_keys = set(FluentFieldDataNamingStrategy._mapping.keys())
        scalar_keys = set(FluentFieldDataScalarNamingStrategy._mapping.keys())
        vector_keys = set(FluentFieldDataVectorNamingStrategy._mapping.keys())
        assert scalar_keys.issubset(combined_keys)
        assert vector_keys.issubset(combined_keys)

    def test_scalar_vector_disjoint(self):
        """Scalar and vector field data mappings must not share any keys."""
        scalar_keys = set(FluentFieldDataScalarNamingStrategy._mapping.keys())
        vector_keys = set(FluentFieldDataVectorNamingStrategy._mapping.keys())
        assert scalar_keys.isdisjoint(vector_keys)


# ---------------------------------------------------------------------------
# Expr — scalar strategy
# ---------------------------------------------------------------------------


class TestFluentExprScalarNamingStrategy:
    def test_pressure(self, expr_scalar):
        assert expr_scalar.to_string(_vc.PRESSURE) == "StaticPressure"

    def test_static_pressure_alias(self, expr_scalar):
        assert expr_scalar.to_string(_vc.STATIC_PRESSURE) == "StaticPressure"

    def test_temperature(self, expr_scalar):
        assert expr_scalar.to_string(_vc.TEMPERATURE) == "StaticTemperature"

    def test_velocity_x_component(self, expr_scalar):
        assert expr_scalar.to_string(_vc.VELOCITY_X) == "Velocity.x"

    def test_velocity_y_component(self, expr_scalar):
        assert expr_scalar.to_string(_vc.VELOCITY_Y) == "Velocity.y"

    def test_velocity_z_component(self, expr_scalar):
        assert expr_scalar.to_string(_vc.VELOCITY_Z) == "Velocity.z"

    def test_vorticity_x_component(self, expr_scalar):
        assert expr_scalar.to_string(_vc.VORTICITY_X) == "Vorticity.x"

    def test_wall_shear_stress_x_component(self, expr_scalar):
        assert (
            expr_scalar.to_string(_vc.WALL_SHEAR_STRESS_X) == "WallShearStressVector.x"
        )

    def test_wall_shear_stress_magnitude(self, expr_scalar):
        assert (
            expr_scalar.to_string(_vc.WALL_SHEAR_STRESS_MAGNITUDE)
            == "WallShearStressVector.mag"
        )

    def test_dvelocity_dx_x_component(self, expr_scalar):
        assert expr_scalar.to_string(_vc.fluent.DVELOCITY_DX_X) == "dVelocitydx.x"

    def test_dvelocity_dx_magnitude(self, expr_scalar):
        assert (
            expr_scalar.to_string(_vc.fluent.DVELOCITY_DX_MAGNITUDE)
            == "dVelocitydx.mag"
        )

    def test_turbulent_kinetic_energy(self, expr_scalar):
        assert (
            expr_scalar.to_string(_vc.TURBULENT_KINETIC_ENERGY)
            == "TurbulentKineticEnergyk"
        )

    def test_cell_volume(self, expr_scalar):
        assert expr_scalar.to_string(_vc.mesh.CELL_VOLUME) == "CellVolume"

    def test_position_x(self, expr_scalar):
        assert expr_scalar.to_string(_vc.POSITION_X) == "Position.x"

    def test_whole_velocity_vector_not_supported(self, expr_scalar):
        """Whole-vector VELOCITY must not be in the scalar strategy."""
        assert not expr_scalar.supports(_vc.VELOCITY)
        with pytest.raises(ValueError):
            expr_scalar.to_string(_vc.VELOCITY)

    def test_vorticity_vector_not_supported(self, expr_scalar):
        assert not expr_scalar.supports(_vc.VORTICITY)
        with pytest.raises(ValueError):
            expr_scalar.to_string(_vc.VORTICITY)

    def test_mesh_velocity_vector_not_supported(self, expr_scalar):
        assert not expr_scalar.supports(_vc.MESH_VELOCITY)
        with pytest.raises(ValueError):
            expr_scalar.to_string(_vc.MESH_VELOCITY)

    def test_wall_shear_stress_vector_not_supported(self, expr_scalar):
        assert not expr_scalar.supports(_vc.WALL_SHEAR_STRESS)
        with pytest.raises(ValueError):
            expr_scalar.to_string(_vc.WALL_SHEAR_STRESS)

    def test_dvelocity_dx_vector_not_supported(self, expr_scalar):
        """dVelocitydx (the 3-component gradient row) must not be in scalar."""
        assert not expr_scalar.supports(_vc.fluent.DVELOCITY_DX)
        with pytest.raises(ValueError):
            expr_scalar.to_string(_vc.fluent.DVELOCITY_DX)

    def test_dvelocity_dy_vector_not_supported(self, expr_scalar):
        assert not expr_scalar.supports(_vc.fluent.DVELOCITY_DY)

    def test_dvelocity_dz_vector_not_supported(self, expr_scalar):
        assert not expr_scalar.supports(_vc.fluent.DVELOCITY_DZ)


# ---------------------------------------------------------------------------
# Expr — vector strategy
# ---------------------------------------------------------------------------


class TestFluentExprVectorNamingStrategy:
    def test_velocity(self, expr_vector):
        assert expr_vector.to_string(_vc.VELOCITY) == "Velocity"

    def test_mesh_velocity(self, expr_vector):
        assert expr_vector.to_string(_vc.MESH_VELOCITY) == "MeshVelocity"

    def test_vorticity(self, expr_vector):
        assert expr_vector.to_string(_vc.VORTICITY) == "Vorticity"

    def test_wall_shear_stress(self, expr_vector):
        assert expr_vector.to_string(_vc.WALL_SHEAR_STRESS) == "WallShearStressVector"

    def test_dvelocity_dx(self, expr_vector):
        assert expr_vector.to_string(_vc.fluent.DVELOCITY_DX) == "dVelocitydx"

    def test_dvelocity_dy(self, expr_vector):
        assert expr_vector.to_string(_vc.fluent.DVELOCITY_DY) == "dVelocitydy"

    def test_dvelocity_dz(self, expr_vector):
        assert expr_vector.to_string(_vc.fluent.DVELOCITY_DZ) == "dVelocitydz"

    def test_pressure_not_supported(self, expr_vector):
        assert not expr_vector.supports(_vc.PRESSURE)
        with pytest.raises(ValueError):
            expr_vector.to_string(_vc.PRESSURE)

    def test_velocity_x_component_not_supported(self, expr_vector):
        """Component VELOCITY_X is scalar — must not be in vector strategy."""
        assert not expr_vector.supports(_vc.VELOCITY_X)
        with pytest.raises(ValueError):
            expr_vector.to_string(_vc.VELOCITY_X)

    def test_dvelocity_dx_x_component_not_supported(self, expr_vector):
        """Scalar component dVelocitydx.x must not be in vector strategy."""
        assert not expr_vector.supports(_vc.fluent.DVELOCITY_DX_X)
        with pytest.raises(ValueError):
            expr_vector.to_string(_vc.fluent.DVELOCITY_DX_X)


# ---------------------------------------------------------------------------
# Expr — combined (backward-compat) strategy
# ---------------------------------------------------------------------------


class TestFluentExprNamingStrategy:
    def test_combined_contains_scalar_entries(self, expr_combined):
        assert expr_combined.to_string(_vc.PRESSURE) == "StaticPressure"
        assert expr_combined.to_string(_vc.VELOCITY_X) == "Velocity.x"
        assert (
            expr_combined.to_string(_vc.WALL_SHEAR_STRESS_MAGNITUDE)
            == "WallShearStressVector.mag"
        )

    def test_combined_contains_vector_entries(self, expr_combined):
        assert expr_combined.to_string(_vc.VELOCITY) == "Velocity"
        assert expr_combined.to_string(_vc.VORTICITY) == "Vorticity"
        assert expr_combined.to_string(_vc.fluent.DVELOCITY_DX) == "dVelocitydx"

    def test_combined_mapping_is_superset(self):
        """Combined _mapping must be exactly the union of scalar + vector."""
        combined_keys = set(FluentExprNamingStrategy._mapping.keys())
        scalar_keys = set(FluentExprScalarNamingStrategy._mapping.keys())
        vector_keys = set(FluentExprVectorNamingStrategy._mapping.keys())
        assert scalar_keys.issubset(combined_keys)
        assert vector_keys.issubset(combined_keys)

    def test_scalar_vector_disjoint(self):
        """Scalar and vector expr mappings must not share any keys."""
        scalar_keys = set(FluentExprScalarNamingStrategy._mapping.keys())
        vector_keys = set(FluentExprVectorNamingStrategy._mapping.keys())
        assert scalar_keys.isdisjoint(vector_keys)


# ---------------------------------------------------------------------------
# SVAR — scalar strategy
# ---------------------------------------------------------------------------


class TestFluentSVarScalarNamingStrategy:
    def test_pressure(self, svar_scalar):
        assert svar_scalar.to_string(_vc.PRESSURE) == "SV_P"

    def test_static_pressure_alias(self, svar_scalar):
        assert svar_scalar.to_string(_vc.STATIC_PRESSURE) == "SV_P"

    def test_velocity_x(self, svar_scalar):
        assert svar_scalar.to_string(_vc.VELOCITY_X) == "SV_U"

    def test_velocity_y(self, svar_scalar):
        assert svar_scalar.to_string(_vc.VELOCITY_Y) == "SV_V"

    def test_velocity_z(self, svar_scalar):
        assert svar_scalar.to_string(_vc.VELOCITY_Z) == "SV_W"

    def test_density(self, svar_scalar):
        assert svar_scalar.to_string(_vc.DENSITY) == "SV_DENSITY"

    def test_temperature(self, svar_scalar):
        assert svar_scalar.to_string(_vc.TEMPERATURE) == "SV_T"

    def test_enthalpy(self, svar_scalar):
        assert svar_scalar.to_string(_vc.SPECIFIC_ENTHALPY) == "SV_H"

    def test_unsupported_descriptor_raises(self, svar_scalar):
        """A descriptor absent from the SVAR scalar map must raise ValueError."""
        assert not svar_scalar.supports(_vc.WALL_Y_PLUS)
        with pytest.raises(ValueError):
            svar_scalar.to_string(_vc.WALL_Y_PLUS)


# ---------------------------------------------------------------------------
# SVAR — vector strategy (empty by design: SVAR API has no named vector types)
# ---------------------------------------------------------------------------


class TestFluentSVarVectorNamingStrategy:
    def test_mapping_is_empty(self):
        """Fluent's SVAR service has no named vector quantities; vectors are
        accessed via component scalars (SV_U/SV_V/SV_W) through
        FluentSVarScalarNamingStrategy.  The vector strategy is therefore
        permanently empty.
        """
        assert FluentSVarVectorNamingStrategy._mapping == {}

    def test_no_descriptors_supported(self, svar_vector):
        assert not svar_vector.supports(_vc.VELOCITY)
        assert not svar_vector.supports(_vc.PRESSURE)

    def test_to_string_raises_for_any_descriptor(self, svar_vector):
        with pytest.raises(ValueError):
            svar_vector.to_string(_vc.VELOCITY)

    def test_to_string_passthrough_still_works(self, svar_vector):
        """Even with an empty mapping, string passthrough must work."""
        assert svar_vector.to_string("SV_U") == "SV_U"

    def test_to_string_none_still_works(self, svar_vector):
        assert svar_vector.to_string(None) is None


# ---------------------------------------------------------------------------
# SVAR — combined (backward-compat) strategy
# ---------------------------------------------------------------------------


class TestFluentSVarNamingStrategy:
    def test_combined_contains_all_scalar_entries(self, svar_combined):
        assert svar_combined.to_string(_vc.PRESSURE) == "SV_P"
        assert svar_combined.to_string(_vc.VELOCITY_X) == "SV_U"
        assert svar_combined.to_string(_vc.TEMPERATURE) == "SV_T"

    def test_combined_mapping_is_superset(self):
        combined_keys = set(FluentSVarNamingStrategy._mapping.keys())
        scalar_keys = set(FluentSVarScalarNamingStrategy._mapping.keys())
        vector_keys = set(FluentSVarVectorNamingStrategy._mapping.keys())
        assert scalar_keys.issubset(combined_keys)
        assert vector_keys.issubset(combined_keys)  # trivially true (empty)


# ---------------------------------------------------------------------------
# to_variable_descriptor round-trips (units repo feature)
# ---------------------------------------------------------------------------


class TestToVariableDescriptorRoundTrip:
    """Verifies the reverse-mapping feature supplied by MappingConversionStrategy."""

    def test_field_scalar_round_trip(self, field_scalar):
        descriptor = _vc.TEMPERATURE
        name = field_scalar.to_string(descriptor)
        assert field_scalar.to_variable_descriptor(name) == descriptor

    def test_field_vector_round_trip(self, field_vector):
        descriptor = _vc.VELOCITY
        name = field_vector.to_string(descriptor)
        assert field_vector.to_variable_descriptor(name) == descriptor

    def test_expr_scalar_round_trip(self, expr_scalar):
        descriptor = _vc.TURBULENT_KINETIC_ENERGY
        name = expr_scalar.to_string(descriptor)
        assert expr_scalar.to_variable_descriptor(name) == descriptor

    def test_expr_vector_round_trip(self, expr_vector):
        descriptor = _vc.fluent.DVELOCITY_DX
        name = expr_vector.to_string(descriptor)
        assert expr_vector.to_variable_descriptor(name) == descriptor

    def test_svar_scalar_round_trip(self, svar_scalar):
        descriptor = _vc.VELOCITY_X
        name = svar_scalar.to_string(descriptor)
        assert svar_scalar.to_variable_descriptor(name) == descriptor

    def test_to_variable_descriptor_unknown_string_returns_none(self, field_scalar):
        """Unknown strings must return None, not raise."""
        assert field_scalar.to_variable_descriptor("no-such-field") is None

    def test_to_variable_descriptor_passthrough_for_descriptor(self, expr_scalar):
        """If a VariableDescriptor is passed, it is returned as-is."""
        descriptor = _vc.PRESSURE
        assert expr_scalar.to_variable_descriptor(descriptor) is descriptor


# ---------------------------------------------------------------------------
# supports() cross-strategy checks
# ---------------------------------------------------------------------------


class TestSupportsAcrossStrategies:
    """Ensures supports() correctly partitions variables between sub-strategies."""

    @pytest.mark.parametrize(
        "descriptor",
        [_vc.VELOCITY, _vc.MESH_VELOCITY, _vc.VORTICITY, _vc.WALL_SHEAR_STRESS],
    )
    def test_field_vectors_supported_only_in_vector_strategy(
        self, descriptor, field_scalar, field_vector
    ):
        assert field_vector.supports(descriptor)
        assert not field_scalar.supports(descriptor)

    @pytest.mark.parametrize(
        "descriptor", [_vc.PRESSURE, _vc.TEMPERATURE, _vc.VELOCITY_X, _vc.WALL_Y_PLUS]
    )
    def test_field_scalars_supported_only_in_scalar_strategy(
        self, descriptor, field_scalar, field_vector
    ):
        assert field_scalar.supports(descriptor)
        assert not field_vector.supports(descriptor)

    @pytest.mark.parametrize(
        "descriptor",
        [
            _vc.VELOCITY,
            _vc.MESH_VELOCITY,
            _vc.VORTICITY,
            _vc.WALL_SHEAR_STRESS,
            _vc.fluent.DVELOCITY_DX,
            _vc.fluent.DVELOCITY_DY,
            _vc.fluent.DVELOCITY_DZ,
        ],
    )
    def test_expr_vectors_supported_only_in_vector_strategy(
        self, descriptor, expr_scalar, expr_vector
    ):
        assert expr_vector.supports(descriptor)
        assert not expr_scalar.supports(descriptor)

    @pytest.mark.parametrize(
        "descriptor",
        [
            _vc.PRESSURE,
            _vc.VELOCITY_X,
            _vc.fluent.DVELOCITY_DX_X,
            _vc.WALL_SHEAR_STRESS_MAGNITUDE,
        ],
    )
    def test_expr_scalars_supported_only_in_scalar_strategy(
        self, descriptor, expr_scalar, expr_vector
    ):
        assert expr_scalar.supports(descriptor)
        assert not expr_vector.supports(descriptor)
