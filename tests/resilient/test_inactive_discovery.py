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

"""Tests for live-introspection discovery of inactive-target activation.

A thermal boundary-condition value is inactive only because the energy model is
off. The resolver must *discover* -- by toggling candidate model flags and
re-checking ``is_active()`` -- that enabling ``setup.models.energy.enabled``
activates the target, keep that flag, and leave unrelated flags untouched.
"""

import pytest

from ansys.fluent.core.resilient.apply import SafeApplier
from ansys.fluent.core.resilient.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.types import Classification, ErrorCategory, Severity
from tests.resilient._fakes import FakeGroup, FakeLeaf, FakeSession, FakeSettings

pytestmark = pytest.mark.resilient


class EnergyFlag(FakeLeaf):
    """A boolean model flag that, when enabled, activates its dependent targets."""

    def __init__(self, dependents):
        super().__init__(value=False)
        self._dependents = dependents

    def set_state(self, value):
        super().set_state(value)
        for dep in self._dependents:
            dep._active = bool(value)


def _coupled_session():
    """A session where energy.enabled governs a thermal BC leaf's activeness."""
    # Thermal temperature leaf, inactive until energy is enabled; also rejects a
    # set while inactive (as live Fluent does).
    temperature = FakeLeaf(293.15, active=False)

    def reject_if_inactive(value):
        if not temperature._active:
            raise RuntimeError("The object is not active")

    temperature._set_raises = reject_if_inactive

    energy = EnergyFlag(dependents=[temperature])
    viscous = EnergyFlag(dependents=[])  # unrelated flag; must stay off

    settings = FakeSettings(
        setup=FakeGroup(
            models=FakeGroup(
                energy=FakeGroup(enabled=energy),
                viscous=FakeGroup(enabled=viscous),
            ),
            boundary_conditions=FakeGroup(
                cold_inlet=FakeGroup(thermal=FakeGroup(temperature=temperature)),
            ),
        )
    )
    session = FakeSession(settings=settings)
    return session, energy, viscous, temperature


def _inactive_cls():
    return Classification(
        category=ErrorCategory.INACTIVE_TARGET,
        severity=Severity.RECOVERABLE,
        message="Target is inactive in the current model state.",
    )


def test_discovers_energy_flag_for_inactive_thermal():
    session, energy, viscous, temperature = _coupled_session()
    resolver = RecoverableErrorResolver(session)
    path = "setup.boundary_conditions.cold_inlet.thermal.temperature"
    fix = resolver.propose(path, 293.15, _inactive_cls())
    assert fix is not None
    assert fix.kind == "activate_model"
    # It discovered the energy flag specifically.
    assert ("setup.models.energy.enabled", True) in fix.pre_mutations
    # Energy left enabled (the discovered activator); viscous untouched.
    assert energy.get_state() is True
    assert viscous.get_state() is False
    # The target is now active.
    assert temperature.is_active() is True


def test_no_fix_when_no_flag_activates_target():
    # A target that stays inactive no matter which flag is toggled -> no fix,
    # and every probed flag is reverted to off.
    stubborn = FakeLeaf(0.0, active=False)
    energy = EnergyFlag(dependents=[])  # does not affect `stubborn`
    settings = FakeSettings(
        setup=FakeGroup(
            models=FakeGroup(energy=FakeGroup(enabled=energy)),
            x=stubborn,
        )
    )
    session = FakeSession(settings=settings)
    resolver = RecoverableErrorResolver(session)
    fix = resolver.propose("setup.x", 1.0, _inactive_cls())
    assert fix is None
    assert energy.get_state() is False  # reverted


def test_end_to_end_auto_activation_via_applier():
    session, energy, viscous, temperature = _coupled_session()
    applier = SafeApplier(session)
    # The user sets the thermal value while energy is off; it must auto-recover.
    out = applier.set("setup.boundary_conditions.cold_inlet.thermal.temperature", 300.0)
    assert out.ok
    assert "activate_model" in out.fixes_applied
    assert energy.get_state() is True
    assert temperature.get_state() == 300.0
