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

"""The resilient controller: all resilient state and behavior of one session."""

from __future__ import annotations

from contextlib import contextmanager
import functools
import logging
import sys
import threading
import time
from typing import Any, Callable, Iterator, NoReturn
import uuid
import warnings
import weakref

from .adapter import ResilientAdapter
from .checkpoint import CheckpointStore
from .classifier import ErrorClassifier
from .config import ResilientConfig
from .exceptions import (
    CheckpointError,
    FailoverError,
    ResilientError,
    ResilientFailoverWarning,
    ResilientWarning,
)
from .interceptor import ResilientSettingsService
from .journal import CommandOp, Journal, ObjectOp, Operation, SetOp
from .mirror import StandbyMirror
from .pool import WarmSessionPool
from .types import (
    Checkpoint,
    Classification,
    EventKind,
    ResilientEvent,
    StepOutcome,
    brief,
)

logger = logging.getLogger("ansys.resilient")

#: Execution modes of a settings call (per thread).
_NORMAL, _INTERNAL, _UNTRACKED = "normal", "internal", "untracked"


def _add_note(err: BaseException, note: str) -> None:
    """Attach a note to an exception (shown in tracebacks on Python 3.11+)."""
    add_note = getattr(err, "add_note", None)
    if callable(add_note):
        add_note(note)


def _summary(text: str, limit: int = 120) -> str:
    """Return the first line of ``text``, shortened to ``limit`` characters."""
    lines = str(text).strip().splitlines()
    line = lines[0] if lines else ""
    return line if len(line) <= limit else line[: limit - 3].rstrip() + "..."


def _warn_degraded(message: str) -> None:
    """Report that resilient mode could not do what it normally does."""
    logger.warning(message)
    warnings.warn(message, ResilientWarning, stacklevel=4)


def _standby_added_hook(controller: ResilientController) -> Callable[[Any], None]:
    """Return a pool hook that mirrors new standbys, without keeping ``controller``."""
    controller_ref = weakref.ref(controller)

    def added(standby: Any) -> None:
        controller = controller_ref()
        if controller is not None and controller.enabled:
            controller._add_mirror(standby)

    return added


