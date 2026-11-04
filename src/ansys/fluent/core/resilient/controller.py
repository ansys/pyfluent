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

"""The resilience controller behind transparent resilient mode.

:class:`ResilientController` holds all resilient state for a single session --
the checkpoint manager, the optional warm pool, the error classifier and the
recoverable-error resolver -- and implements the per-write / per-command envelope
that :class:`~ansys.fluent.core.resilient.interceptor.ResilientSettingsService`
calls into. It operates on the **string path** supplied by the service layer and
resolves live settings objects only when it needs to introspect them for a repair.

The controller is also what the session-level convenience methods
(``checkpoint`` / ``undo`` / ``redo`` / ``rewind_to``) delegate to.
"""

from __future__ import annotations

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.checkpoint import CheckpointManager
from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError
from ansys.fluent.core.resilient.journal import CommandOp, Journal, SetOp
from ansys.fluent.core.resilient.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.types import CheckpointKind, StepOutcome, UndoEntry


def _brief(value) -> object:
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    if isinstance(value, dict):
        return f"<dict:{len(value)} keys>"
    if isinstance(value, (list, tuple)):
        return f"<{type(value).__name__}:{len(value)}>"
    return repr(value)


#: Solve-type commands that may legitimately raise Fluent's clean-stop sentinel
#: (``RuntimeError("()")``) when interrupted. Only for these is that sentinel
#: treated as a benign interrupt -- matching core PyFluent, so the benign category
#: is applied consistently and never swallows the sentinel elsewhere.
_INTERRUPTIBLE_COMMANDS = frozenset({"iterate", "calculate", "dual_time_iterate"})


def _is_interruptible_command(full_path: str) -> bool:
    """Whether a command path is an interruptible (solve) command."""
    leaf = full_path.strip().rstrip(")").split("(")[0].split(".")[-1]
    return leaf in _INTERRUPTIBLE_COMMANDS


