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

"""Tests for two-tier checkpoints and the unified undo / redo stack."""

import os

import pytest

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.checkpoint import CheckpointManager, is_irreversible
from ansys.fluent.core.resilient.exceptions import CheckpointError
from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.types import CheckpointKind
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def _session():
    settings = FakeSettings(setup=FakeGroup(a=FakeLeaf(1), b=FakeLeaf(2)))
    return FakeSession(settings=settings)


def test_is_irreversible():
    assert is_irreversible("solution.run_calculation.iterate")
    assert is_irreversible("file.read_case_data")
    assert not is_irreversible("setup.models.energy.enabled")


def test_settings_undo_redo_roundtrip():
    session = _session()
    mgr = CheckpointManager(session)
    mgr.checkpoint_settings("cp1", ["setup.a"])
    _compat.resolve(session, "setup.a").set_state(99)
    assert _compat.resolve(session, "setup.a").get_state() == 99
    mgr.undo()
    assert _compat.resolve(session, "setup.a").get_state() == 1
    mgr.redo()
    assert _compat.resolve(session, "setup.a").get_state() == 99


def test_new_checkpoint_clears_redo():
    session = _session()
    mgr = CheckpointManager(session)
    mgr.checkpoint_settings("cp1", ["setup.a"])
    mgr.undo()
    assert mgr.redo_stack
    mgr.checkpoint_settings("cp2", ["setup.a"])
    assert not mgr.redo_stack


def test_undo_empty_raises():
    mgr = CheckpointManager(_session())
    with pytest.raises(CheckpointError):
        mgr.undo()


def test_file_checkpoint_writes_and_restores(tmp_path):
    file_group = FakeFileGroup()
    settings = FakeSettings(file_group=file_group, setup=FakeGroup(a=FakeLeaf(1)))
    session = FakeSession(settings=settings)
    cfg = FileCheckpointConfig(directory=str(tmp_path))
    mgr = CheckpointManager(session, file_config=cfg)
    entry = mgr.checkpoint_file("pre-iterate", reason="pre-irreversible")
    assert entry.kind is CheckpointKind.FILE
    assert any(c[0] == "write_case_data" for c in file_group.calls)
    mgr.undo()
    # Undo writes a redo artifact, then reloads the popped one.
    assert any(c[0] == "read_case_data" for c in file_group.calls)


def test_newest_file_checkpoint(tmp_path):
    file_group = FakeFileGroup()
    settings = FakeSettings(file_group=file_group, setup=FakeGroup(a=FakeLeaf(1)))
    session = FakeSession(settings=settings)
    mgr = CheckpointManager(
        session, file_config=FileCheckpointConfig(directory=str(tmp_path))
    )
    mgr.checkpoint_settings("s1", ["setup.a"])
    fentry = mgr.checkpoint_file("f1")
    mgr.checkpoint_settings("s2", ["setup.a"])
    assert mgr.newest_file_checkpoint() is fentry


def test_rewind_to(tmp_path):
    session = _session()
    mgr = CheckpointManager(session)
    mgr.checkpoint_settings("cp1", ["setup.a"])
    _compat.resolve(session, "setup.a").set_state(10)
    mgr.checkpoint_settings("cp2", ["setup.a"])
    _compat.resolve(session, "setup.a").set_state(20)
    undone = mgr.rewind_to("cp1")
    assert [e.name for e in undone] == ["cp2", "cp1"]
    assert _compat.resolve(session, "setup.a").get_state() == 1


def test_file_prune_ring_buffer(tmp_path):
    # FakeFileGroup writes real files, so prune can unlink them.
    settings = FakeSettings(file_group=FakeFileGroup())
    session = FakeSession(settings=settings)
    cfg = FileCheckpointConfig(directory=str(tmp_path), keep_last=2)
    mgr = CheckpointManager(session, file_config=cfg)
    for i in range(4):
        mgr.checkpoint_file(f"cp{i}")
    cas_files = list(tmp_path.glob("*.cas.h5"))
    assert len(cas_files) <= 2


def test_checkpoint_name_with_illegal_chars_is_sanitized(tmp_path):
    # Regression (live v271): a redo/auto checkpoint name carries a settings
    # path and ``:`` prefixes which are illegal in a Windows file name and made
    # the HDF5 write fail. The on-disk file name must be sanitized while the
    # stored entry name stays intact.
    file_group = FakeFileGroup()
    settings = FakeSettings(file_group=file_group)
    session = FakeSession(settings=settings)
    mgr = CheckpointManager(
        session, file_config=FileCheckpointConfig(directory=str(tmp_path))
    )
    name = "redo:auto:solution.run_calculation.iterate"
    entry = mgr.checkpoint_file(name)
    assert entry.name == name  # label preserved
    written = file_group.calls[-1][1]
    filename = os.path.basename(written)
    assert ":" not in filename  # the file name is safe (drive letter aside)
    assert "iterate" in filename
