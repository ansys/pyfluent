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

"""Per-session fatal-error detection.

:class:`SessionHealthMonitor` combines two signals:

* **primary** -- a push-based subscription to the ``FATAL_ERROR`` solver event
  (the exact code path that sets the shared ``ErrorState``), giving near-instant,
  zero-steady-state-cost detection. The callback only flips a flag (no RPCs);
* **backstop** -- a slow daemon poll of the ``ErrorState`` name plus a health
  probe, to catch a hard crash whose event never arrived (the stream itself may
  have died).

Fatal is *sticky* (write-once-true) and all mutation is guarded by a single
``RLock`` because the event-callback thread and the poll thread both touch it.
Teardown is explicit via :meth:`stop` -- never from a finalizer, and the callback
performs no RPCs.
"""

from __future__ import annotations

import threading

from ansys.fluent.core.resilient import _compat


def _solver_fatal_event():
    """Return ``SolverEvent.FATAL_ERROR`` or ``None`` if unavailable."""
    try:
        from ansys.fluent.core.services.streaming_services.events_streaming import (
            SolverEvent,
        )

        return SolverEvent.FATAL_ERROR
    except Exception:  # noqa: BLE001
        return None


class SessionHealthMonitor:
    """Thread-safe health view of a single session."""

    def __init__(self, session, *, interval: float = 2.0):
        self.session = session
        self.interval = interval
        self._lock = threading.RLock()
        self._fatal = False
        self._details: str | None = None
        self._callback_id = None
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    # -- lifecycle --------------------------------------------------------

    def start(self) -> None:
        """Subscribe to the fatal event and start the poll backstop."""
        self._subscribe()
        if self._thread is None:
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._poll_loop,
                name="resilient-health-monitor",
                daemon=True,
            )
            self._thread.start()

    def stop(self) -> None:
        """Unsubscribe and stop the poll thread (explicit; never in a finalizer)."""
        self._stop_event.set()
        thread = self._thread
        self._thread = None
        if thread is not None and thread.is_alive():
            thread.join(timeout=self.interval + 1.0)
        self._unsubscribe()

    def _subscribe(self) -> None:
        from ansys.fluent.core.resilient.adapter import adapter_for

        events = getattr(self.session, "events", None)
        register = getattr(events, "register_callback", None)
        # Prefer the adapter's fatal event; fall back to the Fluent default.
        adapter = adapter_for(self.session)
        fatal_event = adapter.fatal_event()
        if fatal_event is None:
            fatal_event = _solver_fatal_event()
        if not callable(register) or fatal_event is None:
            return
        try:
            self._callback_id = register(fatal_event, self._on_fatal)
        except Exception:  # noqa: BLE001  # nosec B110
            self._callback_id = None

    def _unsubscribe(self) -> None:
        events = getattr(self.session, "events", None)
        unregister = getattr(events, "unregister_callback", None)
        if self._callback_id is not None and callable(unregister):
            try:
                unregister(self._callback_id)
            except Exception:  # noqa: BLE001  # nosec B110
                pass
        self._callback_id = None

    # -- signals ----------------------------------------------------------

    def _on_fatal(self, session, event_info=None) -> None:
        """Fatal-event callback. Flips the sticky flag only; performs no RPCs."""
        details = None
        message = getattr(event_info, "message", None)
        if message:
            details = str(message)
        self._mark_fatal(details)

    def _poll_loop(self) -> None:
        while not self._stop_event.wait(self.interval):
            try:
                if _compat.is_fatal(self.session):
                    self._mark_fatal(_compat.fatal_details(self.session))
                elif not _compat.is_server_healthy(self.session):
                    self._mark_fatal("Fluent server is no longer serving.")
            except Exception:  # noqa: BLE001  # nosec B112
                continue

    def _mark_fatal(self, details: str | None) -> None:
        with self._lock:
            if not self._fatal:
                self._fatal = True
                self._details = details

    # -- queries ----------------------------------------------------------

    def is_fatal(self) -> bool:
        """Whether a fatal state has been observed (sticky)."""
        with self._lock:
            return self._fatal

    def is_healthy(self) -> bool:
        """Whether the session is not fatal and the server is serving."""
        if self.is_fatal():
            return False
        return _compat.is_server_healthy(self.session)

    def details(self) -> str | None:
        """The fatal-error details, if any."""
        with self._lock:
            return self._details
