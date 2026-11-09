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

"""Backend-neutral connection lifecycle for the platform layer.

These pieces are independent of the communication backend (gRPC, REST, ...):

* :class:`MonitorThread` runs registered cleanup callbacks once the main thread
  finishes, guaranteeing session teardown at interpreter exit.
* :class:`ErrorState` is the default concrete error state shared across a
  connection's services; it satisfies the ``transport.ErrorState`` protocol.
* :class:`Connection` owns the generic lifecycle: the finalizer-callback
  registry, the shared monitor thread, and the exit-signalling threads. A
  backend-specific connection (such as Fluent's) subclasses it and adds its own
  transport and teardown logic.
"""

from __future__ import annotations

from collections.abc import Callable
import threading


class MonitorThread(threading.Thread):
    """Daemon thread that runs cleanup callbacks when the main thread exits.

    Ensures cleanup of session objects and shutdown of non-daemon threads.

    Attributes
    ----------
    cbs : list[Callable]
        Cleanup/shutdown functions.
    """

    def __init__(self):
        """Initialize MonitorThread."""
        super().__init__(daemon=True)
        self.cbs: list[Callable] = []

    def run(self) -> None:
        """Run monitor thread."""
        main_thread = threading.main_thread()
        main_thread.join()
        for cb in self.cbs:
            cb()


class ErrorState:
    """Indicates the error state of a connected client.

    Satisfies the :class:`~ansys.solver.core.transport.ErrorState` protocol.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> session = pyfluent.launch_fluent()
    >>> session._fluent_connection._error_state.set("test", "test details")
    >>> session._fluent_connection._error_state.name
    'test'
    >>> session._fluent_connection._error_state.details
    'test details'
    >>> session._fluent_connection._error_state.clear()
    >>> session._fluent_connection._error_state.name
    ''
    """

    @property
    def name(self):
        """Get name."""
        return self._name

    @property
    def details(self):
        """Get details."""
        return self._details

    def __init__(self, name: str = "", details: str | None = ""):
        """Initializes the error state object.

        Parameters
        ----------
            name : str
                The name of the error state, by default an empty string, indicating no errors.
            details : str
                Additional details of the error, by default an empty string.
        """
        self._name = name
        self._details = details

    def set(self, name: str, details: str):
        """Method to set the error state name and details to new values."""
        self._name = name
        self._details = details

    def clear(self):
        """Method to clear the current error state, emptying the error name and details
        properties."""
        self._name = ""
        self._details = ""


class Connection:
    """Backend-neutral connection lifecycle.

    Provides the finalizer-callback registry, a process-wide monitor thread that
    runs those callbacks at interpreter exit, and the long-running thread that
    keeps teardown work alive until exit is signalled. Subclasses add the
    backend-specific transport and build the actual finalizer.
    """

    _monitor_thread: MonitorThread | None = None

    def __init__(self) -> None:
        """Initialize the generic connection lifecycle."""
        self.finalizer_cbs: list[Callable] = []
        self._exit_event = threading.Event()
        # session.exit() is handled in the daemon thread (MonitorThread) which
        # ensures shutdown of non-daemon threads. A daemon thread is terminated
        # abruptly during interpreter exit, after all non-daemon threads exit.
        # This long-running non-daemon thread is exited at the end of exit() so
        # everything within exit() runs during interpreter shutdown.
        self._waiting_thread = threading.Thread(target=self._exit_event.wait)
        self._waiting_thread.start()

    def register_finalizer_cb(self, cb: Callable, at_start: bool = False) -> None:
        """Register a callback to run with the finalizer."""
        if at_start:
            self.finalizer_cbs.insert(0, cb)
        else:
            self.finalizer_cbs.append(cb)

    @classmethod
    def _ensure_monitor_thread(cls) -> MonitorThread:
        """Start the shared monitor thread on first use and return it."""
        if not Connection._monitor_thread:
            Connection._monitor_thread = MonitorThread()
            Connection._monitor_thread.start()
        return Connection._monitor_thread

    def _install_finalizer(self, finalizer: Callable) -> None:
        """Store the finalizer and schedule it on the shared monitor thread."""
        self._finalizer = finalizer
        self._ensure_monitor_thread().cbs.append(finalizer)
