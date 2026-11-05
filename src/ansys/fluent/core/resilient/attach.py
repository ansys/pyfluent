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

"""Attach transparent resilient mode to a live solver session.

:func:`enable_resilient_mode` turns an ordinary :class:`Solver` into a
resilience-enabled one *in place*, without changing the user-facing API:

* it wraps the session's settings service with
  :class:`~ansys.fluent.core.resilient.interceptor.ResilientSettingsService`, so
  every ``obj.x = v`` / ``obj.set_state(v)`` / ``command(...)`` on the settings
  tree is transparently classified, auto-recovered, checkpointed and (optionally)
  failed over;
* it attaches ``checkpoint`` / ``undo`` / ``redo`` / ``rewind_to`` /
  ``last_outcome`` / ``resilient_checkpoints`` members to the session; and
* it stores the owning :class:`ResilientController` as ``session._resilient``.

This is the function behind ``launch_fluent(..., resilient_mode=True)`` and
``Solver.from_install(..., resilient_mode=True)``, and it can also be called
directly on an already-connected session.
"""

from __future__ import annotations

from ansys.fluent.core.resilient.controller import ResilientController
from ansys.fluent.core.resilient.interceptor import ResilientSettingsService
from ansys.fluent.core.resilient.pool import PoolConfig, WarmSessionPool
from ansys.fluent.core.resilient.types import CheckpointKind


def enable_resilient_mode(
    session, config=None, *, pool_size: int | None = None, adapter=None
):
    """Enable transparent resilient mode on a live solver session.

    Parameters
    ----------
    session :
        A live solver session.
    config : ResilientConfig, optional
        Full configuration. When omitted a default is created.
    pool_size : int, optional
        Convenience override for the warm-pool size. ``1`` (default) wraps the
        single session with no failover; ``> 1`` launches warm standbys.
    adapter : ResilientAdapter, optional
        The product adapter (Fluent, CFX, ...). When omitted, the Fluent adapter
        is used. The adapter is the single seam that makes the engine reusable
        across products; it is attached to the session so a process can drive
        multiple products concurrently.

    Returns
    -------
    The same ``session``, now resilience-enabled, for chaining.
    """
    # Imported here to avoid a circular import (solver.py imports this module's
    # siblings indirectly).
    from ansys.fluent.core.resilient.solver import ResilientConfig

    if config is None:
        config = ResilientConfig()
    if pool_size is not None:
        config.pool.size = pool_size

    # Resolve and attach the product adapter BEFORE anything else reads it.
    if adapter is None:
        from ansys.fluent.core.resilient.fluent_adapter import FluentAdapter

        adapter = FluentAdapter()
    session._resilient_adapter = adapter

    pool = None
    if config.pool.size and config.pool.size > 1:
        pool = WarmSessionPool(config.pool, seed_session=session)
        session = pool.active
        session._resilient_adapter = adapter

    controller = ResilientController(session, config, pool=pool)

    # Wrap the live settings service and force the settings tree to rebind to it.
    inner_service = adapter.settings_service(session)
    wrapped = ResilientSettingsService(inner_service, controller)
    adapter.set_settings_service(session, wrapped)
    # Drop any cached settings root so it is rebuilt against the wrapped service.
    adapter.invalidate_settings_cache(session)

    _attach_session_api(session, controller)
    session._resilient = controller
    # Enable product-specific recovery of inactive-target attribute access (e.g.
    # the Fluent Group.__getattribute__ guard). A no-op when the product does not
    # raise such errors during navigation.
    from ansys.fluent.core.resilient import patch as _patch

    unregister = adapter.install_inactive_patch(
        _patch.register_session, _patch.unregister_session, _patch._controller_for
    )
    if unregister is None:
        # Default behaviour (Fluent): use the built-in patch registration.
        _patch.register_session()
    return session


def _attach_session_api(session, controller: ResilientController) -> None:
    """Attach the resilient convenience methods onto the session object."""

    def checkpoint(name, *, kind: CheckpointKind | None = None, paths=None):
        """Take an explicit checkpoint (file checkpoint by default)."""
        return controller.checkpoint(name, kind=kind, paths=paths)

    def undo():
        """Undo the newest checkpoint (settings restore or case reload)."""
        return controller.undo()

    def redo():
        """Redo the most recently undone checkpoint."""
        return controller.redo()

    def rewind_to(name):
        """Undo repeatedly until the named checkpoint is restored."""
        return controller.rewind_to(name)

    # Bind as plain attributes (functions), which is sufficient for instances.
    session.checkpoint = checkpoint
    session.undo = undo
    session.redo = redo
    session.rewind_to = rewind_to
    # Read-only-ish convenience: direct access to the undo / redo stacks.
    session.resilient_checkpoints = controller.checkpoints


def is_resilient(session) -> bool:
    """Whether resilient mode has been enabled on ``session``."""
    return getattr(session, "_resilient", None) is not None


def last_outcome(session):
    """The :class:`StepOutcome` of the most recent intercepted write, if any."""
    service = getattr(session, "_settings_service", None)
    return getattr(service, "last_outcome", None)


def on_journal_event(session, listener) -> None:
    """Register a journal ``(event_name, op)`` listener on a resilient session.

    ``event_name`` is one of ``"record"`` / ``"undo"`` / ``"redo"``. Use this to
    surface the automatic undo/redo recovery cycle (e.g. in a demo's logs).
    """
    controller = getattr(session, "_resilient", None)
    if controller is not None:
        controller.on_journal_event(listener)
