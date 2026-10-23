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

"""Tests for the SafeApplier and recoverable-error resolver."""

import pytest

from ansys.fluent.core.resilient.apply import SafeApplier
from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError
from tests.resilient._fakes import FakeGroup, FakeLeaf, FakeSession, FakeSettings

pytestmark = pytest.mark.resilient


def _session(**children):
    return FakeSession(settings=FakeSettings(**children))


def test_set_success_captures_old_value():
    leaf = FakeLeaf(1.0)
    session = _session(setup=FakeGroup(a=leaf))
    outcome = SafeApplier(session).set("setup.a", 2.0)
    assert outcome.ok
    assert outcome.old_value == 1.0
    assert leaf.get_state() == 2.0


def test_set_inactive_target_refused_before_set():
    leaf = FakeLeaf(1.0, active=False)
    session = _session(setup=FakeGroup(a=leaf))
    with pytest.raises(UnrecoverableStepError):
        SafeApplier(session).set("setup.a", 2.0)
    # Must not have written.
    assert leaf.get_state() == 1.0


def test_out_of_range_auto_clamped():
    def reject(value):
        if value > 1.0:
            raise RuntimeError("value is above maximum 1.0")

    leaf = FakeLeaf(0.0, minimum=0.0, maximum=1.0, set_raises=reject)
    session = _session(setup=FakeGroup(ti=leaf))
    outcome = SafeApplier(session).set("setup.ti", 5.0)
    assert outcome.ok
    assert "clamp" in outcome.fixes_applied
    assert leaf.get_state() == 1.0


def test_wrong_value_snapped_to_nearest_allowed():
    def reject(value):
        if value not in ("laminar", "k-epsilon"):
            raise RuntimeError(f"{value!r} is not an allowed value")

    leaf = FakeLeaf("laminar", allowed=["laminar", "k-epsilon"], set_raises=reject)
    session = _session(setup=FakeGroup(model=leaf))
    outcome = SafeApplier(session).set("setup.model", "k-epsilonn")
    assert outcome.ok
    assert "nearest_allowed" in outcome.fixes_applied
    assert leaf.get_state() == "k-epsilon"


def test_unresolvable_recoverable_raises_after_attempts():
    def always_reject(value):
        raise RuntimeError("value is above maximum 1.0")

    # No min/max exposed -> resolver cannot clamp -> gives up.
    leaf = FakeLeaf(0.0, set_raises=always_reject)
    session = _session(setup=FakeGroup(x=leaf))
    with pytest.raises(UnrecoverableStepError):
        SafeApplier(session).set("setup.x", 5.0)


def test_catastrophic_set_propagates():
    def die(value):
        session_holder["s"].go_fatal("boom")
        raise RuntimeError("fatal: solver crashed")

    session_holder = {}
    leaf = FakeLeaf(0.0, set_raises=die)
    session = _session(setup=FakeGroup(x=leaf))
    session_holder["s"] = session
    with pytest.raises(RuntimeError):
        SafeApplier(session).set("setup.x", 1.0)
