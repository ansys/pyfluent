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

"""User-facing facade for the resilient execution runtime.

:class:`ResilientSolver` wraps a warm pool of Fluent solver sessions and exposes
a small, resilient surface: :meth:`set`, :meth:`command`, :meth:`checkpoint`,
:meth:`undo`, :meth:`redo`, and :meth:`rewind_to`. A human or an agent uses the
identical surface -- there is no dependency on ``fastmcp`` or the AI layer.

Resilience envelope per operation:

* **recoverable** errors (inactive target, out-of-range, disallowed value, wrong
  type) are repaired automatically and retried by the resolver;
* **catastrophic** (fatal) errors trigger a failover to a warm standby and a
  replay of the last good checkpoint, after which the operation is retried once;
* irreversible commands (``iterate``, ``read_case``, ...) are preceded by an
  automatic file checkpoint so they remain undoable and replayable.

Opt-in::

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core.resilient import ResilientSolver

    session = pyfluent.launch_fluent(mode="solver")
    with ResilientSolver(session, pool_size=3) as rsolver:
        rsolver.command("file.read_case_data", file_name="elbow.cas.h5")
        rsolver.set("setup.models.energy.enabled", True)
        rsolver.checkpoint("pre-iterate")
        rsolver.command("solution.run_calculation.iterate", iter_count=100)
        rsolver.undo()
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ansys.fluent.core.resilient.apply import SafeApplier
from ansys.fluent.core.resilient.checkpoint import CheckpointManager, is_irreversible
from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.pool import PoolConfig, WarmSessionPool
from ansys.fluent.core.resilient.types import CheckpointKind, StepOutcome, UndoEntry


@dataclass
class ResilientConfig:
    """Top-level configuration for a :class:`ResilientSolver`."""

    pool: PoolConfig = field(default_factory=PoolConfig)
    file_checkpoint: FileCheckpointConfig | None = None
    max_resolver_attempts: int = 3
    auto_file_checkpoint_before_irreversible: bool = True


class ResilientSolver:
    """Resilient facade over a warm pool of Fluent solver sessions."""

    def __init__(
        self,
        session=None,
        *,
        pool_size: int = 1,
        config: ResilientConfig | None = None,
        _pool: WarmSessionPool | None = None,
    ):
        if config is None:
            config = ResilientConfig(pool=PoolConfig(size=pool_size))
        elif session is not None or pool_size != 1:
            # An explicit pool_size overrides the config default when given.
            if pool_size != 1:
                config.pool.size = pool_size
        self.config = config
        self._pool = _pool or WarmSessionPool(config.pool, seed_session=session)
        self._classifier = ErrorClassifier()
        self._applier = SafeApplier(
            self._pool.active,
            classifier=self._classifier,
            max_resolver_attempts=config.max_resolver_attempts,
        )
        self._checkpoints = CheckpointManager(
            self._pool.active, file_config=config.file_checkpoint
        )

    @classmethod
    def launch(
        cls,
        *,
        pool_size: int = 1,
        config: ResilientConfig | None = None,
        **launch_kwargs,
    ) -> "ResilientSolver":
        """Launch a seed session via ``launch_fluent`` and wrap it.

        Extra keyword arguments are forwarded to ``launch_fluent`` and reused for
        any warm standbys.
        """
        import ansys.fluent.core as pyfluent

        if config is None:
            config = ResilientConfig(
                pool=PoolConfig(size=pool_size, launch_kwargs=dict(launch_kwargs))
            )
        else:
            config.pool.size = pool_size
            config.pool.launch_kwargs = dict(launch_kwargs)
        session = pyfluent.launch_fluent(**launch_kwargs)
        return cls(session, config=config)

    # -- user surface -----------------------------------------------------

    @property
    def session(self):
        """The current active solver session (changes after a failover)."""
        return self._pool.active

    @property
    def pool(self) -> WarmSessionPool:
        """The underlying warm session pool."""
        return self._pool

    @property
    def checkpoints(self) -> CheckpointManager:
        """The checkpoint manager (undo / redo stacks)."""
        return self._checkpoints

    def set(self, path: str, value) -> StepOutcome:
        """Apply ``path = value`` with auto-recovery and failover."""
        try:
            return self._applier.set(path, value)
        except Exception as err:  # noqa: BLE001
            return self._maybe_failover_and_retry(
                err, lambda: self._applier.set(path, value), path
            )

    def command(self, path: str, **kwargs) -> StepOutcome:
        """Invoke a settings command with auto file-checkpointing and failover."""
        if self.config.auto_file_checkpoint_before_irreversible and is_irreversible(
            path
        ):
            try:
                self._checkpoints.checkpoint_file(
                    f"auto:{path}", reason="pre-irreversible"
                )
            except Exception:  # noqa: BLE001  # nosec B110
                # Inability to checkpoint must not block the user's command.
                pass
        try:
            return self._applier.command(path, **kwargs)
        except Exception as err:  # noqa: BLE001
            return self._maybe_failover_and_retry(
                err, lambda: self._applier.command(path, **kwargs), path
            )

    def checkpoint(
        self, name: str, *, kind: CheckpointKind | None = None, paths=None
    ) -> UndoEntry:
        """Take an explicit checkpoint.

        ``kind`` defaults to a file checkpoint when none is given (the safest,
        broadest option); pass :attr:`CheckpointKind.SETTINGS` for a lightweight
        in-memory snapshot.
        """
        if kind is CheckpointKind.SETTINGS:
            return self._checkpoints.checkpoint_settings(name, paths)
        return self._checkpoints.checkpoint_file(name)

    def undo(self) -> UndoEntry:
        """Undo the newest checkpoint (settings restore or case reload)."""
        return self._checkpoints.undo()

    def redo(self) -> UndoEntry:
        """Redo the most recently undone checkpoint."""
        return self._checkpoints.redo()

    def rewind_to(self, name: str) -> list[UndoEntry]:
        """Undo repeatedly until the named checkpoint has been restored."""
        return self._checkpoints.rewind_to(name)

    # -- failover plumbing ------------------------------------------------

    def _maybe_failover_and_retry(self, err, retry, path: str) -> StepOutcome:
        cls = self._classifier.classify(err, self.session)
        if not cls.catastrophic:
            raise err
        standby = self._pool.failover(self._checkpoints)
        self._applier.rebind(standby)
        outcome = retry()
        outcome.failed_over = True
        return outcome

    # -- lifecycle --------------------------------------------------------

    def __enter__(self) -> "ResilientSolver":
        return self

    def __exit__(self, *exc) -> None:
        self.shutdown()

    def shutdown(self) -> None:
        """Explicit, orderly teardown of the pool (monitors + sessions)."""
        self._pool.shutdown()
