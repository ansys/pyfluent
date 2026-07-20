# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the discovery layer and per-slot accessors.

Uses lightweight fakes that mimic the settings-tree contract
(``.setup.boundary_conditions.get_object_names()``, etc.).
No live Fluent session required.
"""

import pytest

from ansys.fluent.core.expressions import ExpressionBuilder
from ansys.units import VariableCatalog as V

# --------------------------------------------------------------------------- #
# Fakes                                                                       #
# --------------------------------------------------------------------------- #


class _FakeContainer:
    def __init__(self, names):
        self._names = list(names)

    def get_object_names(self):
        return list(self._names)

    def __iter__(self):
        return iter(self._names)


class _FakeSetup:
    def __init__(self, bcs, named_exprs):
        self.boundary_conditions = _FakeContainer(bcs)
        self.named_expressions = _FakeContainer(named_exprs)


class _FakeResults:
    def __init__(self, surfaces):
        self.surfaces = _FakeContainer(surfaces)


class _FakeSettings:
    def __init__(self, bcs=(), named_exprs=(), surfaces=()):
        self.setup = _FakeSetup(bcs, named_exprs)
        self.results = _FakeResults(surfaces)


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #


@pytest.fixture
def offline():
    return ExpressionBuilder()


@pytest.fixture
def online():
    return ExpressionBuilder(
        settings=_FakeSettings(
            bcs=["inlet1", "inlet2", "outlet"],
            named_exprs=["dp", "ke"],
            surfaces=["plane-1", "inlet1"],  # inlet1 duplicated -> dedup
        )
    )


# --------------------------------------------------------------------------- #
# Builder-level discovery                                                     #
# --------------------------------------------------------------------------- #


def test_offline_surface_names_empty(offline):
    assert offline.surface_names() == []


def test_online_surface_names_deduped(online):
    assert online.surface_names() == ["inlet1", "inlet2", "outlet", "plane-1"]


def test_online_named_expressions(online):
    assert online.named_expression_names() == ["dp", "ke"]


def test_variables_listing_static(offline):
    # Doesn't need a live session - driven by the naming strategy mapping.
    vs = offline.variables()
    assert V.ABSOLUTE_PRESSURE in vs
    assert V.TEMPERATURE in vs


# --------------------------------------------------------------------------- #
# Slot accessors -- locations                                                 #
# --------------------------------------------------------------------------- #


def test_location_slot_allowed_values_online(online):
    inv = online.reductions.area_ave
    assert inv.locations.allowed_values() == ["inlet1", "inlet2", "outlet", "plane-1"]


def test_location_slot_is_allowed_online(online):
    inv = online.reductions.area_ave
    assert inv.locations.is_allowed("inlet1") is True
    assert inv.locations.is_allowed("bogus") is False
    assert inv.locations.is_allowed(["inlet1", "outlet"]) is True
    assert inv.locations.is_allowed(["inlet1", "bogus"]) is False


def test_location_slot_permissive_offline(offline):
    inv = offline.reductions.area_ave
    assert inv.locations.allowed_values() == []
    # No settings -> can't refute, so accept.
    assert inv.locations.is_allowed("anything") is True


# --------------------------------------------------------------------------- #
# Slot accessors -- scalar expression (segregated sub-slots)                  #
# --------------------------------------------------------------------------- #


def test_scalar_slot_variables_sub_slot(online):
    inv = online.reductions.area_ave
    vs = inv.expression.variables.allowed_values()
    assert V.ABSOLUTE_PRESSURE in vs
    assert inv.expression.variables.is_allowed(V.ABSOLUTE_PRESSURE) is True
    assert inv.expression.variables.is_allowed("AbsolutePressure") is False


def test_scalar_slot_named_sub_slot(online):
    inv = online.reductions.area_ave
    assert inv.expression.named.allowed_values() == ["dp", "ke"]
    assert inv.expression.named.is_allowed("dp") is True
    assert inv.expression.named.is_allowed("nope") is False


def test_scalar_slot_agglomerated(online):
    inv = online.reductions.area_ave
    all_allowed = inv.expression.allowed_values()
    assert V.ABSOLUTE_PRESSURE in all_allowed
    assert "dp" in all_allowed
    assert inv.expression.is_allowed(V.ABSOLUTE_PRESSURE) is True
    assert inv.expression.is_allowed("dp") is True
    assert inv.expression.is_allowed("nope") is False


def test_scalar_slot_named_permissive_offline(offline):
    inv = offline.reductions.area_ave
    # No settings -> named list empty, but is_allowed must not falsely refute.
    assert inv.expression.named.is_allowed("anything") is True


# --------------------------------------------------------------------------- #
# Invoker introspection                                                       #
# --------------------------------------------------------------------------- #


def test_invoker_exposes_slots_in_dir(online):
    inv = online.reductions.area_ave
    d = dir(inv)
    assert "expression" in d
    assert "locations" in d


def test_invoker_unknown_slot_raises(online):
    inv = online.reductions.area_ave
    with pytest.raises(AttributeError):
        inv.nonexistent
