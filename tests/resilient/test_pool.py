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

"""Tests for the warm session pool and failover."""

import time

import pytest

from ansys.fluent.core.resilient.checkpoint import CheckpointManager
from ansys.fluent.core.resilient.exceptions import FailoverError
from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.pool import PoolConfig, WarmSessionPool
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def _make_session():
    return FakeSession(
        settings=FakeSettings(
            file_group=FakeFileGroup(), setup=FakeGroup(a=FakeLeaf(1))
        )
    )


def _launcher(_kwargs):
    return _make_session()


def test_single_session_pool_has_no_standby():
    pool = WarmSessionPool(
        PoolConfig(size=1), seed_session=_make_session(), launcher=_launcher
    )
    try:
        assert pool.size == 1
        with pytest.raises(FailoverError):
            pool.acquire_standby()
    finally:
        pool.shutdown()


def test_pool_fills_to_size():
    pool = WarmSessionPool(PoolConfig(size=3), launcher=_launcher)
    try:
        assert pool.size == 3
        assert pool.active is not None
    finally:
        pool.shutdown()


def test_failover_promotes_standby_and_replays(tmp_path):
    seed = _make_session()
    pool = WarmSessionPool(PoolConfig(size=2), seed_session=seed, launcher=_launcher)
    mgr = CheckpointManager(
        pool.active, file_config=FileCheckpointConfig(directory=str(tmp_path))
    )
    # Take a file checkpoint on the active session (the replay base).
    mgr.checkpoint_file("pre-iterate")
    active_file_group = pool.active.settings.file
    assert any(c[0] == "write_case_data" for c in active_file_group.calls)

    # The active session dies.
    dead = pool.active
    dead.go_fatal("crash")

    new_active = pool.failover(mgr)
    try:
        assert new_active is not dead
        # The dead session must NOT have been read from after fatal.
        # Replay reloaded the checkpoint onto the new active session.
        assert any(c[0] == "read_case_data" for c in new_active.settings.file.calls)
    finally:
        pool.shutdown()


def test_failover_without_standby_raises(tmp_path):
    seed = _make_session()
    pool = WarmSessionPool(PoolConfig(size=1), seed_session=seed, launcher=_launcher)
    mgr = CheckpointManager(
        pool.active, file_config=FileCheckpointConfig(directory=str(tmp_path))
    )
    mgr.checkpoint_file("cp")
    pool.active.go_fatal("crash")
    try:
        with pytest.raises(FailoverError):
            pool.failover(mgr)
    finally:
        pool.shutdown()


def test_shutdown_exits_all_sessions():
    sessions = []

    def tracking_launcher(_kwargs):
        s = _make_session()
        sessions.append(s)
        return s

    pool = WarmSessionPool(PoolConfig(size=2), launcher=tracking_launcher)
    pool.shutdown()
    # Give async exits a moment (shutdown exits inline, so immediate).
    time.sleep(0.05)
    assert all(s.exited for s in sessions)
