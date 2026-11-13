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

"""Keep a warm standby session up to date with the active session.

Every change that succeeds on the active session is queued for each standby and
applied there, in order, on a background thread, so the user's script never
waits for the standbys. A standby whose change fails is *out of sync*: the
following changes are skipped until a resynchronizing job (restoring a
checkpoint) brings it back to the state of the active session.
"""

from __future__ import annotations

from collections import deque
import logging
import sys
import threading
from typing import Any, Callable

logger = logging.getLogger("ansys.resilient")


class StandbyMirror:
    """Ordered queue of changes applied to one standby session.

    Parameters
    ----------
    standby : object
        The standby session.
    synced : bool
        Whether the standby already has the state of the active session.
    on_error : callable
        Called as ``on_error(mirror, description, error)`` when a change fails on
        the standby.
    """

    def __init__(
        self,
        standby: Any,
        *,
        synced: bool,
        on_error: Callable[[StandbyMirror, str, Exception], None],
    ):
        self.standby = standby
        self._synced = synced
        #: Whether any change was applied, or attempted, on the standby.
        self._touched = False
        self._on_error = on_error
        self._jobs: deque[tuple[str, Callable[[], None] | None, bool]] = deque()
        self._condition = threading.Condition()
        self._busy = False
        self._closed = False
        self._thread = threading.Thread(
            target=self._run, name="resilient-standby-mirror", daemon=True
        )
        self._thread.start()

    @property
    def synced(self) -> bool:
        """Whether the standby has the state of the active session."""
        with self._condition:
            return self._synced

    @property
    def touched(self) -> bool:
        """Whether a change was applied, or attempted, on the standby."""
        with self._condition:
            return self._touched

    @property
    def closed(self) -> bool:
        """Whether the mirror was closed."""
        with self._condition:
            return self._closed

    def invalidate(self, reason: str) -> None:
        """Mark the standby out of sync once the changes queued so far have run."""
        with self._condition:
            if self._closed:
                return
            self._jobs.append((reason, None, False))
            self._condition.notify_all()

    def submit(
        self, description: str, job: Callable[[], None], *, resync: bool = False
    ) -> None:
        """Queue ``job``.

        A ``resync`` job runs even when the standby is out of sync, and brings it
        back in sync when it succeeds. Other jobs are skipped while it is out of
        sync.
        """
        with self._condition:
            if self._closed:
                return
            self._jobs.append((description, job, resync))
            self._condition.notify_all()

    def wait(self, timeout: float | None = None) -> bool:
        """Wait until every queued job has run; return whether it did in time."""
        with self._condition:
            return self._condition.wait_for(
                lambda: self._closed or (not self._jobs and not self._busy), timeout
            )

    def close(self) -> None:
        """Stop the worker; jobs not yet started are dropped."""
        with self._condition:
            self._closed = True
            self._jobs.clear()
            self._condition.notify_all()

    def _next_job(self) -> tuple[str, Callable[[], None], bool] | None:
        with self._condition:
            while True:
                self._condition.wait_for(lambda: self._closed or bool(self._jobs))
                if self._closed:
                    return None
                description, job, resync = self._jobs.popleft()
                if job is None:
                    logger.info("Standby session out of sync: %s", description)
                    self._synced = False
                elif self._synced or resync:
                    self._busy = True
                    self._touched = True
                    return description, job, resync
                # Skipped: out of sync, this change would apply to the wrong state.
                self._condition.notify_all()

    def _run(self) -> None:
        while True:
            item = self._next_job()
            if item is None or sys.is_finalizing():
                return
            description, job, resync = item
            try:
                job()
            except Exception as err:  # noqa: BLE001
                with self._condition:
                    self._synced = False
                try:
                    self._on_error(self, description, err)
                except Exception as report_err:  # noqa: BLE001
                    logger.debug("Reporting a standby failure failed: %s", report_err)
            else:
                if resync:
                    with self._condition:
                        self._synced = True
            with self._condition:
                self._busy = False
                self._condition.notify_all()
