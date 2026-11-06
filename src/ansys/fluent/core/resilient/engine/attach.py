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

"""Enable and disable resilient mode on a live session."""

from __future__ import annotations

import dataclasses
import functools
import logging
from typing import Any, Callable

from .adapter import ResilientAdapter, instance_attr
from .config import ResilientConfig
from .controller import ResilientController
from .exceptions import ResilientError
from .journal import Journal, SetOp
from .pool import WarmSessionPool
from .types import Checkpoint, ResilientEvent, StepOutcome

logger = logging.getLogger("ansys.resilient")


class ResilientSession:
    """Resilient-mode controls of a session, available as ``session.resilient``."""

    def __init__(self, controller: ResilientController):
        self._controller = controller

    @property
    def enabled(self) -> bool:
        """Whether resilient mode is active on the session."""
        return self._controller.enabled

    @property
    def config(self) -> ResilientConfig:
        """The resilient-mode configuration."""
        return self._controller.config

    @property
    def adapter(self) -> ResilientAdapter:
        """The product adapter."""
        return self._controller.adapter

    @property
    def active_session(self) -> Any:
        """The session that currently serves settings calls.

        This is the original session until a failover, and the standby session
        that took over afterwards.
        """
        return self._controller.session

    @property
    def pool(self) -> WarmSessionPool | None:
        """The warm standby pool, or ``None`` when failover is not enabled."""
        return self._controller.pool

    @property
    def journal(self) -> Journal:
        """The journal of state-changing operations."""
        return self._controller.journal

    @property
    def checkpoints(self) -> list[Checkpoint]:
        """The retained checkpoints, oldest first."""
        return self._controller.store.checkpoints

    @property
    def last_outcome(self) -> StepOutcome | None:
        """The outcome of the most recent intercepted write or command."""
        return self._controller.last_outcome

    def checkpoint(self, name: str) -> Checkpoint:
        """Write a checkpoint that :meth:`rollback` can restore.

        Parameters
        ----------
        name : str
            Name of the checkpoint.

        Returns
        -------
        Checkpoint
            The written checkpoint.
        """
        return self._controller.checkpoint(name)

    def rollback(self, name: str | None = None) -> Checkpoint:
        """Restore the newest checkpoint, or the newest one called ``name``.

        Checkpoints written after it, and journal entries recorded after it, are
        discarded.

        Parameters
        ----------
        name : str, optional
            Name of the checkpoint to restore.

        Returns
        -------
        Checkpoint
            The restored checkpoint.
        """
        return self._controller.rollback(name)

    def undo(self) -> SetOp:
        """Undo the most recent settings value write.

        Returns
        -------
        SetOp
            The undone operation.
        """
        return self._controller.undo()

    def redo(self) -> SetOp:
        """Re-apply the most recently undone settings value write.

        Returns
        -------
        SetOp
            The redone operation.
        """
        return self._controller.redo()

    def on_event(self, listener: Callable[[ResilientEvent], None]) -> None:
        """Call ``listener`` with every :class:`ResilientEvent` of the session.

        Parameters
        ----------
        listener : callable
            Called with one :class:`ResilientEvent` argument.
        """
        self._controller.on_event(listener)

    def disable(self) -> None:
        """Turn resilient mode off and exit the standby sessions."""
        self._controller.disable()

    def __repr__(self) -> str:
        controller = self._controller
        pool = controller.pool
        standbys = len(pool.standbys) if pool is not None else 0
        return (
            f"<ResilientSession product={controller.adapter.product_name!r} "
            f"enabled={controller.enabled} recovery={controller.config.recovery.value!r} "
            f"standbys={standbys} checkpoints={len(controller.store.checkpoints)} "
            f"journal={len(controller.journal)}>"
        )


def is_resilient(session: Any) -> bool:
    """Return whether resilient mode is enabled on ``session``.

    Parameters
    ----------
    session : object
        A product session.

    Returns
    -------
    bool
        Whether resilient mode is enabled.
    """
    api = instance_attr(session, "resilient")
    return isinstance(api, ResilientSession) and api.enabled


def _standby_launcher(
    config: ResilientConfig,
    adapter: ResilientAdapter,
    session: Any,
    standby_launcher: Callable[[], Any] | None,
) -> Callable[[], Any]:
    pool = config.pool
    if pool.launcher is not None:
        return pool.launcher
    if pool.launch_kwargs is not None:
        return functools.partial(adapter.launch, **pool.launch_kwargs)
    launcher = standby_launcher or adapter.standby_launcher(session)
    if launcher is None:
        raise ResilientError(
            f"Resilient mode cannot tell how to launch standby {adapter.product_name} "
            "sessions for this session. Enable resilient mode when launching the "
            "session (resilient_mode=True), or pass PoolConfig(launch_kwargs=...) "
            "or PoolConfig(launcher=...)."
        )
    return launcher


def enable_resilient_mode(
    session: Any,
    config: ResilientConfig | None = None,
    *,
    adapter: ResilientAdapter,
    pool_size: int | None = None,
    standby_launcher: Callable[[], Any] | None = None,
    journal_complete: bool = False,
) -> Any:
    """Enable resilient mode on a live session.

    Parameters
    ----------
    session : object
        A live product session with a settings tree.
    config : ResilientConfig, optional
        Resilient-mode configuration. The default configuration is used when
        omitted. The object is not modified.
    adapter : ResilientAdapter
        The product adapter.
    pool_size : int, optional
        Shortcut for ``config.pool.size``.
    standby_launcher : callable, optional
        Zero-argument callable that launches a standby session like ``session``.
        Product launch functions pass it; it is used only when the configuration
        does not say how to launch standbys.
    journal_complete : bool, optional
        Whether ``session`` was just launched, so that the journal records its
        whole history. Product launch functions pass ``True``.

    Returns
    -------
    object
        The same session, with resilient controls available as
        ``session.resilient``.

    Raises
    ------
    ResilientError
        If resilient mode is already enabled, the session has no settings service,
        or standby sessions cannot be launched.
    """
    if is_resilient(session):
        raise ResilientError(
            "Resilient mode is already enabled on this session. Call "
            "session.resilient.disable() before enabling it again."
        )
    if adapter.settings_service(session) is None:
        raise ResilientError(
            f"This {adapter.product_name} session has no settings service; resilient "
            "mode applies only to sessions with a settings tree."
        )
    config = dataclasses.replace(config) if config is not None else ResilientConfig()
    if pool_size is not None:
        config.pool = dataclasses.replace(config.pool, size=pool_size)
    pool = None
    if config.pool.size > 1:
        pool = WarmSessionPool(
            session,
            size=config.pool.size,
            launcher=_standby_launcher(config, adapter, session, standby_launcher),
            adapter=adapter,
        )
    controller = ResilientController(
        session, config, adapter, pool=pool, journal_complete=journal_complete
    )
    controller.api = ResilientSession(controller)
    controller.bind(session)
    logger.info(
        "Resilient mode enabled on a %s session (recovery=%s, model activation=%s, "
        "pool size=%d, checkpoints in run %s).",
        adapter.product_name,
        config.recovery.value,
        config.allow_model_activation,
        config.pool.size,
        controller.run_id,
    )
    return session


def disable_resilient_mode(session: Any) -> Any:
    """Disable resilient mode on ``session``.

    Settings calls go directly to the product again and the standby sessions are
    exited. Calling this on a session without resilient mode does nothing.

    Parameters
    ----------
    session : object
        A product session.

    Returns
    -------
    object
        The same session.
    """
    api = instance_attr(session, "resilient")
    if isinstance(api, ResilientSession):
        api.disable()
    return session
