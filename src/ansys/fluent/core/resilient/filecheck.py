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

"""File-tier checkpoints (case / data files on disk).

Settings snapshots cannot undo irreversible commands (``iterate``,
``read_case``, ...). For those, the runtime writes a case/data file via
``settings.file.write_case_data`` (or ``write_case``) and reloads it via
``read_case_data`` (or ``read_case``). A ring buffer (``keep_last``) prunes old
artifacts to bound disk usage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import time

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.exceptions import CheckpointError
from ansys.fluent.core.resilient.types import CheckpointKind, UndoEntry

#: Characters that are illegal in file names on common platforms (notably the
#: colon and path separators on Windows) are replaced with an underscore.
_ILLEGAL_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _sanitize(name: str) -> str:
    """Make a checkpoint label safe to embed in an on-disk file name.

    The human-readable checkpoint ``name`` can contain a settings path (with
    dots) or a ``redo:`` / ``auto:`` prefix (with colons); neither is valid in a
    Windows file name. This replaces every illegal character with ``_`` and
    trims trailing dots/spaces, while leaving the stored entry ``name`` intact.
    """
    cleaned = _ILLEGAL_FILENAME_CHARS.sub("_", name).strip(" .")
    return cleaned or "checkpoint"


#: A conservative path-length ceiling. Windows' classic ``MAX_PATH`` is 260; we
#: leave headroom for the ``.dat.h5`` companion Fluent writes alongside a case.
_MAX_PATH_LEN = 240


def preflight_write(file_path: str) -> None:
    """Validate a checkpoint target *before* the write RPC is issued.

    A case/data write is a synchronous command: if the server-side HDF5 write
    fails in a way that never returns a response (illegal name, unwritable or
    missing directory, over-long path), the client can block indefinitely.
    Checking the target locally first turns that latent hang into an immediate,
    actionable :class:`CheckpointError`.

    Raises
    ------
    CheckpointError
        If the file name still contains illegal characters, the parent directory
        does not exist or is not writable, or the path is implausibly long.
    """
    path = Path(file_path)
    name = path.name
    if _ILLEGAL_FILENAME_CHARS.search(name):
        raise CheckpointError(
            f"Checkpoint file name {name!r} contains characters that are "
            "illegal on this platform; refusing to issue the write to avoid a "
            "stuck command."
        )
    parent = path.parent
    if not parent.exists():
        raise CheckpointError(
            f"Checkpoint directory {str(parent)!r} does not exist; refusing to "
            "issue the write."
        )
    if not parent.is_dir():
        raise CheckpointError(
            f"Checkpoint path parent {str(parent)!r} is not a directory."
        )
    if not os.access(parent, os.W_OK):
        raise CheckpointError(
            f"Checkpoint directory {str(parent)!r} is not writable; refusing to "
            "issue the write."
        )
    if len(str(path.resolve())) > _MAX_PATH_LEN:
        raise CheckpointError(
            f"Checkpoint path is too long ({len(str(path))} chars); shorten the "
            "checkpoint directory to avoid a filesystem error."
        )


def preflight_read(file_path: str | None) -> None:
    """Validate a checkpoint artifact *before* the read RPC is issued.

    Reloading a missing, inaccessible, or empty artifact is a common cause of a
    read command that never returns. Verifying the file locally first fails fast
    with a clear :class:`CheckpointError` instead.

    Raises
    ------
    CheckpointError
        If the artifact path is empty, does not exist, is not readable, or is
        an empty (zero-byte) file.
    """
    if not file_path:
        raise CheckpointError("No checkpoint artifact path to restore from.")
    path = Path(file_path)
    if not path.exists():
        raise CheckpointError(
            f"Checkpoint artifact {str(path)!r} no longer exists; cannot "
            "restore (it may have been pruned or moved)."
        )
    if not path.is_file():
        raise CheckpointError(f"Checkpoint artifact {str(path)!r} is not a file.")
    if not os.access(path, os.R_OK):
        raise CheckpointError(f"Checkpoint artifact {str(path)!r} is not readable.")
    try:
        if path.stat().st_size == 0:
            raise CheckpointError(
                f"Checkpoint artifact {str(path)!r} is empty; refusing to issue "
                "the read."
            )
    except OSError as err:
        raise CheckpointError(
            f"Cannot stat checkpoint artifact {str(path)!r}: {err}"
        ) from err


@dataclass
class FileCheckpointConfig:
    """Configuration for the file-checkpoint tier."""

    #: Directory where ``.cas.h5`` / ``.dat.h5`` artifacts are written.
    directory: str | Path = "resilient_checkpoints"
    #: Ring-buffer depth; older artifacts beyond this count are pruned.
    keep_last: int = 5
    #: Write case+data (``True``) or case only (``False``).
    data: bool = True
    #: Template for artifact base names; ``{name}`` and ``{ts}`` are filled.
    name_template: str = "resilient_{name}_{ts}"

    def resolved_directory(self) -> Path:
        """Return the checkpoint directory as a ``Path`` (not yet created)."""
        return Path(self.directory)


class FileCheckpointStore:
    """Write / restore / prune case-data checkpoint artifacts."""

    def __init__(self, config: FileCheckpointConfig | None = None):
        self.config = config or FileCheckpointConfig()
        #: Ordered artifact paths this store has written (for pruning).
        self._written: list[str] = []

    def _settings_file(self, session):
        settings = _compat.settings_root(session)
        file_group = getattr(settings, "file", None)
        if file_group is None:
            raise CheckpointError(
                "Session settings expose no 'file' group; cannot write a file "
                "checkpoint."
            )
        return file_group

    def write(self, session, name: str) -> UndoEntry:
        """Write a case/data checkpoint and return a FILE :class:`UndoEntry`."""
        file_group = self._settings_file(session)
        directory = self.config.resolved_directory()
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as err:  # noqa: BLE001
            raise CheckpointError(
                f"Could not create checkpoint directory {directory!r}: {err}"
            ) from err
        ts = time.strftime("%Y%m%d_%H%M%S") + f"_{int(time.time() * 1000) % 1000:03d}"
        base = self.config.name_template.format(name=_sanitize(name), ts=ts)
        suffix = ".cas.h5"
        file_path = str(directory / f"{base}{suffix}")
        # Fail fast locally so a bad target cannot wedge the write command.
        preflight_write(file_path)
        try:
            if self.config.data:
                file_group.write_case_data(file_name=file_path)
            else:
                file_group.write_case(file_name=file_path)
        except Exception as err:  # noqa: BLE001
            raise CheckpointError(
                f"Failed to write file checkpoint {name!r}: {err}"
            ) from err
        self._written.append(file_path)
        self._prune()
        return UndoEntry(
            kind=CheckpointKind.FILE,
            name=name,
            case_data_path=file_path,
            data=self.config.data,
        )

    def restore(self, session, entry: UndoEntry) -> None:
        """Reload the case/data artifact referenced by ``entry``."""
        if entry.kind is not CheckpointKind.FILE or not entry.case_data_path:
            raise CheckpointError("Entry is not a file checkpoint.")
        file_group = self._settings_file(session)
        # Fail fast locally so a missing / unreadable artifact cannot wedge the
        # read command.
        preflight_read(entry.case_data_path)
        if entry.data:
            companion = Path(entry.case_data_path[: -len(".cas.h5")] + ".dat.h5")
            if entry.case_data_path.endswith(".cas.h5") and not companion.exists():
                raise CheckpointError(
                    f"Checkpoint data file {str(companion)!r} is missing; cannot "
                    "restore case+data."
                )
        try:
            if entry.data:
                file_group.read_case_data(file_name=entry.case_data_path)
            else:
                file_group.read_case(file_name=entry.case_data_path)
        except Exception as err:  # noqa: BLE001
            raise CheckpointError(
                f"Failed to restore file checkpoint {entry.name!r} from "
                f"{entry.case_data_path!r}: {err}"
            ) from err

    def artifact_exists(self, entry: UndoEntry) -> bool:
        """Whether the on-disk artifact for ``entry`` still exists."""
        path = entry.case_data_path
        return bool(path and Path(path).exists())

    def _prune(self) -> None:
        keep = max(1, self.config.keep_last)
        while len(self._written) > keep:
            stale = self._written.pop(0)
            self._remove_artifact(stale)

    @staticmethod
    def _remove_artifact(file_path: str) -> None:
        # Fluent may emit companion files (e.g. a separate .dat.h5); remove the
        # declared path and a sibling .dat.h5 best-effort.
        candidates = [Path(file_path)]
        if file_path.endswith(".cas.h5"):
            candidates.append(Path(file_path[: -len(".cas.h5")] + ".dat.h5"))
        for candidate in candidates:
            try:
                if candidate.exists():
                    candidate.unlink()
            except Exception:  # noqa: BLE001  # nosec B112
                continue
