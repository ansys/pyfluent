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

"""Transparent recovery of inactive-target *attribute access*.

Fluent raises :class:`InactiveObjectError` **client-side**, inside
``Group.__getattribute__``, the moment you navigate into an inactive branch -- for
example ``cold_inlet.thermal`` while the energy model is off. That happens before
any write reaches the settings-service layer, so it cannot be caught there.

To make inactive-target recovery fully transparent, this module installs a guarded
wrapper around ``Group.__getattribute__`` that:

* for **non-resilient** sessions (the common case) is a *zero-overhead passthrough*
  -- a module-level counter gates it, so when no resilient session is active the
  original method runs unchanged;
* for a **resilient** session, catches only the specific ``InactiveObjectError``
  raised for a child-name access, asks that session's resolver to discover (by live
  introspection) which model activates the object, and -- if one does -- retries the
  original access. If nothing activates it, the original error is re-raised
  unchanged.

The wrapper is installed once and reference-counted: each resilient session
increments the count on enable; the original behaviour is fully restored when the
count returns to zero.
"""

from __future__ import annotations

import threading

#: Number of live resilient sessions. While zero, the patched ``__getattribute__``
#: is a straight passthrough to the original (no behavioural change at all).
_resilient_sessions = 0
_lock = threading.RLock()
_installed = False
_original_getattribute = None


def _inactive_object_error_cls():
    from ansys.fluent.core.solver.flobject import InactiveObjectError

    return InactiveObjectError


def _group_cls():
    from ansys.fluent.core.solver.flobject import Group

    return Group


def _controller_for(obj):
    """Return the resilient controller governing ``obj``'s tree, or ``None``.

    Reaches the settings root's ``flproxy``; when resilient mode is enabled that
    is a ``ResilientSettingsService`` carrying the controller.
    """
    try:
        root = obj._root
        flproxy = root.flproxy
    except Exception:  # noqa: BLE001
        return None
    return getattr(flproxy, "_controller", None)


def _make_wrapper(original):
    inactive_error = _inactive_object_error_cls()

    def __getattribute__(self, name):  # noqa: N807
        # Fast path: when no resilient session is active, behave exactly like the
        # original. This keeps the hot attribute-access path unchanged for every
        # ordinary (non-resilient) session.
        if _resilient_sessions == 0:
            return original(self, name)
        try:
            return original(self, name)
        except inactive_error:
            # Only attempt recovery for a genuine child-name navigation on a
            # resilient session; otherwise re-raise unchanged.
            controller = _controller_for(self)
            if controller is None:
                raise
            resolver = getattr(controller, "_resolver", None)
            if resolver is None:
                raise
            try:
                enabled = resolver.activate_object(self)
            except Exception:  # noqa: BLE001
                enabled = []
            if not enabled:
                raise
            # Activation succeeded: retry the original access, now that the
            # governing model is on.
            return original(self, name)

    return __getattribute__


def install() -> None:
    """Install the guarded ``Group.__getattribute__`` wrapper (idempotent)."""
    global _installed, _original_getattribute
    with _lock:
        if _installed:
            return
        group = _group_cls()
        _original_getattribute = group.__getattribute__
        group.__getattribute__ = _make_wrapper(_original_getattribute)
        _installed = True


def register_session() -> None:
    """Enable the active-recovery behaviour for one more resilient session."""
    global _resilient_sessions
    install()
    with _lock:
        _resilient_sessions += 1


def unregister_session() -> None:
    """Disable active-recovery for one resilient session (ref-counted)."""
    global _resilient_sessions
    with _lock:
        if _resilient_sessions > 0:
            _resilient_sessions -= 1


def active_session_count() -> int:
    """Number of resilient sessions currently registered (for tests)."""
    return _resilient_sessions
