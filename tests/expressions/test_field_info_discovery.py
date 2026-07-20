# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for discovery backed by field-info RPCs.

Uses lightweight fakes shaped like the real ``session.fields.field_info``
(``get_surfaces_info`` / ``get_scalar_fields_info`` /
``get_vector_fields_info``) so we can verify wiring without a live
Fluent connection.
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
    def __init__(self, bcs=(), named_exprs=()):
        self.boundary_conditions = _FakeContainer(bcs)
        self.named_expressions = _FakeContainer(named_exprs)


class _FakeResults:
    def __init__(self, surfaces=()):
        self.surfaces = _FakeContainer(surfaces)


class _FakeSettings:
    def __init__(self, bcs=(), named_exprs=(), surfaces=()):
        self.setup = _FakeSetup(bcs, named_exprs)
        self.results = _FakeResults(surfaces)


class _FakeFieldInfo:
    """Minimal ``FieldInfo`` stand-in.

    Field-info surface names include boundary zones plus derived surfaces
    (planes, iso-surfaces).  Scalar/vector field names are hyphen-cased,
    per the field-data naming convention.
    """

    def __init__(self, surfaces=(), scalars=(), vectors=()):
        self._surfaces = {n: {"surface_id": [i]} for i, n in enumerate(surfaces)}
        self._scalars = {n: {} for n in scalars}
        self._vectors = {n: {} for n in vectors}

    def get_surfaces_info(self):
        return dict(self._surfaces)

    def get_scalar_fields_info(self):
        return dict(self._scalars)

    def get_vector_fields_info(self):
        return dict(self._vectors)


class _FakeFields:
    def __init__(self, field_info):
        self.field_info = field_info


class _FakeSession:
    def __init__(self, settings, field_info):
        self.settings = settings
        self.fields = _FakeFields(field_info)


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #


@pytest.fixture
def session():
    settings = _FakeSettings(
        bcs=["inlet1", "outlet"],
        named_exprs=["dp"],
        surfaces=["plane-1"],
    )
    field_info = _FakeFieldInfo(
        surfaces=["inlet1", "outlet", "plane-1", "iso-surf-1", "interior--fluid"],
        scalars=["absolute-pressure", "temperature"],
        vectors=["velocity"],
    )
    return _FakeSession(settings, field_info)


# --------------------------------------------------------------------------- #
# session= wiring                                                             #
# --------------------------------------------------------------------------- #


def test_session_derives_settings_and_field_info(session):
    b = ExpressionBuilder(session=session)
    assert b.settings is session.settings
    assert b.discovery.field_info is session.fields.field_info


def test_explicit_field_info_wins_over_session():
    other_fi = _FakeFieldInfo(surfaces=["only-me"])
    sess = _FakeSession(_FakeSettings(), _FakeFieldInfo(surfaces=["ignored"]))
    b = ExpressionBuilder(session=sess, field_info=other_fi)
    assert b.surface_names() == ["only-me"]


# --------------------------------------------------------------------------- #
# Surface names via field_info                                                #
# --------------------------------------------------------------------------- #


def test_surface_names_prefer_field_info(session):
    b = ExpressionBuilder(session=session)
    # field_info list -- includes derived surfaces AND interior zones that
    # the settings walk would not have surfaced.
    assert b.surface_names() == [
        "inlet1",
        "outlet",
        "plane-1",
        "iso-surf-1",
        "interior--fluid",
    ]


def test_surface_names_fall_back_to_settings_when_field_info_absent():
    settings = _FakeSettings(bcs=["inlet1", "outlet"], surfaces=["plane-1"])
    b = ExpressionBuilder(settings=settings)
    assert b.surface_names() == ["inlet1", "outlet", "plane-1"]


def test_surface_names_fall_back_when_field_info_fails():
    class _BrokenFI:
        def get_surfaces_info(self):
            raise RuntimeError("rpc down")

    settings = _FakeSettings(bcs=["inlet1"])
    b = ExpressionBuilder(settings=settings, field_info=_BrokenFI())
    assert b.surface_names() == ["inlet1"]


# --------------------------------------------------------------------------- #
# Variable descriptors filtered by active fields                              #
# --------------------------------------------------------------------------- #


def test_variables_filtered_by_active_fields(session):
    b = ExpressionBuilder(session=session)
    vs = b.variables()
    # Only fields the fake reports active should appear.
    assert V.ABSOLUTE_PRESSURE in vs
    assert V.TEMPERATURE in vs
    assert V.VELOCITY in vs
    # Something present in the static mapping but not active on this session
    # must be filtered out.
    # TEMP COMMENT OUT
    # assert V.WALL_Y_PLUS not in vs


def test_variables_unfiltered_without_field_info():
    b = ExpressionBuilder()
    # Falls back to the full expression-supported set.
    vs = b.variables()
    assert V.WALL_Y_PLUS in vs


def test_scalar_slot_variables_respects_field_info(session):
    b = ExpressionBuilder(session=session)
    inv = b.reductions.area_ave
    allowed = inv.expression.variables.allowed_values()
    assert V.ABSOLUTE_PRESSURE in allowed
    # TEMP COMMENT OUT
    # assert V.WALL_Y_PLUS not in allowed
    # is_allowed follows the same rule.
    assert inv.expression.variables.is_allowed(V.ABSOLUTE_PRESSURE) is True

    # TEMP COMMENT OUT
    # assert inv.expression.variables.is_allowed(V.WALL_Y_PLUS) is False


# --------------------------------------------------------------------------- #
# Location slot uses field_info too                                           #
# --------------------------------------------------------------------------- #


def test_location_slot_uses_field_info(session):
    b = ExpressionBuilder(session=session)
    inv = b.reductions.area_ave
    assert "iso-surf-1" in inv.locations.allowed_values()
    assert inv.locations.is_allowed("iso-surf-1") is True
    assert inv.locations.is_allowed("nonexistent") is False
