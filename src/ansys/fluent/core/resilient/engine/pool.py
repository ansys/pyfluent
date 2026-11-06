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

"""Warm standby sessions for failover.

Standbys are launched when the pool is created, so a failover does not wait for
a product launch. Health is checked on demand (when a standby is needed) rather
than by background polling. Replaced and retired sessions are exited on a
background thread so that a failover never blocks on tearing down a dead server.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Callable

from .adapter import ResilientAdapter
from .exceptions import FailoverError, ResilientError

logger = logging.getLogger("ansys.resilient")


class WarmSessionPool:
    """One active session plus ``size - 1`` warm standby sessions.

    Parameters
    ----------
    active : object
        The session in use.
    size : int
        Total number of sessions, including the active one.
    launcher : callable
        Zero-argument callable that launches a standby session.
    adapter : ResilientAdapter
        The product adapter.

    Raises
    ------
    ResilientError
        If a standby session cannot be launched.
    """

    def __init__(
        self,
        active: Any,
        *,
        size: int,
        launcher: Callable[[], Any],
        adapter: ResilientAdapter,
    ):
        self._adapter = adapter
        self._launcher = launcher
        self._size = size
        self._active = active
        self._standbys: list[Any] = []
        self._lock = threading.RLock()
        self._closed = False
        try:
            for _ in range(size - 1):
                self._standbys.append(launcher())
        except Exception as err:  # noqa: BLE001
            for standby in self._standbys:
                adapter.exit_session(standby)
            self._standbys.clear()
            raise ResilientError(
                f"Could not launch a standby {adapter.product_name} session for the "
                f"resilient pool: {err}"
            ) from err

    @property
    def active(self) -> Any:
        """Return the active session."""
        return self._active

    @property
    def standbys(self) -> list[Any]:
        """Return the warm standby sessions."""
        with self._lock:
            return list(self._standbys)

    @property
    def size(self) -> int:
        """Return the configured number of sessions, including the active one."""
        return self._size

    def take_standby(self) -> Any:
        """Remove and return a healthy standby session.

        Unhealthy standbys found on the way are exited.

        Raises
        ------
        FailoverError
            If no healthy standby is available.
        """
        with self._lock:
            while self._standbys:
                standby = self._standbys.pop(0)
                if self._adapter.is_server_healthy(standby):
                    return standby
                self._retire(standby)
        raise FailoverError(
            f"No healthy standby {self._adapter.product_name} session is available "
            "for failover."
        )

    def promote(self, standby: Any, *, retire_previous: bool = True) -> Any:
        """Make ``standby`` the active session; return the previous active session.

        The previous session is exited in the background unless
        ``retire_previous`` is ``False``, and a replacement standby is launched in
        the background.
        """
        with self._lock:
            previous = self._active
            self._active = standby
        if previous is not None and retire_previous:
            self._retire(previous)
        self._refill_in_background()
        return previous

    def release(self, session: Any) -> None:
        """Put back a standby that was taken but not promoted."""
        with self._lock:
            if self._closed:
                self._retire(session)
            else:
                self._standbys.insert(0, session)

    def shutdown(self, *, keep: Any = None) -> None:
        """Exit every session of the pool except ``keep``."""
        with self._lock:
            self._closed = True
            sessions = list(self._standbys)
            if self._active is not None:
                sessions.append(self._active)
            self._standbys.clear()
            self._active = keep
        for session in sessions:
            if session is not keep:
                self._adapter.exit_session(session)

    # -- internals -------------------------------------------------------------

    def _retire(self, session: Any) -> None:
        threading.Thread(
            target=self._adapter.exit_session,
            args=(session,),
            name="resilient-retire-session",
            daemon=True,
        ).start()

    def _refill_in_background(self) -> None:
        def refill():
            try:
                standby = self._launcher()
            except Exception as err:  # noqa: BLE001
                logger.warning(
                    "Could not launch a replacement standby session: %s", err
                )
                return
            with self._lock:
                if self._closed:
                    self._retire(standby)
                else:
                    self._standbys.append(standby)

        with self._lock:
            if self._closed or len(self._standbys) + 1 >= self._size:
                return
        threading.Thread(
            target=refill, name="resilient-refill-standby", daemon=True
        ).start()
