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

"""Warm pool of Fluent sessions with health monitoring and failover.

One session is *active*; the rest are warm standbys launched eagerly (when
``size > 1``). Each session is watched by a :class:`SessionHealthMonitor`. On a
catastrophic (fatal) error the pool promotes a healthy standby and replays the
*last good checkpoint* onto it -- a fatal session's RPCs are refused, so its state
is never read; recovery relies solely on the last checkpoint.

The default ``size`` is **1**, which disables failover (there is nothing to fail
over to); users opt into ``N > 1`` to pay for warm standbys (N licenses + N x
RAM/cores).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import threading

from ansys.fluent.core.resilient.exceptions import FailoverError
from ansys.fluent.core.resilient.health import SessionHealthMonitor
from ansys.fluent.core.resilient.types import CheckpointKind


@dataclass
class PoolConfig:
    """Configuration for the warm session pool."""

    #: Total number of live sessions (1 active + ``size - 1`` warm standbys).
    size: int = 1
    #: Keyword arguments forwarded to ``launch_fluent`` for standbys.
    launch_kwargs: dict = field(default_factory=dict)
    #: Health-monitor poll interval (seconds).
    health_interval: float = 2.0
    #: Replay strategy after failover: "auto" | "settings" | "file".
    replay_from: str = "auto"


def _launch_session(launch_kwargs: dict):
    """Launch a fresh Fluent session via the public entry point (default)."""
    import ansys.fluent.core as pyfluent

    return pyfluent.launch_fluent(**launch_kwargs)


class WarmSessionPool:
    """A pool of live Fluent sessions supporting failover + checkpoint replay."""

    def __init__(
        self,
        config: PoolConfig | None = None,
        *,
        seed_session=None,
        launcher=None,
    ):
        self.config = config or PoolConfig()
        if launcher is None and seed_session is not None:
            # Launch standbys via the seed session's product adapter, so the pool
            # works for any product (Fluent, CFX, ...).
            from ansys.fluent.core.resilient.adapter import adapter_for

            adapter = adapter_for(seed_session)
            launcher = lambda kw: adapter.launch(**kw)  # noqa: E731
        self._launcher = launcher or _launch_session
        self._lock = threading.RLock()
        self._sessions: list = []
        self._monitors: dict[int, SessionHealthMonitor] = {}
        self._active = None
        if seed_session is not None:
            self._adopt(seed_session, make_active=True)
        self._fill()

    # -- construction helpers --------------------------------------------

    def _fill(self) -> None:
        """Launch warm standbys until the pool reaches ``config.size``."""
        with self._lock:
            while len(self._sessions) < max(1, self.config.size):
                session = self._launcher(self.config.launch_kwargs)
                make_active = self._active is None
                self._adopt(session, make_active=make_active)

    def _adopt(self, session, *, make_active: bool) -> None:
        monitor = SessionHealthMonitor(session, interval=self.config.health_interval)
        monitor.start()
        self._sessions.append(session)
        self._monitors[id(session)] = monitor
        if make_active:
            self._active = session

    # -- queries ----------------------------------------------------------

    @property
    def active(self):
        """The current active session."""
        return self._active

    @property
    def size(self) -> int:
        """Number of live sessions currently in the pool."""
        with self._lock:
            return len(self._sessions)

    def active_is_fatal(self) -> bool:
        """Whether the active session has entered a fatal state."""
        monitor = self._monitors.get(id(self._active))
        return bool(monitor and monitor.is_fatal())

    # -- standby management ----------------------------------------------

    def acquire_standby(self):
        """Return the healthiest standby, lazily refilling the pool afterwards.

        Raises
        ------
        FailoverError
            If no healthy standby is available.
        """
        with self._lock:
            for session in self._sessions:
                if session is self._active:
                    continue
                monitor = self._monitors.get(id(session))
                if monitor is None or monitor.is_healthy():
                    return session
        raise FailoverError(
            "No healthy standby session is available for failover. Increase "
            "pool size (pool_size > 1) to enable resilient failover."
        )

    # -- failover ---------------------------------------------------------

    def failover(self, checkpoint_mgr) -> object:
        """Promote a standby and replay the last good checkpoint onto it.

        The dead (fatal) session is retired without any state read -- its RPCs
        are refused. Returns the new active session.

        Raises
        ------
        FailoverError
            If no standby is available or replay fails.
        """
        with self._lock:
            dead = self._active
            standby = self.acquire_standby()
            self._replay(checkpoint_mgr, standby)
            self._active = standby
            checkpoint_mgr.rebind(standby)
            self._retire(dead)
            self._refill_async()
            return standby

    def _replay(self, checkpoint_mgr, standby) -> None:
        strategy = self.config.replay_from
        file_entry = checkpoint_mgr.newest_file_checkpoint()
        last = checkpoint_mgr.last_good()
        try:
            if strategy == "settings":
                if last is not None:
                    checkpoint_mgr.replay(last)
                return
            # "file" or "auto": reload the newest case/data base first.
            if file_entry is not None:
                checkpoint_mgr.rebind(standby)
                checkpoint_mgr.replay(file_entry)
            if (
                strategy == "auto"
                and last is not None
                and last.kind is CheckpointKind.SETTINGS
            ):
                checkpoint_mgr.replay(last)
            if file_entry is None and last is None:
                raise FailoverError(
                    "No checkpoint is available to replay onto the standby; "
                    "take a checkpoint before risky operations."
                )
        except FailoverError:
            raise
        except Exception as err:  # noqa: BLE001
            raise FailoverError(
                f"Failed to replay checkpoint onto the standby session: {err}"
            ) from err

    def _retire(self, session) -> None:
        if session is None:
            return
        monitor = self._monitors.pop(id(session), None)
        if monitor is not None:
            try:
                monitor.stop()
            except Exception:  # noqa: BLE001  # nosec B110
                pass
        if session in self._sessions:
            self._sessions.remove(session)
        # Tear the dead session down off the critical path; never in a finalizer.
        thread = threading.Thread(target=self._safe_exit, args=(session,), daemon=True)
        thread.start()

    @staticmethod
    def _safe_exit(session) -> None:
        exit_fn = getattr(session, "exit", None)
        if callable(exit_fn):
            try:
                exit_fn()
            except Exception:  # noqa: BLE001  # nosec B110
                pass

    def _refill_async(self) -> None:
        if len(self._sessions) >= max(1, self.config.size):
            return
        thread = threading.Thread(target=self._refill, daemon=True)
        thread.start()

    def _refill(self) -> None:
        try:
            with self._lock:
                while len(self._sessions) < max(1, self.config.size):
                    session = self._launcher(self.config.launch_kwargs)
                    self._adopt(session, make_active=False)
        except Exception:  # noqa: BLE001  # nosec B110
            # A standby refill failure must not crash the active workflow.
            pass

    # -- teardown ---------------------------------------------------------

    def shutdown(self) -> None:
        """Explicit, orderly teardown of all monitors and sessions."""
        with self._lock:
            for monitor in self._monitors.values():
                try:
                    monitor.stop()
                except Exception:  # noqa: BLE001  # nosec B110
                    pass
            self._monitors.clear()
            sessions = list(self._sessions)
            self._sessions.clear()
            self._active = None
        for session in sessions:
            self._safe_exit(session)