class ResilientController:
    """Owns resilient state and the apply envelope for one session."""

    def __init__(self, session, config, *, pool=None):
        self.session = session
        self.config = config
        self.auto_file_checkpoint = config.auto_file_checkpoint_before_irreversible
        self.auto_rollback = getattr(config, "auto_rollback_on_failed_command", True)
        self._pool = pool
        self._classifier = ErrorClassifier()
        self._resolver = RecoverableErrorResolver(
            session, max_attempts=config.max_resolver_attempts
        )
        self._checkpoints = CheckpointManager(
            session, file_config=config.file_checkpoint
        )
        #: Operation journal: the replayable timeline of successful set / command
        #: operations, using get_state values as undo points.
        self._journal = Journal(restore=self._restore_value)
        #: The checkpoint taken immediately before the current irreversible
        #: command, used for automatic rollback if that command fails.
        self._pending_rollback_entry = None

    def _restore_value(self, path: str, value) -> None:
        """Write ``value`` back to the live tree at ``path`` (journal undo/redo)."""
        try:
            service = self._settings_service()
            if service is not None:
                service.set_var(path, value)
        except Exception:  # noqa: BLE001  # nosec B110
            # Best-effort: an undo/redo restore must never raise.
            pass

    def _settings_service(self):
        """The live (inner) settings service, or None."""
        wrapped = getattr(self.session, "_settings_service", None)
        return getattr(wrapped, "inner", wrapped)

    # -- accessors --------------------------------------------------------

    @property
    def checkpoints(self) -> CheckpointManager:
        """The checkpoint manager (undo / redo stacks)."""
        return self._checkpoints

    @property
    def journal(self) -> Journal:
        """The operation journal (replayable timeline with undo / redo)."""
        return self._journal

    def on_journal_event(self, listener) -> None:
        """Register a ``(event_name, op)`` journal listener (record / undo / redo)."""
        self._journal.on_event(listener)

    @property
    def pool(self):
        """The warm session pool, or ``None`` when resilience wraps a single session."""
        return self._pool

    def _rebind(self, session) -> None:
        """Point the controller (and its helpers) at a new session after failover."""
        self.session = session
        self._resolver.session = session
        self._checkpoints.rebind(session)

    # -- intercepted writes ----------------------------------------------

    def apply_set(self, service, path: str, value) -> StepOutcome:
        """Apply ``service.set_var(path, value)`` with recovery and failover."""
        try:
            return self._set_once(service, path, value)
        except Exception as err:  # noqa: BLE001
            return self._maybe_failover(
                err, lambda svc: self._set_once(svc, path, value), path
            )

    def _set_once(self, service, path: str, value) -> StepOutcome:
        # Read the current value first: this is the undo point (last-good state).
        old_value = self._read_value(service, path)
        try:
            service.set_var(path, value)
        except Exception as err:  # noqa: BLE001
            return self._handle_set_failure(service, path, value, old_value, err)
        # Success: record the operation on the journal (silent timeline entry).
        self._journal.record(SetOp(path=path, old_value=old_value, new_value=value))
        return StepOutcome(
            path=path, ok=True, old_value=_brief(old_value), new_value=_brief(value)
        )

    def _read_value(self, service, path: str):
        """Read the current value at ``path`` (the undo point), tolerating failure."""
        try:
            return service.get_var(path)
        except Exception:  # noqa: BLE001
            return None

    def _handle_set_failure(self, service, path, value, old_value, err) -> StepOutcome:
        # A value set is NOT interruptible, so the clean-stop sentinel is never
        # treated as benign here -- it is surfaced as a genuine error (consistent
        # handling; nothing swallowed).
        cls = self._classifier.classify(err, self.session, interruptible=False)
        if cls.catastrophic:
            raise err
        # UNDO: the set was rejected; restore the last-good value we read so the
        # session is explicitly back at the previous successful state.
        self._emit_undo(path, old_value)
        if cls.recoverable:
            return self._resolve_and_retry(service, path, value, old_value, cls)
        raise UnrecoverableStepError(
            f"Could not apply {path!r}: {cls.message}"
        ) from err

    def _emit_undo(self, path: str, old_value) -> None:
        """Restore the pre-step value and notify journal listeners of an undo."""
        try:
            self._restore_value(path, old_value)
        finally:
            # A failed step is recorded + immediately undone so listeners (logs)
            # see the undo of exactly this step, keeping the journal consistent.
            undo_op = SetOp(path=path, old_value=old_value, new_value=old_value)
            self._journal._notify("undo", undo_op)

    def _resolve_and_retry(self, service, path, value, old_value, cls) -> StepOutcome:
        """Fix-and-retry (REDO) against the service, bounded by max attempts."""
        current_value = value
        current_cls = cls
        fixes: list[str] = []
        last_error = current_cls.message
        for attempt in range(1, self.config.max_resolver_attempts + 1):
            fix = self._resolver.propose(path, current_value, current_cls)
            if fix is None:
                break
            fixes.append(fix.kind)
            for pre_path, pre_value in fix.pre_mutations:
                try:
                    # Pre-mutations (e.g. enabling a governing model) use Python
                    # dotted paths, so apply them through the live object, not the
                    # scheme-path service layer.
                    _compat.resolve_any(self.session, pre_path).set_state(pre_value)
                except Exception as pre_err:  # noqa: BLE001
                    last_error = f"pre-mutation {pre_path!r} failed: {pre_err}"
                    break
            if fix.new_value is not None:
                current_value = fix.new_value
            try:
                service.set_var(path, current_value)
            except Exception as retry_err:  # noqa: BLE001
                retry_cls = self._classifier.classify(retry_err, self.session)
                if retry_cls.catastrophic:
                    raise
                current_cls = retry_cls
                last_error = str(retry_err)
                continue
            # REDO succeeded with the repaired value: record it and notify.
            op = SetOp(
                path=path,
                old_value=old_value,
                new_value=current_value,
                fixes=list(fixes),
            )
            self._journal.record(op)
            self._journal._notify("redo", op)
            return StepOutcome(
                path=path,
                ok=True,
                old_value=_brief(old_value),
                new_value=_brief(current_value),
                attempts=attempt + 1,
                fixes_applied=fixes,
            )
        raise UnrecoverableStepError(
            f"Could not resolve error at {path!r} after {len(fixes)} fix "
            f"attempt(s): {last_error}"
        )

    # -- intercepted commands --------------------------------------------

    def apply_command(self, service, path: str, command: str, kwds: dict):
        """Execute a command with benign-stop handling, failover and auto-rollback.

        Raises
        ------
        Exception
            Re-raises a catastrophic error (handled by failover) or, when
            auto-rollback is disabled or no pre-command checkpoint exists, the
            original non-catastrophic command failure.
        """
        full = f"{path}.{command}" if path else command
        try:
            try:
                return self._command_once(service, path, command, kwds)
            except Exception as err:  # noqa: BLE001
                return self._maybe_failover(
                    err,
                    lambda svc: self._command_once(svc, path, command, kwds),
                    full,
                )
        except Exception as err:  # noqa: BLE001
            # Reached only for non-catastrophic, non-recovered failures (failover
            # re-raises catastrophic errors above). If the command was irreversible
            # and we checkpointed just before it, automatically roll back to that
            # last-good state so the user does not have to.
            cls = self._classifier.classify(err, self.session)
            if (
                self.auto_rollback
                and not cls.catastrophic
                and self._pending_rollback_entry is not None
            ):
                entry = self._pending_rollback_entry
                self._pending_rollback_entry = None
                try:
                    self._checkpoints.replay(entry)
                except Exception:  # noqa: BLE001
                    raise err from None
                return (
                    StepOutcome(
                        path=full,
                        ok=False,
                        result="auto-rolled-back",
                        error=str(err),
                    ),
                    None,
                )
            raise
        finally:
            # A successful command consumes its pending rollback point.
            self._pending_rollback_entry = None

    def _command_once(self, service, path: str, command: str, kwds: dict):
        full = f"{path}.{command}" if path else command
        try:
            result = service.execute_cmd(path, command, **kwds)
        except Exception as err:  # noqa: BLE001
            # Only solve-type commands may legitimately raise the clean-stop
            # sentinel; treat the benign interrupt as such exactly there (mirrors
            # core PyFluent), and as a real error everywhere else.
            cls = self._classifier.classify(
                err, self.session, interruptible=_is_interruptible_command(full)
            )
            if cls.severity.value == "benign":
                return StepOutcome(path=full, ok=True, result="interrupted"), None
            if cls.catastrophic:
                raise
            raise UnrecoverableStepError(
                f"Command {full!r} failed: {cls.message}"
            ) from err
        self._record_command(full, command, kwds)
        return StepOutcome(path=full, ok=True, result=_brief(result)), result

    def _record_command(self, full: str, command: str, kwds: dict) -> None:
        """Record a successful command on the journal."""
        from ansys.fluent.core.resilient.checkpoint import is_irreversible

        irreversible = is_irreversible(full)
        self._journal.record(
            CommandOp(
                path=full,
                args=dict(kwds),
                irreversible=irreversible,
                checkpoint_name=(
                    getattr(self._pending_rollback_entry, "name", None)
                    if irreversible
                    else None
                ),
            )
        )

    # -- failover ---------------------------------------------------------

    def _maybe_failover(self, err, retry, path: str):
        cls = self._classifier.classify(err, self.session)
        if not cls.catastrophic or self._pool is None:
            raise err
        standby = self._pool.failover(self._checkpoints)
        self._rebind(standby)
        # Re-point the live service proxy at the standby's settings service.
        new_service = getattr(standby, "_settings_service", None)
        inner = getattr(new_service, "inner", new_service)
        result = retry(inner)
        # apply_command returns a tuple; apply_set returns a StepOutcome.
        if isinstance(result, tuple):
            outcome, _ = result
            outcome.failed_over = True
            return result
        result.failed_over = True
        return result

    # -- checkpoint surface (delegated to by the session methods) --------

    def auto_checkpoint(self, label: str) -> None:
        """Best-effort file checkpoint before an irreversible command.

        Remembers the created entry so the command can be rolled back to it
        automatically if it fails (see :meth:`apply_command`).
        """
        self._pending_rollback_entry = None
        try:
            self._pending_rollback_entry = self._checkpoints.checkpoint_file(
                f"auto:{label}", reason="pre-irreversible"
            )
        except Exception:  # noqa: BLE001  # nosec B110
            # Inability to checkpoint must not block the user's command.
            pass

    def checkpoint(
        self, name: str, *, kind: CheckpointKind | None = None, paths=None
    ) -> UndoEntry:
        """Take an explicit checkpoint (file by default)."""
        if kind is CheckpointKind.SETTINGS:
            return self._checkpoints.checkpoint_settings(name, paths)
        return self._checkpoints.checkpoint_file(name)

    def undo(self) -> UndoEntry:
        """Undo the newest checkpoint."""
        return self._checkpoints.undo()

    def redo(self) -> UndoEntry:
        """Redo the most recently undone checkpoint."""
        return self._checkpoints.redo()

    def rewind_to(self, name: str) -> list[UndoEntry]:
        """Undo repeatedly until the named checkpoint is restored."""
        return self._checkpoints.rewind_to(name)

    def shutdown(self) -> None:
        """Explicit teardown of the pool, if any."""
        if self._pool is not None:
            self._pool.shutdown()

    # Expose resolve for callers/tests that want a live object.
    def resolve(self, path: str):
        """Resolve a dotted path to a live settings object."""
        return _compat.resolve(self.session, path)
