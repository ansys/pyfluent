# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Journal, checkpoint store, pool, and configuration."""

from pathlib import Path
import threading
import time

from _resilient_fakes import FakeAdapter, FakeSession
import pytest

from ansys.fluent.core.resilient.engine import (
    CheckpointConfig,
    CheckpointError,
    CommandOp,
    FailoverError,
    Journal,
    PoolConfig,
    RecoveryPolicy,
    ResilientConfig,
    ResilientError,
    SetOp,
    WarmSessionPool,
)
from ansys.fluent.core.resilient.engine.checkpoint import (
    CheckpointStore,
    preflight_read,
    preflight_write,
    sanitize,
)

pytestmark = pytest.mark.resilient


# -- journal --------------------------------------------------------------------


def test_journal_assigns_increasing_sequence_numbers():
    journal = Journal()
    first = journal.record(SetOp("a", 1, 0, True))
    second = journal.record(CommandOp("x", "iterate", {"iter_count": 2}))
    assert (first.seq, second.seq) == (0, 1)
    assert journal.next_seq == 2
    assert [op["kind"] for op in journal.to_script()] == ["set", "command"]


def test_journal_undo_redo_restore_values_in_lifo_order():
    journal = Journal()
    state = {"a": 0}
    journal.record(SetOp("a", 1, 0, True))
    journal.record(SetOp("a", 2, 1, True))
    write = state.__setitem__
    journal.undo(write)
    assert state["a"] == 1
    journal.undo(write)
    assert state["a"] == 0
    journal.redo(write)
    assert state["a"] == 1
    # A new operation discards the undone tail.
    journal.record(SetOp("a", 5, 1, True))
    assert not journal.can_redo()


def test_journal_refuses_to_undo_commands_and_unknown_values():
    journal = Journal()
    journal.record(SetOp("a", 1))
    with pytest.raises(ResilientError, match="not captured"):
        journal.undo(lambda path, value: None)
    journal.record(CommandOp("x", "iterate"))
    with pytest.raises(ResilientError, match="rollback"):
        journal.undo(lambda path, value: None)


def test_journal_reports_overflow_since_a_checkpoint():
    journal = Journal(max_ops=2)
    for value in range(4):
        journal.record(SetOp("a", value))
    assert [op.new_value for op in journal.live_since(2)] == [2, 3]
    with pytest.raises(ResilientError, match="journal_max_ops"):
        journal.live_since(0)


def test_journal_truncate():
    journal = Journal()
    for value in range(3):
        journal.record(SetOp("a", value))
    journal.truncate(1)
    assert [op.new_value for op in journal.operations] == [0]


# -- configuration -----------------------------------------------------------------


def test_config_validation():
    assert ResilientConfig(recovery="strict").recovery is RecoveryPolicy.STRICT
    with pytest.raises(ValueError, match="recovery policy"):
        ResilientConfig(recovery="sometimes")
    with pytest.raises(ValueError):
        PoolConfig(size=0)
    with pytest.raises(ValueError):
        CheckpointConfig(keep_last=0)


# -- checkpoint files --------------------------------------------------------------


def test_sanitize_produces_valid_file_names():
    assert sanitize("auto:solution/iterate") == "auto_solution_iterate"
    assert sanitize("...") == "checkpoint"


def test_preflight_checks(tmp_path):
    preflight_write(tmp_path / "ok.json")
    with pytest.raises(CheckpointError, match="does not exist"):
        preflight_write(tmp_path / "missing" / "x.json")
    with pytest.raises(CheckpointError, match="does not exist"):
        preflight_read(tmp_path / "nothing.json")
    empty = tmp_path / "empty.json"
    empty.write_text("")
    with pytest.raises(CheckpointError, match="empty"):
        preflight_read(empty)


def _store(tmp_path, adapter=None, keep_last=5):
    return CheckpointStore(
        adapter or FakeAdapter(),
        CheckpointConfig(directory=tmp_path, keep_last=keep_last),
        run_id="run",
    )


def test_store_writes_into_a_per_run_directory_and_prunes(tmp_path):
    session = FakeSession()
    store = _store(tmp_path, keep_last=2)
    written = [store.write(session, f"cp{i}").path for i in range(3)]
    assert all(p.startswith(str(tmp_path / "run")) for p in written)
    assert [c.name for c in store.checkpoints] == ["cp1", "cp2"]
    assert not (tmp_path / "run" / "001_cp0.json").exists()
    assert store.find().name == "cp2"
    assert store.find("cp1").path == written[1]
    with pytest.raises(CheckpointError, match="No checkpoint named"):
        store.find("cp0")


def test_store_restore_and_discard_after(tmp_path):
    session = FakeSession()
    store = _store(tmp_path)
    first = store.write(session, "first")
    session.settings.setup.intensity.value = 0.5
    second = store.write(session, "second")
    store.restore(session, first)
    assert session.settings.setup.intensity.value == 0.05
    store.discard_after(first)
    assert store.checkpoints == [first]
    assert not Path(second.path).exists()


def test_store_detects_a_checkpoint_that_was_not_written(tmp_path):
    class SilentAdapter(FakeAdapter):
        def write_checkpoint(self, session, file_path, *, include_data):
            return False

    with pytest.raises(CheckpointError, match="not written correctly"):
        _store(tmp_path, SilentAdapter()).write(FakeSession(), "cp")


def test_store_uses_server_paths_for_remote_servers(tmp_path):
    class RemoteAdapter(FakeAdapter):
        def shares_client_filesystem(self, session):
            return False

        def write_checkpoint(self, session, file_path, *, include_data):
            self.path = file_path
            return False

    adapter = RemoteAdapter()
    store = CheckpointStore(adapter, CheckpointConfig(), run_id="run")
    checkpoint = store.write(FakeSession(), "cp")
    assert checkpoint.path == "resilient_run_001_cp.json"


# -- pool -----------------------------------------------------------------------------


def test_pool_launches_standbys_and_promotes():
    adapter = FakeAdapter(factory=FakeSession)
    active = FakeSession()
    pool = WarmSessionPool(
        active, size=3, launcher=adapter.standby_launcher(active), adapter=adapter
    )
    assert pool.size == 3
    assert len(pool.standbys) == 2
    standby = pool.take_standby()
    previous = pool.promote(standby)
    assert previous is active and pool.active is standby
    _wait_for(lambda: active.exited)
    _wait_for(lambda: len(pool.standbys) == 2)  # refilled in the background
    pool.shutdown(keep=standby)
    assert not standby.exited
    assert all(s.exited for s in adapter.launched if s is not standby)


def test_pool_skips_unhealthy_standbys():
    adapter = FakeAdapter(factory=FakeSession)
    pool = WarmSessionPool(
        FakeSession(), size=2, launcher=adapter.standby_launcher(None), adapter=adapter
    )
    pool.standbys[0].serving = False
    with pytest.raises(FailoverError):
        pool.take_standby()


def test_pool_cleans_up_when_a_standby_cannot_be_launched():
    launched = []

    def launcher():
        if launched:
            raise RuntimeError("no license")
        session = FakeSession()
        launched.append(session)
        return session

    with pytest.raises(ResilientError, match="no license"):
        WarmSessionPool(FakeSession(), size=3, launcher=launcher, adapter=FakeAdapter())
    assert launched[0].exited


def _wait_for(condition, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return
        threading.Event().wait(0.02)
    raise AssertionError("condition not met in time")