class ResilientController:
    """Resilient state of one session: journal, checkpoints, recovery and failover.

    The controller is created by :func:`enable_resilient_mode`; users interact with
    it through ``session.resilient``.

    Parameters
    ----------
    session : object
        The product session.
    config : ResilientConfig
        Resilient-mode configuration.
    adapter : ResilientAdapter
        The product adapter.
    pool : WarmSessionPool, optional
        Warm standby sessions for failover.
    journal_complete : bool, optional
        Whether the journal records the session from its launch, so that a standby
        launched the same way can be brought to the same state by replaying it.
    """

    def __init__(
        self,
        session: Any,
        config: ResilientConfig,
        adapter: ResilientAdapter,
        *,
        pool: WarmSessionPool | None = None,
        journal_complete: bool = False,
    ):
        self.session = session
        self.config = config
        self.adapter = adapter
        self.pool = pool
        self.run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
        self.journal = Journal(max_ops=config.journal_max_ops)
        self.store = CheckpointStore(adapter, config.checkpoint, run_id=self.run_id)
        self.last_outcome: StepOutcome | None = None
        self.enabled = True
        self._classifier = ErrorClassifier(adapter)
        self._journal_complete = journal_complete
        self._listeners: list[Callable[[ResilientEvent], None]] = []
        self._thread_state = threading.local()
        self._bound_sessions: list[Any] = []
        self._retiring: set[int] = set()
        #: Retired sessions, kept alive so that their ids cannot be reused.
        self._retired: list[Any] = []
        self._failover_lock = threading.RLock()
        #: The session object the user enabled resilient mode on.
        self._origin = session
        self.proxy = ResilientSettingsService(adapter.settings_service(session), self)
        self.api: Any = None
        #: Standby mirrors, by ``id`` of their standby session.
        self._mirrors: dict[int, StandbyMirror] = {}
        #: Keeps journal records and the changes queued for standbys in one order.
        self._mirror_lock = threading.RLock()
        if pool is not None:
            for standby in pool.standbys:
                self._add_mirror(standby)
            pool.on_standby_added = _standby_added_hook(self)

    # -- execution modes -------------------------------------------------------

    def _mode(self) -> str:
        return getattr(self._thread_state, "mode", _NORMAL)

    @contextmanager
    def _in_mode(self, mode: str) -> Iterator[None]:
        previous = self._mode()
        # Untracked calls stay untracked even if nested inside internal calls.
        self._thread_state.mode = _UNTRACKED if previous == _UNTRACKED else mode
        try:
            yield
        finally:
            self._thread_state.mode = previous

    @property
    def _inner(self) -> Any:
        return self.proxy.inner

    # -- binding sessions -------------------------------------------------------

    def bind(self, session: Any) -> None:
        """Route ``session``'s settings calls through this controller."""
        self.adapter.set_settings_service(session, self.proxy)
        self.adapter.invalidate_settings_cache(session)
        session.resilient = self.api
        self._bound_sessions.append(session)
        self.adapter.register_exit_callback(session, self._exit_callback(session))

    def _exit_callback(self, session: Any) -> Callable[[], None]:
        controller_ref = weakref.ref(self)
        session_id = id(session)

        def on_exit() -> None:
            controller = controller_ref()
            if controller is None or sys.is_finalizing():
                return
            if session_id in controller._retiring or controller.pool is None:
                return
            # The user exited a session of this resilient run: exit the standbys.
            controller._close_mirrors()
            controller.pool.shutdown(keep=session)

        return on_exit

    def _retire(self, session: Any) -> None:
        self._retiring.add(id(session))
        self._retired.append(session)

    # -- events ------------------------------------------------------------------

    def on_event(self, listener: Callable[[ResilientEvent], None]) -> None:
        """Register a listener called with every :class:`ResilientEvent`."""
        self._listeners.append(listener)

    def _emit(
        self,
        kind: EventKind,
        message: str,
        *,
        path: str | None = None,
        warning: type[Warning] | None = None,
        **data: Any,
    ) -> None:
        if warning is not None:
            logger.warning(message)
            warnings.warn(message, warning, stacklevel=3)
        else:
            logger.info(message)
        event = ResilientEvent(kind=kind, message=message, path=path, data=data)
        for listener in list(self._listeners):
            try:
                listener(event)
            except Exception as err:  # noqa: BLE001
                logger.warning("A resilient event listener failed: %s", err)

    # -- value writes ------------------------------------------------------------

    def apply_set(self, path: str, value: Any) -> None:
        """Handle an intercepted ``set_var`` call."""
        mode = self._mode()
        if not self.enabled or mode == _UNTRACKED:
            self._inner.set_var(path, value)
            return
        if mode == _INTERNAL:
            old, known = self._read(self._inner, path)
            self._inner.set_var(path, value)
            self._record(SetOp(path, value, old, known))
            return
        session = self.session
        try:
            outcome = self._set(self._inner, path, value)
        except Exception as err:  # noqa: BLE001
            self._fail_over_without_repeating(err, session, path)
        self.last_outcome = outcome

    @staticmethod
    def _read(inner: Any, path: str) -> tuple[Any, bool]:
        if not path:
            # Reading the whole tree is too expensive to do before every write.
            return None, False
        try:
            return inner.get_var(path), True
        except Exception:  # noqa: BLE001
            return None, False

    def _set(self, inner: Any, path: str, value: Any) -> StepOutcome:
        old, known = self._read(inner, path)
        inner.set_var(path, value)
        self._record(SetOp(path, value, old, known))
        return StepOutcome(
            path=path,
            ok=True,
            old_value=brief(old) if known else None,
            new_value=brief(value),
        )

    # -- commands and structural changes -------------------------------------------

    def apply_command(self, path: str, command: str, kwds: dict[str, Any]) -> Any:
        """Handle an intercepted ``execute_cmd`` call."""
        if not self.enabled or self._mode() != _NORMAL:
            return self._inner.execute_cmd(path, command, **kwds)
        full = f"{path}/{command}" if path else command
        session = self.session
        checkpoint = None
        if self.config.auto_checkpoint and self.adapter.is_irreversible(full):
            checkpoint = self._auto_checkpoint(full)
        try:
            result = self._inner.execute_cmd(path, command, **kwds)
        except Exception as err:  # noqa: BLE001
            return self._command_failed(err, session, path, command, kwds, checkpoint)
        self._record_command(path, command, kwds, checkpoint)
        self.last_outcome = StepOutcome(path=full, ok=True, result=brief(result))
        return result

    def _record_command(
        self,
        path: str,
        command: str,
        kwds: dict[str, Any],
        checkpoint: Checkpoint | None,
        *,
        mirror: bool = True,
    ) -> None:
        full = f"{path}/{command}" if path else command
        self._record(
            CommandOp(
                path,
                command,
                dict(kwds),
                irreversible=self.adapter.is_irreversible(full),
                checkpoint=checkpoint.name if checkpoint else None,
            ),
            mirror=mirror,
        )

    def _command_failed(
        self,
        err: Exception,
        session: Any,
        path: str,
        command: str,
        kwds: dict[str, Any],
        checkpoint: Checkpoint | None,
    ) -> Any:
        full = f"{path}/{command}" if path else command
        cls = self._classifier.classify(
            err, session, interruptible=self.adapter.is_interruptible(full)
        )
        if cls.benign:
            # The command stopped part way, so repeating it on a standby would not
            # give the same state. Standbys resynchronize at the next checkpoint.
            self._record_command(path, command, kwds, checkpoint, mirror=False)
            self.last_outcome = StepOutcome(path=full, ok=True, result="interrupted")
            return None
        if cls.catastrophic:
            self._fail_over_without_repeating(err, session, full, cls)
        outcome = StepOutcome(path=full, ok=False, error=str(err))
        if self.config.auto_rollback and checkpoint is not None:
            try:
                self._restore(checkpoint)
            except Exception as restore_err:  # noqa: BLE001
                logger.error(
                    "Could not roll back to checkpoint %r after %s failed: %s",
                    checkpoint.name,
                    full,
                    restore_err,
                )
                _add_note(
                    err,
                    f"Resilient mode could not restore checkpoint {checkpoint.name!r}: "
                    f"{restore_err}",
                )
            else:
                outcome.rolled_back = True
                message = (
                    f"{self.adapter.command_name(full)} failed; restored checkpoint "
                    f"{checkpoint.name!r}, the state before the command."
                )
                _add_note(err, f"Resilient mode: {message}")
                self._emit(
                    EventKind.ROLLBACK,
                    message,
                    path=full,
                    checkpoint=checkpoint.to_dict(),
                    error=str(err),
                )
        self.last_outcome = outcome
        raise err

    def apply_object_change(
        self, method: str, path: str, args: tuple[Any, ...]
    ) -> None:
        """Handle an intercepted ``create`` / ``delete`` / ``rename`` / resize call."""
        if not self.enabled or self._mode() == _UNTRACKED:
            getattr(self._inner, method)(path, *args)
            return

        def call(inner: Any) -> StepOutcome:
            getattr(inner, method)(path, *args)
            self._record(ObjectOp(method, path, tuple(args)))
            return StepOutcome(path=path, ok=True, result=method)

        session = self.session
        try:
            outcome = call(self._inner)
        except Exception as err:  # noqa: BLE001
            self._fail_over_without_repeating(err, session, path, method=method)
        self.last_outcome = outcome

    # -- reads ---------------------------------------------------------------------

    def apply_query(
        self, method: str, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> Any:
        """Handle a delegated read; fail over if the server died.

        Reads have no side effects, so a read that fails because the server died
        is repeated on the standby that takes over.

        Raises
        ------
        Exception
            The error of the read when it is not caused by a dead server, or when
            no standby is configured.
        """
        session = self.session
        try:
            return getattr(self._inner, method)(*args, **kwargs)
        except Exception as err:  # noqa: BLE001
            if not self.enabled or self.pool is None or self._mode() != _NORMAL:
                raise
            cls = self._classifier.classify(err, session)
            if not cls.catastrophic:
                raise
            inner = self._failover(cls, session)
            return getattr(inner, method)(*args, **kwargs)

    # -- failover -----------------------------------------------------------------

    def _no_pool_note(self) -> str:
        return (
            f"The {self.adapter.product_name} server is no longer usable. Enable "
            "warm standby sessions (PoolConfig(size=2) or more) for automatic "
            "failover."
        )

    def _fail_over_without_repeating(
        self,
        err: Exception,
        session: Any,
        path: str,
        cls: Classification | None = None,
        *,
        method: str | None = None,
    ) -> NoReturn:
        """Fail over after a write or command hit a dead server, then raise ``err``.

        The call is not repeated on the standby: if the call is what made the
        server fail, repeating it would make the standby fail too. The standby
        takes over with the state from before the call, because only calls that
        succeeded are applied to standbys.

        Raises
        ------
        Exception
            ``err``, with a note saying what resilient mode did.
        FailoverError
            If no standby can take over.
        """
        if cls is None:
            cls = self._classifier.classify(err, session)
        if not cls.catastrophic:
            raise err
        if self.pool is None:
            _add_note(err, self._no_pool_note())
            raise err
        self._failover(cls, session)
        product = self.adapter.product_name
        call = self._display_path(path)
        if method is not None:
            call = f"{method} {call}"
        _add_note(
            err,
            f"Resilient mode: the {product} server failed during {call}. A "
            "standby session took over with the state from before this call. The "
            "call was not repeated, because it may be what made "
            f"{product} fail. Run it again to apply it.",
        )
        self.last_outcome = StepOutcome(
            path=path, ok=False, error=str(err), failed_over=True
        )
        raise err

    def _failover(self, cls: Classification, failed: Any) -> Any:
        """Replace the dead session ``failed`` with a standby; return its service.

        Raises
        ------
        FailoverError
            If no standby is available or the standby cannot be brought to the
            state of the dead session.
        """
        with self._failover_lock:
            if failed is not self.session:
                # Another thread already replaced the failed session.
                return self._inner
            return self._replace_active_session(cls)

    def _replace_active_session(self, cls: Classification) -> Any:
        product = self.adapter.product_name
        reason = _summary(cls.details or cls.message, limit=80)
        logger.error("The active %s session failed: %s", product, reason)
        standby, mirror = self._take_standby()
        try:
            if mirror is None or not mirror.synced:
                # Not kept up to date: rebuild it from a checkpoint and the journal.
                self._replay_onto(
                    standby, touched=mirror is not None and mirror.touched
                )
        except Exception as err:  # noqa: BLE001
            self._retire(standby)
            self.adapter.exit_session(standby)
            raise FailoverError(
                f"A standby {product} session could not be brought to the state of "
                f"the failed session: {err}"
            ) from err
        dead = self.session
        # The user's own session object is left for the user to exit: its exit
        # then shuts down the pool. Sessions promoted earlier are exited here.
        retire = dead is not self._origin
        if retire:
            self._retire(dead)
        self.pool.promote(standby, retire_previous=retire)
        self.session = standby
        self.proxy.rebind_inner(self.adapter.settings_service(standby))
        self.bind(standby)
        self._emit(
            EventKind.FAILOVER,
            f"The {product} session failed and a standby took over with the same "
            "state; settings calls now go to it (use session.resilient."
            f"active_session for other services). Cause: {reason}",
            warning=ResilientFailoverWarning,
        )
        return self._inner

    def _take_standby(self) -> tuple[Any, StandbyMirror | None]:
        """Take a standby, preferring one in sync, once it applied queued changes.

        Raises
        ------
        FailoverError
            If no healthy standby is available.
        """
        while True:
            with self._mirror_lock:
                mirrors = dict(self._mirrors)

            def in_sync(standby: Any, mirrors: dict = mirrors) -> bool:
                mirror = mirrors.get(id(standby))
                return mirror is not None and mirror.synced

            standby = self.pool.take_standby(prefer=in_sync)
            with self._mirror_lock:
                mirror = self._mirrors.pop(id(standby), None)
                self._close_stale_mirrors()
            if mirror is None:
                return standby, None
            caught_up = self._wait_for_mirror(mirror)
            mirror.close()
            if caught_up:
                return standby, mirror
            # The standby died while applying changes; try another one.
            self._retire(standby)
            self.adapter.exit_session(standby)

    def _wait_for_mirror(self, mirror: StandbyMirror) -> bool:
        """Wait for ``mirror``'s queued changes; return whether its server is alive."""
        while not mirror.wait(timeout=1.0):
            if not self.adapter.is_server_healthy(mirror.standby):
                return False
        return self.adapter.is_server_healthy(mirror.standby)

    def _replay_onto(self, standby: Any, *, touched: bool = False) -> None:
        base = self.store.newest()
        if base is not None:
            self.store.restore(standby, base)
            start = base.journal_seq
        elif self._journal_complete and not touched:
            start = 0
        else:
            raise FailoverError(
                "No checkpoint has been written, and the standby cannot be rebuilt "
                "from the journal alone. Call session.resilient.checkpoint() "
                "before risky work."
            )
        inner = self.adapter.settings_service(standby)
        for op in self.journal.live_since(start):
            self._apply_op(inner, op)

    def _apply_op(self, inner: Any, op: Operation) -> None:
        """Apply a journaled operation through the settings service ``inner``."""
        if isinstance(op, SetOp):
            inner.set_var(op.path, op.new_value)
        elif isinstance(op, CommandOp):
            if self.adapter.is_replayable(op.full_path):
                inner.execute_cmd(op.path, op.command, **op.args)
        else:
            getattr(inner, op.method)(op.path, *op.args)

    # -- keeping standbys up to date -------------------------------------------------

    def _record(self, op: Operation, *, mirror: bool = True) -> None:
        """Journal a change that succeeded on the active session; queue it for standbys.

        With ``mirror=False``, the standbys are marked out of sync instead.
        """
        with self._mirror_lock:
            self.journal.record(op)
            if not mirror:
                for standby_mirror in self._mirrors.values():
                    standby_mirror.invalidate(f"{op.describe()} was not repeated")
                return
            if isinstance(op, CommandOp) and not self.adapter.is_replayable(
                op.full_path
            ):
                return
            for standby_mirror in self._mirrors.values():
                standby_mirror.submit(
                    op.describe(),
                    functools.partial(self._apply_to, standby_mirror.standby, op),
                )

    def _apply_to(self, standby: Any, op: Operation) -> None:
        self._apply_op(self.adapter.settings_service(standby), op)

    def _mirror_value(self, path: str, value: Any, description: str) -> None:
        """Queue a value write that is not a journal record (undo and redo)."""
        for standby_mirror in self._mirrors.values():
            service = functools.partial(
                self.adapter.settings_service, standby_mirror.standby
            )
            standby_mirror.submit(
                description,
                lambda service=service: service().set_var(path, value),
            )

    def _add_mirror(self, standby: Any) -> None:
        """Start keeping ``standby`` up to date, after catching it up."""
        with self._mirror_lock:
            if id(standby) in self._mirrors:
                return
            mirror = StandbyMirror(standby, synced=False, on_error=self._mirror_failed)
            self._mirrors[id(standby)] = mirror
            self._catch_up(mirror)

    def _catch_up(self, mirror: StandbyMirror, base: Checkpoint | None = None) -> None:
        """Queue the job that brings ``mirror``'s standby to the active state.

        The standby is restored from ``base`` (by default the newest checkpoint),
        then the operations journaled since are applied. Without a checkpoint, an
        untouched standby is caught up from the journal if it covers the session
        from its launch; otherwise it stays out of sync until a checkpoint exists.
        Call with ``_mirror_lock`` held.
        """
        if base is None:
            base = self.store.newest()
        if base is not None:
            start = base.journal_seq
        elif self._journal_complete and not mirror.touched:
            start = 0
        else:
            return
        try:
            ops = self.journal.live_since(start)
        except ResilientError as err:
            logger.warning("A standby session cannot be caught up yet: %s", err)
            return
        standby = mirror.standby

        def catch_up() -> None:
            if base is not None:
                self.store.restore(standby, base)
            inner = self.adapter.settings_service(standby)
            for op in ops:
                self._apply_op(inner, op)

        source = f"checkpoint {base.name!r}" if base is not None else "the journal"
        mirror.submit(f"catching up from {source}", catch_up, resync=True)

    def _mirror_failed(
        self, mirror: StandbyMirror, description: str, err: Exception
    ) -> None:
        if mirror.closed or not self.enabled:
            return
        message = (
            f"A standby {self.adapter.product_name} session could not apply "
            f"{description}: {_summary(err)}. It is out of sync until the next "
            "checkpoint brings it back."
        )
        logger.warning(message)
        warnings.warn(message, ResilientWarning, stacklevel=2)

    def _close_stale_mirrors(self) -> None:
        """Close the mirrors of standbys that left the pool. Call with the lock held."""
        current = {id(standby) for standby in self.pool.standbys}
        for key in [key for key in self._mirrors if key not in current]:
            self._mirrors.pop(key).close()

    def _close_mirrors(self) -> None:
        with self._mirror_lock:
            for mirror in self._mirrors.values():
                mirror.close()
            self._mirrors.clear()

    def wait_for_standbys(self, timeout: float | None = None) -> bool:
        """Wait until every standby applied the changes queued for it.

        Returns
        -------
        bool
            Whether every standby applied them within ``timeout`` seconds and is
            in sync with the active session.
        """
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._mirror_lock:
            mirrors = list(self._mirrors.values())
        for mirror in mirrors:
            remaining = None if deadline is None else deadline - time.monotonic()
            if not mirror.wait(remaining) or not mirror.synced:
                return False
        return True

    # -- checkpoints, rollback, undo and redo ---------------------------------------

    def _auto_checkpoint(self, full: str) -> Checkpoint | None:
        try:
            with self._in_mode(_UNTRACKED):
                possible = self.adapter.can_checkpoint(self.session)
        except Exception as err:  # noqa: BLE001
            _warn_degraded(
                f"No automatic checkpoint before {full}; it cannot be rolled back if "
                f"it fails: {_summary(err)}"
            )
            return None
        if not possible:
            logger.debug(
                "No automatic checkpoint before %s: nothing to save yet.", full
            )
            return None
        name = f"auto-{self.adapter.command_name(full)}"
        try:
            checkpoint = self._write_checkpoint(
                name, before=self.adapter.command_name(full)
            )
        except Exception as err:  # noqa: BLE001
            _warn_degraded(
                f"The automatic checkpoint before {full} failed; it cannot be rolled "
                f"back if it fails: {_summary(err)}"
            )
            return None
        return checkpoint

    def _write_checkpoint(self, name: str, *, before: str | None = None) -> Checkpoint:
        reason = f"before {before}" if before else "requested"
        with self._in_mode(_UNTRACKED):
            checkpoint = self.store.write(
                self.session, name, reason=reason, journal_seq=self.journal.next_seq
            )
        with self._mirror_lock:
            # The checkpoint brings out-of-sync standbys back in sync.
            for mirror in self._mirrors.values():
                if not mirror.synced:
                    self._catch_up(mirror, checkpoint)
        when = f" before {before}" if before else ""
        self._emit(
            EventKind.CHECKPOINT,
            f"Checkpoint {name!r} written{when}: {checkpoint.path}",
            checkpoint=checkpoint.to_dict(),
        )
        return checkpoint

    def checkpoint(self, name: str) -> Checkpoint:
        """Write a checkpoint called ``name``.

        Raises
        ------
        CheckpointError
            If the session has nothing to checkpoint or the write fails.
        """
        if not self.adapter.can_checkpoint(self.session):
            raise CheckpointError(
                f"The {self.adapter.product_name} session has nothing to checkpoint "
                "yet (for example, no case is loaded)."
            )
        return self._write_checkpoint(name)

    def _restore(self, checkpoint: Checkpoint) -> None:
        with self._in_mode(_UNTRACKED):
            self.store.restore(self.session, checkpoint)
        self.journal.truncate(checkpoint.journal_seq)
        self.store.discard_after(checkpoint)

    def rollback(self, name: str | None = None) -> Checkpoint:
        """Restore the newest checkpoint, or the newest one called ``name``.

        Newer checkpoints and the journal entries recorded after the restored
        checkpoint are discarded.

        Raises
        ------
        CheckpointError
            If no matching checkpoint exists or the restore fails.
        """
        checkpoint = self.store.find(name)
        with self._mirror_lock:
            self._restore(checkpoint)
            for mirror in self._mirrors.values():
                self._catch_up(mirror, checkpoint)
        self._emit(
            EventKind.ROLLBACK,
            f"Restored checkpoint {checkpoint.name!r}.",
            checkpoint=checkpoint.to_dict(),
        )
        return checkpoint

    def _display_path(self, path: str) -> str:
        """Return ``path`` without the session and settings-root prefixes."""
        text = path.removeprefix("<session>.")
        for prefix in self.adapter.path_prefixes:
            if text.startswith(prefix):
                return text[len(prefix) :]
        return text

    def undo(self) -> SetOp:
        """Undo the most recent value write.

        Raises
        ------
        ResilientError
            If the most recent operation cannot be undone.
        """
        with self._mirror_lock:
            with self._in_mode(_UNTRACKED):
                op = self.journal.undo(self._inner.set_var)
            self._mirror_value(op.path, op.old_value, f"undo of {op.describe()}")
        self._emit(
            EventKind.UNDO,
            f"Undid {self._display_path(op.path)} = {op.new_value!r}; restored "
            f"{op.old_value!r}.",
            path=op.path,
        )
        return op

    def redo(self) -> SetOp:
        """Re-apply the most recently undone value write.

        Raises
        ------
        ResilientError
            If there is nothing to redo.
        """
        with self._mirror_lock:
            with self._in_mode(_UNTRACKED):
                op = self.journal.redo(self._inner.set_var)
            self._mirror_value(op.path, op.new_value, f"redo of {op.describe()}")
        self._emit(
            EventKind.REDO,
            f"Redid {self._display_path(op.path)} = {op.new_value!r}.",
            path=op.path,
        )
        return op

    # -- disabling ------------------------------------------------------------------

    def disable(self) -> None:
        """Stop intercepting settings calls and exit the standby sessions."""
        if not self.enabled:
            return
        self.enabled = False
        inner = self._inner
        for session in self._bound_sessions:
            try:
                if self.adapter.settings_service(session) is self.proxy:
                    self.adapter.set_settings_service(session, inner)
                    self.adapter.invalidate_settings_cache(session)
                if session.__dict__.get("resilient") is self.api:
                    del session.__dict__["resilient"]
            except Exception as err:  # noqa: BLE001
                logger.debug("Could not unbind a session: %s", err)
        self._bound_sessions.clear()
        self._close_mirrors()
        if self.pool is not None:
            self.pool.shutdown(keep=self.session)
