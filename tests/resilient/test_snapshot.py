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

"""Tests for path resolution and settings snapshot / restore."""

import pytest

from ansys.fluent.core.resilient import _compat, snapshot
from ansys.fluent.core.resilient.exceptions import PathResolutionError
from tests.resilient._fakes import (
    FakeGroup,
    FakeLeaf,
    FakeNamedObject,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def _tree():
    inlet = FakeGroup(velocity=FakeLeaf(0.0))
    bcs = FakeNamedObject(inlet=inlet)
    setup = FakeGroup(
        boundary_conditions=bcs,
        models=FakeGroup(energy=FakeGroup(enabled=FakeLeaf(False))),
    )
    return FakeSettings(setup=setup)


def test_parse_segments_strips_prefix_and_keys():
    segs = _compat.parse_segments('solver.settings.a.b["x"].c')
    assert segs == [("a", None), ("b", "x"), ("c", None)]


def test_resolve_named_object():
    session = type("S", (), {"settings": _tree()})()
    obj = _compat.resolve(session, 'setup.boundary_conditions["inlet"].velocity')
    assert obj.get_state() == 0.0


def test_resolve_missing_raises():
    session = type("S", (), {"settings": _tree()})()
    with pytest.raises(PathResolutionError):
        _compat.resolve(session, "setup.nope.here")


def test_resolve_parent():
    session = type("S", (), {"settings": _tree()})()
    parent, leaf = _compat.resolve_parent(session, "setup.models.energy.enabled")
    assert leaf == "enabled"
    assert parent.enabled.get_state() is False


def test_snapshot_and_restore_roundtrip():
    session = type("S", (), {"settings": _tree()})()
    paths = ["setup.models.energy.enabled"]
    entry = snapshot.capture_settings(session, paths, "cp")
    _compat.resolve(session, paths[0]).set_state(True)
    assert _compat.resolve(session, paths[0]).get_state() is True
    outcomes = snapshot.restore_settings(session, entry)
    assert all(o.ok for o in outcomes)
    assert _compat.resolve(session, paths[0]).get_state() is False


def test_snapshot_root():
    session = type("S", (), {"settings": _tree()})()
    entry = snapshot.capture_settings(session, None, "root")
    assert "<root>" in entry.states


def test_snapshot_bad_path_recorded_not_raised():
    session = type("S", (), {"settings": _tree()})()
    entry = snapshot.capture_settings(session, ["setup.bad.path"], "cp")
    assert "setup.bad.path" in entry.errors
    assert not entry.states


def test_safe_set_state_recurses_on_runtime_error():
    # A group whose bulk set_state fails, but children succeed individually.
    good = FakeLeaf(1)

    class PickyGroup(FakeGroup):
        def set_state(self, state):
            raise RuntimeError("bulk set not supported")

    group = PickyGroup(a=good)
    snapshot.safe_set_state(group, {"a": 42})
    assert good.get_state() == 42
