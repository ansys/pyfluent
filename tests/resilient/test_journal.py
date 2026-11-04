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

"""Tests for the operation journal and the get_state undo/redo recovery cycle."""

import pytest

from ansys.fluent.core.resilient.attach import enable_resilient_mode
from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.journal import CommandOp, Journal, SetOp
from ansys.fluent.core.resilient.solver import ResilientConfig
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


# -- Journal unit tests -----------------------------------------------------


def test_journal_record_and_order():
    restored = []
    j = Journal(restore=lambda p, v: restored.append((p, v)))
    j.record(SetOp("a", old_value=1, new_value=2))
    j.record(SetOp("b", old_value=3, new_value=4))
    assert [op.path for op in j.live_operations] == ["a", "b"]
    assert j.can_undo() and not j.can_redo()


def test_journal_undo_restores_old_value():
    restored = []
    j = Journal(restore=lambda p, v: restored.append((p, v)))
    j.record(SetOp("a", old_value=1, new_value=2))
    op = j.undo()
    assert op.path == "a"
    assert restored == [("a", 1)]  # restored the OLD value
    assert j.can_redo() and not j.can_undo()


def test_journal_redo_reapplies_new_value():
    restored = []
    j = Journal(restore=lambda p, v: restored.append((p, v)))
    j.record(SetOp("a", old_value=1, new_value=2))
    j.undo()
    restored.clear()
    op = j.redo()
    assert op.path == "a"
    assert restored == [("a", 2)]  # re-applied the NEW value


def test_journal_record_truncates_redo_tail():
    j = Journal(restore=lambda p, v: None)
    j.record(SetOp("a", 1, 2))
    j.record(SetOp("b", 3, 4))
    j.undo()  # back over "b"
    j.record(SetOp("c", 5, 6))  # new op invalidates the undone "b"
    assert [op.path for op in j.live_operations] == ["a", "c"]
    assert not j.can_redo()


def test_journal_listeners_notified():
    events = []
    j = Journal(restore=lambda p, v: None)
    j.on_event(lambda name, op: events.append((name, op.path)))
    j.record(SetOp("a", 1, 2))
    j.undo()
    j.redo()
    assert events == [("record", "a"), ("undo", "a"), ("redo", "a")]


def test_sequential_sets_to_same_path_undo_in_lifo_order():
    """Reviewer Point 1: undoing a value does NOT override a later change.

    Models the viscous-model scenario: the same path is set twice in sequence.
    Each op captures the live value at set-time as its own ``old_value`` (read
    via get_state immediately before the write), so sequential undo unwinds in
    exact LIFO order and never restores a stale default over a later change.
    """
    live = {"model": "k-omega"}  # the live value on the (fake) tree

    def restore(path, value):
        live[path] = value

    j = Journal(restore=restore)
    # Op1: k-omega -> k-epsilon (old captured live = k-omega)
    j.record(SetOp("model", old_value="k-omega", new_value="k-epsilon"))
    live["model"] = "k-epsilon"
    # Op2: k-epsilon -> laminar (old captured live = k-epsilon, AFTER Op1)
    j.record(SetOp("model", old_value="k-epsilon", new_value="laminar"))
    live["model"] = "laminar"

    # Undo Op2 -> restores the value BEFORE Op2, i.e. k-epsilon (NOT the default).
    j.undo()
    assert live["model"] == "k-epsilon"
    # Undo Op1 -> restores the value BEFORE Op1, i.e. the original k-omega.
    j.undo()
    assert live["model"] == "k-omega"


def test_command_op_recorded_in_replay_script():
    j = Journal(restore=lambda p, v: None)
    j.record(CommandOp("solution.run_calculation.iterate", {"iter_count": 10}))
    script = j.replay_script()
    assert script[0]["kind"] == "command"
    assert script[0]["args"] == {"iter_count": 10}


# -- End-to-end recovery cycle (get_state -> set -> undo -> recover -> redo) --


def _session_with_clamp():
    def reject_high(value):
        if isinstance(value, (int, float)) and value > 1.0:
            raise RuntimeError("Value is not in range")

    leaf = FakeLeaf(0.05, minimum=0.0, maximum=1.0, set_raises=reject_high)
    settings = FakeSettings(file_group=FakeFileGroup(), setup=FakeGroup(ti=leaf))
    return FakeSession(settings=settings), leaf


def _config(tmp_path):
    return ResilientConfig(
        file_checkpoint=FileCheckpointConfig(directory=str(tmp_path))
    )


def test_set_cycle_emits_undo_then_redo_and_records(tmp_path):
    session, leaf = _session_with_clamp()
    enable_resilient_mode(session, _config(tmp_path))
    events = []
    session._resilient.on_journal_event(lambda name, op: events.append(name))

    # Set an out-of-range value: the cycle is set -> fail -> undo (restore old)
    # -> recover (clamp) -> redo (apply fixed) -> record.
    session._settings_service.set_var("setup.ti", 5.0)

    assert "undo" in events and "redo" in events
    # The journal recorded the successful (clamped) operation.
    ops = session._resilient.journal.live_operations
    assert ops and ops[-1].new_value == 1.0
    assert ops[-1].old_value == 0.05  # the get_state undo value
    assert leaf.get_state() == 1.0


def test_successful_set_records_without_undo_redo(tmp_path):
    session, _ = _session_with_clamp()
    enable_resilient_mode(session, _config(tmp_path))
    events = []
    session._resilient.on_journal_event(lambda name, op: events.append(name))
    # A valid value needs no recovery: only a silent record, no undo/redo.
    session._settings_service.set_var("setup.ti", 0.5)
    assert events == ["record"]
    assert session._resilient.journal.live_operations[-1].new_value == 0.5
