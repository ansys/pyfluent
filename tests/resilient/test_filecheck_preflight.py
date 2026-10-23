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

"""Tests for file-checkpoint pre-flight validation.

These assert that a bad checkpoint target (illegal name, missing / unwritable
directory, over-long path, missing / empty / unreadable artifact) is rejected
*locally* with a ``CheckpointError`` before any write/read command is issued --
so a malformed target can never wedge a synchronous Fluent file command.
"""

import pytest

from ansys.fluent.core.resilient.exceptions import CheckpointError
from ansys.fluent.core.resilient.filecheck import (
    FileCheckpointConfig,
    FileCheckpointStore,
    preflight_read,
    preflight_write,
)
from ansys.fluent.core.resilient.types import CheckpointKind, UndoEntry
from tests.resilient._fakes import FakeFileGroup, FakeSession, FakeSettings

pytestmark = pytest.mark.resilient


# -- preflight_write --------------------------------------------------------


def test_preflight_write_ok(tmp_path):
    preflight_write(str(tmp_path / "ok.cas.h5"))  # no raise


def test_preflight_write_illegal_name(tmp_path):
    with pytest.raises(CheckpointError, match="illegal"):
        preflight_write(str(tmp_path / "bad:name.cas.h5"))


def test_preflight_write_missing_directory(tmp_path):
    with pytest.raises(CheckpointError, match="does not exist"):
        preflight_write(str(tmp_path / "nope" / "x.cas.h5"))


def test_preflight_write_unwritable_directory(tmp_path, monkeypatch):
    # Simulate a non-writable directory without depending on OS permissions.
    import ansys.fluent.core.resilient.filecheck as fc

    monkeypatch.setattr(fc.os, "access", lambda *a, **k: False)
    with pytest.raises(CheckpointError, match="not writable"):
        preflight_write(str(tmp_path / "x.cas.h5"))


def test_preflight_write_path_too_long(tmp_path):
    long_name = "a" * 300 + ".cas.h5"
    with pytest.raises(CheckpointError, match="too long"):
        preflight_write(str(tmp_path / long_name))


# -- preflight_read ---------------------------------------------------------


def test_preflight_read_ok(tmp_path):
    f = tmp_path / "ok.cas.h5"
    f.write_bytes(b"not-empty")
    preflight_read(str(f))  # no raise


def test_preflight_read_none():
    with pytest.raises(CheckpointError, match="No checkpoint artifact"):
        preflight_read(None)


def test_preflight_read_missing(tmp_path):
    with pytest.raises(CheckpointError, match="no longer exists"):
        preflight_read(str(tmp_path / "gone.cas.h5"))


def test_preflight_read_empty(tmp_path):
    f = tmp_path / "empty.cas.h5"
    f.touch()  # zero bytes
    with pytest.raises(CheckpointError, match="empty"):
        preflight_read(str(f))


# -- store wiring -----------------------------------------------------------


def test_store_write_rejects_bad_directory_before_rpc(tmp_path):
    # A file group that would record a call if the RPC were reached.
    file_group = FakeFileGroup()
    session = FakeSession(settings=FakeSettings(file_group=file_group))
    # Point at a directory that mkdir creates, then make os.access fail.
    store = FileCheckpointStore(FileCheckpointConfig(directory=str(tmp_path)))
    import ansys.fluent.core.resilient.filecheck as fc

    orig_access = fc.os.access
    fc.os.access = lambda *a, **k: False
    try:
        with pytest.raises(CheckpointError, match="not writable"):
            store.write(session, "cp")
    finally:
        fc.os.access = orig_access
    # The RPC must NOT have been issued.
    assert file_group.calls == []


def test_store_restore_rejects_missing_artifact_before_rpc(tmp_path):
    file_group = FakeFileGroup()
    session = FakeSession(settings=FakeSettings(file_group=file_group))
    store = FileCheckpointStore(FileCheckpointConfig(directory=str(tmp_path)))
    entry = UndoEntry(
        kind=CheckpointKind.FILE,
        name="cp",
        case_data_path=str(tmp_path / "never_written.cas.h5"),
        data=True,
    )
    with pytest.raises(CheckpointError, match="no longer exists"):
        store.restore(session, entry)
    assert file_group.calls == []
