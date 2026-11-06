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

"""Checkpoint files: naming, retention and pre-flight checks.

The adapter writes and reads the product's checkpoint files (for example a case
and data file). This module decides *where* they go, keeps the newest
``keep_last`` of them, and -- when the server shares the client's file system --
validates paths before and after each write so that a bad target fails fast
instead of leaving a synchronous server command waiting.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import re
import threading
from typing import Any

from .adapter import ResilientAdapter
from .config import CheckpointConfig
from .exceptions import CheckpointError
from .types import Checkpoint

logger = logging.getLogger("ansys.resilient")

#: Characters that are not valid in file names on common platforms.
_ILLEGAL_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

#: Conservative path-length limit (Windows ``MAX_PATH`` is 260 characters).
_MAX_PATH_LEN = 240


def sanitize(name: str) -> str:
    """Make a checkpoint name safe to use in a file name."""
    cleaned = _ILLEGAL_FILENAME_CHARS.sub("_", name).strip(" .")
    return cleaned[:60] or "checkpoint"


def preflight_write(file_path: str | os.PathLike) -> None:
    """Check that a checkpoint can be written to ``file_path``.

    Raises
    ------
    CheckpointError
        If the file name is invalid, the directory is missing or not writable,
        or the path is too long.
    """
    path = Path(file_path)
    if _ILLEGAL_FILENAME_CHARS.search(path.name):
        raise CheckpointError(f"Checkpoint file name {path.name!r} is not valid.")
    parent = path.parent
    if not parent.is_dir():
        raise CheckpointError(f"Checkpoint directory {str(parent)!r} does not exist.")
    if not os.access(parent, os.W_OK):
        raise CheckpointError(f"Checkpoint directory {str(parent)!r} is not writable.")
    if len(str(path.resolve())) > _MAX_PATH_LEN:
        raise CheckpointError(
            f"Checkpoint path {str(path)!r} is longer than {_MAX_PATH_LEN} "
            "characters; use a shorter checkpoint directory."
        )


def preflight_read(file_path: str | os.PathLike) -> None:
    """Check that the checkpoint file at ``file_path`` can be read.

    Raises
    ------
    CheckpointError
        If the file is missing, unreadable, or empty.
    """
    path = Path(file_path)
    if not path.is_file():
        raise CheckpointError(f"Checkpoint file {str(path)!r} does not exist.")
    if not os.access(path, os.R_OK):
        raise CheckpointError(f"Checkpoint file {str(path)!r} is not readable.")
    if path.stat().st_size == 0:
        raise CheckpointError(f"Checkpoint file {str(path)!r} is empty.")


class CheckpointStore:
    """Write, restore and prune the checkpoints of one resilient session."""

    def __init__(
        self, adapter: ResilientAdapter, config: CheckpointConfig, *, run_id: str
    ):
        self._adapter = adapter
        self._config = config
        self._run_id = run_id
        self._checkpoints: list[Checkpoint] = []
        self._counter = 0
        self._lock = threading.RLock()

    # -- queries ---------------------------------------------------------------

    @property
    def checkpoints(self) -> list[Checkpoint]:
        """Return the retained checkpoints (oldest first)."""
        with self._lock:
            return list(self._checkpoints)

    def newest(self) -> Checkpoint | None:
        """Return the newest retained checkpoint, if any."""
        with self._lock:
            return self._checkpoints[-1] if self._checkpoints else None

    def find(self, name: str | None = None) -> Checkpoint:
        """Return the newest checkpoint, or the newest one called ``name``.

        Raises
        ------
        CheckpointError
            If no matching checkpoint is retained.
        """
        with self._lock:
            for checkpoint in reversed(self._checkpoints):
                if name is None or checkpoint.name == name:
                    return checkpoint
        if name is None:
            raise CheckpointError("No checkpoint has been written yet.")
        raise CheckpointError(
            f"No checkpoint named {name!r}; retained checkpoints: "
            f"{[c.name for c in self.checkpoints]}."
        )

    # -- writing and restoring ---------------------------------------------------

    def _target(self, session: Any, name: str) -> tuple[str, bool]:
        """Return the checkpoint file path and whether the client can reach it."""
        self._counter += 1
        file_name = (
            f"{self._counter:03d}_{sanitize(name)}{self._adapter.checkpoint_suffix}"
        )
        if self._adapter.shares_client_filesystem(session):
            base = self._config.directory
            directory = (
                Path(base) if base is not None else Path.cwd() / "resilient_checkpoints"
            )
            directory = (directory / self._run_id).resolve()
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                raise CheckpointError(
                    f"Cannot create checkpoint directory {str(directory)!r}: {err}"
                ) from err
            return str(directory / file_name), True
        # The server has its own file system: write next to the server's working
        # directory (or into the configured server-side directory).
        file_name = f"resilient_{self._run_id}_{file_name}"
        if self._config.directory is not None:
            return f"{str(self._config.directory).rstrip('/')}/{file_name}", False
        return file_name, False

    def write(
        self,
        session: Any,
        name: str,
        *,
        reason: str | None = None,
        journal_seq: int = 0,
    ) -> Checkpoint:
        """Write a checkpoint of ``session``.

        Raises
        ------
        CheckpointError
            If the checkpoint cannot be written or verified.
        """
        with self._lock:
            file_path, local = self._target(session, name)
            if local:
                preflight_write(file_path)
            try:
                included = self._adapter.write_checkpoint(
                    session, file_path, include_data=self._config.include_data
                )
            except CheckpointError:
                raise
            except Exception as err:  # noqa: BLE001
                raise CheckpointError(
                    f"Writing checkpoint {name!r} to {file_path!r} failed: {err}"
                ) from err
            include_data = bool(included)
            if local:
                for artifact in self._adapter.checkpoint_artifacts(
                    file_path, include_data=include_data
                ):
                    try:
                        preflight_read(artifact)
                    except CheckpointError as err:
                        raise CheckpointError(
                            f"Checkpoint {name!r} was not written correctly: {err}"
                        ) from err
            checkpoint = Checkpoint(
                name=name,
                path=file_path,
                include_data=include_data,
                reason=reason,
                journal_seq=journal_seq,
            )
            self._checkpoints.append(checkpoint)
            self._prune(local)
            return checkpoint

    def restore(self, session: Any, checkpoint: Checkpoint) -> None:
        """Restore ``session`` from ``checkpoint``.

        Raises
        ------
        CheckpointError
            If the checkpoint files are missing or the product fails to read them.
        """
        if self._adapter.shares_client_filesystem(session) and os.path.isabs(
            checkpoint.path
        ):
            for artifact in self._adapter.checkpoint_artifacts(
                checkpoint.path, include_data=checkpoint.include_data
            ):
                preflight_read(artifact)
        try:
            self._adapter.read_checkpoint(
                session, checkpoint.path, include_data=checkpoint.include_data
            )
        except CheckpointError:
            raise
        except Exception as err:  # noqa: BLE001
            raise CheckpointError(
                f"Restoring checkpoint {checkpoint.name!r} from "
                f"{checkpoint.path!r} failed: {err}"
            ) from err

    def discard_after(self, checkpoint: Checkpoint) -> None:
        """Forget every checkpoint newer than ``checkpoint``."""
        with self._lock:
            if checkpoint in self._checkpoints:
                index = self._checkpoints.index(checkpoint)
                stale = self._checkpoints[index + 1 :]
                del self._checkpoints[index + 1 :]
                for item in stale:
                    self._delete(item)

    # -- retention -------------------------------------------------------------

    def _prune(self, local: bool) -> None:
        while len(self._checkpoints) > self._config.keep_last:
            stale = self._checkpoints.pop(0)
            if local:
                self._delete(stale)
            else:
                logger.debug(
                    "Checkpoint %s is on the server file system and was not deleted.",
                    stale.path,
                )

    def _delete(self, checkpoint: Checkpoint) -> None:
        if not os.path.isabs(checkpoint.path):
            return
        for artifact in self._adapter.checkpoint_artifacts(
            checkpoint.path, include_data=checkpoint.include_data
        ):
            try:
                Path(artifact).unlink(missing_ok=True)
            except OSError as err:
                logger.debug("Could not delete checkpoint file %s: %s", artifact, err)
