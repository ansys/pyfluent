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

"""Behavior of a resilient session, driven through its settings service."""

import sys

from _resilient_fakes import FakeAdapter, FakeLeaf, FakeSession, service_of
import pytest

from ansys.fluent.core.resilient.engine import (
    CheckpointConfig,
    CheckpointError,
    EventKind,
    FailoverError,
    PoolConfig,
    ResilientConfig,
    ResilientError,
    ResilientFailoverWarning,
    ResilientSession,
    ResilientWarning,
    disable_resilient_mode,
    enable_resilient_mode,
    is_resilient,
)
from ansys.fluent.core.resilient.engine.interceptor import ResilientSettingsService

pytestmark = pytest.mark.resilient


def _enable(session=None, tmp_path=None, adapter=None, **config):
    session = session or FakeSession()
    if tmp_path is not None:
        config.setdefault("checkpoint", CheckpointConfig(directory=tmp_path))
    enable_resilient_mode(
        session,
        ResilientConfig(**config),
        adapter=adapter or FakeAdapter(),
        journal_complete=True,
    )
    events = []
    session.resilient.on_event(events.append)
    return session, events


def _set(session, path, value):
    session._settings_service.set_var(path, value)


# -- enabling and disabling ----------------------------------------------------------


def test_enable_wraps_the_service_and_adds_the_session_api():
    session, _ = _enable()
    assert isinstance(session._settings_service, ResilientSettingsService)
    assert isinstance(session.resilient, ResilientSession)
    assert is_resilient(session)
    assert session.cache_invalidations == 1
    with pytest.raises(ResilientError, match="already enabled"):
        enable_resilient_mode(session, adapter=FakeAdapter())


def test_disable_restores_the_product_service():
    session, _ = _enable()
    disable_resilient_mode(session)
    assert not is_resilient(session)
    assert not isinstance(session._settings_service, ResilientSettingsService)
    assert "resilient" not in vars(session)
    # It can be enabled again.
    enable_resilient_mode(session, adapter=FakeAdapter())
    assert is_resilient(session)


def test_enable_requires_a_settings_service():
    session = FakeSession()
    session._settings_service = None
    with pytest.raises(ResilientError, match="no settings service"):
        enable_resilient_mode(session, adapter=FakeAdapter())


def test_user_config_is_not_modified():
    config = ResilientConfig()
    enable_resilient_mode(FakeSession(), config, adapter=FakeAdapter(), pool_size=1)
    assert config.pool.size == 1


def test_repr_reports_the_session_state():
    session, _ = _enable()
    text = repr(session.resilient)
    assert text.startswith("<ResilientSession")
    assert "enabled=True" in text
    assert "journal=" in text and "checkpoints=" in text


# -- value writes ----------------------------------------------------------------------


def test_accepted_write_is_journaled_with_its_previous_value():
    session, events = _enable()
    _set(session, "setup.intensity", 0.1)
    op = session.resilient.journal.operations[-1]
    assert (op.path, op.old_value, op.new_value) == ("setup.intensity", 0.05, 0.1)
    assert session.resilient.last_outcome.ok
    assert events == []


def test_rejected_value_raises_the_original_error_unchanged():
    # Resilient mode never changes a value to make a rejected write succeed.
    session, events = _enable()

    def reject(value):
        if value > 1.0:
            raise RuntimeError("Value is not in range.")

    session.settings.setup.intensity.reject = reject
    with pytest.raises(RuntimeError, match="not in range"):
        _set(session, "setup.intensity", 1.05)
    assert session.settings.setup.intensity.value == 0.05
    assert events == []
    assert len(session.resilient.journal) == 0


def test_unrepairable_error_propagates_unchanged():
    session, _ = _enable()
    error = KeyError("custom")

    def reject(value):
        raise error

    session.settings.setup.intensity.reject = reject
    with pytest.raises(KeyError) as info:
        _set(session, "setup.intensity", 0.3)
    assert info.value is error
    assert len(session.resilient.journal) == 0


def test_inactive_target_write_raises_the_original_error():
    # An inactive target raises; resilient mode does not activate a model.
    session, _ = _enable()
    session.settings.setup.plain = FakeLeaf(1.0, active=False)
    with pytest.raises(RuntimeError, match="not allowed to be set"):
        _set(session, "setup.plain", 2.0)


# -- commands, checkpoints, rollback -------------------------------------------------


def _with_iterate(session, *, fail=False):
    def iterate(iter_count=1):
        session.settings.setup.intensity.value = 0.9
        if fail:
            raise RuntimeError("Divergence detected in AMG solver")
        return iter_count

    session.settings.commands["iterate"] = iterate


def test_irreversible_command_is_checkpointed_first(tmp_path):
    session, events = _enable(tmp_path=tmp_path)
    _with_iterate(session)
    assert session._settings_service.execute_cmd("", "iterate", iter_count=3) == 3
    checkpoint = session.resilient.checkpoints[-1]
    assert checkpoint.name == "auto-iterate"
    assert [e.kind for e in events] == [EventKind.CHECKPOINT]
    op = session.resilient.journal.operations[-1]
    assert (op.command, op.args, op.checkpoint) == (
        "iterate",
        {"iter_count": 3},
        "auto-iterate",
    )


def test_failed_irreversible_command_is_rolled_back_and_raised(tmp_path):
    session, events = _enable(tmp_path=tmp_path)
    _with_iterate(session, fail=True)
    with pytest.raises(RuntimeError, match="Divergence") as info:
        session._settings_service.execute_cmd("", "iterate")
    assert session.settings.setup.intensity.value == 0.05
    assert session.resilient.last_outcome.rolled_back
    assert [e.kind for e in events] == [EventKind.CHECKPOINT, EventKind.ROLLBACK]
    if sys.version_info >= (3, 11):
        assert "restored checkpoint" in info.value.__notes__[0]


def test_auto_rollback_can_be_disabled(tmp_path):
    session, _ = _enable(tmp_path=tmp_path, auto_rollback=False)
    _with_iterate(session, fail=True)
    with pytest.raises(RuntimeError):
        session._settings_service.execute_cmd("", "iterate")
    assert session.settings.setup.intensity.value == 0.9


def test_no_automatic_checkpoint_without_a_case(tmp_path):
    session, _ = _enable(tmp_path=tmp_path)
    session.has_case = False
    _with_iterate(session)
    session._settings_service.execute_cmd("", "iterate")
    assert session.resilient.checkpoints == []
    with pytest.raises(CheckpointError, match="nothing to checkpoint"):
        session.resilient.checkpoint("manual")


def test_failed_automatic_checkpoint_is_reported_and_the_command_runs(tmp_path):
    class _FullDisk(FakeAdapter):
        def write_checkpoint(self, session, file_path, *, include_data):
            raise OSError("No space left on device")

    session, _ = _enable(tmp_path=tmp_path, adapter=_FullDisk())
    _with_iterate(session)
    with pytest.warns(ResilientWarning, match="cannot be rolled back"):
        assert session._settings_service.execute_cmd("", "iterate", iter_count=2) == 2
    assert session.resilient.checkpoints == []


def test_clean_stop_of_a_solve_command_is_not_an_error(tmp_path):
    session, _ = _enable(tmp_path=tmp_path)

    def iterate(**kwargs):
        raise RuntimeError("()")

    session.settings.commands["iterate"] = iterate
    assert session._settings_service.execute_cmd("", "iterate") is None
    assert session.resilient.last_outcome.result == "interrupted"


def test_rollback_discards_later_checkpoints_and_journal_entries(tmp_path):
    session, _ = _enable(tmp_path=tmp_path)
    session.resilient.checkpoint("base")
    _set(session, "setup.intensity", 0.2)
    session.resilient.checkpoint("later")
    _set(session, "setup.intensity", 0.3)
    restored = session.resilient.rollback("base")
    assert restored.name == "base"
    assert session.settings.setup.intensity.value == 0.05
    assert [c.name for c in session.resilient.checkpoints] == ["base"]
    assert len(session.resilient.journal) == 0


def test_undo_and_redo_of_value_writes():
    session, events = _enable()
    _set(session, "setup.model", "laminar")
    _set(session, "setup.model", "k-omega")
    assert session.resilient.undo().new_value == "k-omega"
    assert session.settings.setup.model.value == "laminar"
    session.resilient.undo()
    assert session.settings.setup.model.value == "k-epsilon"
    session.resilient.redo()
    assert session.settings.setup.model.value == "laminar"
    assert [e.kind for e in events] == [EventKind.UNDO, EventKind.UNDO, EventKind.REDO]


def test_structural_changes_are_journaled():
    session, _ = _enable()
    session._settings_service.create("setup", "new_zone")
    op = session.resilient.journal.operations[-1]
    assert (op.method, op.path, op.args) == ("create", "setup", ("new_zone",))


# -- failover -------------------------------------------------------------------------


def _session_with_iterate(**kwargs):
    session = FakeSession()
    _with_iterate(session)
    return session


def _pool_session(tmp_path, *, size=2, **config):
    adapter = FakeAdapter(factory=_session_with_iterate)
    session, events = _enable(
        session=_session_with_iterate(),
        tmp_path=tmp_path,
        adapter=adapter,
        pool=PoolConfig(size=size),
        **config,
    )
    return session, events, adapter


def test_crash_without_standbys_raises_the_original_error():
    session, _ = _enable()
    session.crash()
    with pytest.raises(ConnectionError, match="Socket closed"):
        _set(session, "setup.intensity", 0.5)


def test_crash_fails_over_and_replays_the_journal(tmp_path):
    session, events, adapter = _pool_session(tmp_path)
    _set(session, "setup.intensity", 0.4)
    _set(session, "setup.model", "laminar")
    session.crash()
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError):
        _set(session, "setup.intensity", 0.6)
    standby = session.resilient.active_session
    assert standby is adapter.launched[0]
    # The standby has the state from before the failed write.
    assert standby.settings.setup.model.value == "laminar"
    assert standby.settings.setup.intensity.value == 0.4
    assert session.resilient.last_outcome.failed_over
    assert not session.resilient.last_outcome.ok
    assert events[-1].kind is EventKind.FAILOVER
    # Both the original and the new session route through the same proxy.
    assert session._settings_service is standby._settings_service
    assert standby.resilient is session.resilient
    # Running the write again applies it on the standby.
    _set(session, "setup.intensity", 0.6)
    assert standby.settings.setup.intensity.value == 0.6


def test_failover_starts_from_the_newest_checkpoint(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    session._settings_service.execute_cmd("", "iterate")
    _set(session, "setup.model", "laminar")
    session.crash()
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError):
        _set(session, "setup.intensity", 0.2)
    standby = session.resilient.active_session
    # Restored from the pre-iterate checkpoint, then iterate (which sets the
    # intensity to 0.9) and the later write were replayed.
    assert standby.settings.file.reads
    assert standby.settings.setup.model.value == "laminar"
    assert standby.settings.setup.intensity.value == 0.9


def test_a_command_that_hit_a_dead_server_is_not_repeated(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    session.crash()
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError) as info:
        session._settings_service.execute_cmd("", "iterate", iter_count=7)
    standby = session.resilient.active_session
    assert standby is adapter.launched[0]
    assert "iterate" not in [call[2] for call in service_of(standby).calls]
    outcome = session.resilient.last_outcome
    assert outcome.failed_over and not outcome.ok
    if sys.version_info >= (3, 11):
        assert "not repeated" in info.value.__notes__[-1]
    # Running the command again runs it on the standby.
    assert session._settings_service.execute_cmd("", "iterate", iter_count=7) == 7


def _crash_on(target, crashed):
    """Mimic a call that makes the server of ``target`` fail."""
    crashed.append(target)
    target.crash()
    raise ConnectionError("failed to connect to all addresses; Socket closed")


def test_a_command_that_crashes_the_server_does_not_crash_the_standby(tmp_path):
    session, events, adapter = _pool_session(tmp_path)
    standby = adapter.launched[0]
    crashed = []
    # The command crashes whichever server runs it.
    for target in (session, standby):
        target.settings.commands["poison"] = lambda target=target: _crash_on(
            target, crashed
        )
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError) as info:
        session._settings_service.execute_cmd("", "poison")
    assert crashed == [session]
    assert session.resilient.active_session is standby
    assert standby.serving
    assert [e.kind for e in events].count(EventKind.FAILOVER) == 1
    if sys.version_info >= (3, 11):
        assert "not repeated" in info.value.__notes__[-1]
    # The standby keeps serving.
    _set(session, "setup.intensity", 0.3)
    assert standby.settings.setup.intensity.value == 0.3


def test_a_write_that_crashes_the_server_does_not_crash_the_standby(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    standby = adapter.launched[0]
    crashed = []
    for target in (session, standby):
        target.settings.setup.intensity.reject = lambda value, target=target: _crash_on(
            target, crashed
        )
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError):
        _set(session, "setup.intensity", 0.7)
    assert crashed == [session]
    assert session.resilient.active_session is standby
    assert standby.serving
    assert standby.settings.setup.intensity.value == 0.05


def test_read_on_a_dead_server_fails_over_and_is_repeated(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    _set(session, "setup.intensity", 0.3)
    session.crash()
    # Navigating the settings tree usually reads attributes before writing.
    with pytest.warns(ResilientFailoverWarning):
        value = session._settings_service.get_var("setup.intensity")
    assert value == 0.3
    assert session.resilient.active_session is adapter.launched[0]


def test_read_errors_of_a_live_server_do_not_fail_over(tmp_path):
    session, _, _ = _pool_session(tmp_path)
    with pytest.raises(LookupError):
        session._settings_service.get_var("setup.missing")
    assert session.resilient.active_session is session


def test_calls_that_saw_the_same_crash_fail_over_once(tmp_path):
    session, events, _ = _pool_session(tmp_path, size=3)
    session.crash()
    with pytest.warns(ResilientFailoverWarning):
        session._settings_service.get_attrs("setup", ["active?"])
    standby = session.resilient.active_session
    # A call that started on the dead session before the failover finished.
    controller = session.resilient._controller
    controller._failover(controller._classifier.classify(ConnectionError()), session)
    assert session.resilient.active_session is standby
    assert [e.kind for e in events].count(EventKind.FAILOVER) == 1


def test_failover_needs_a_checkpoint_when_the_history_is_unknown(tmp_path):
    adapter = FakeAdapter(factory=FakeSession)
    session = FakeSession()
    enable_resilient_mode(
        session,
        ResilientConfig(
            pool=PoolConfig(size=2), checkpoint=CheckpointConfig(directory=tmp_path)
        ),
        adapter=adapter,
    )
    session.crash()
    with pytest.raises(FailoverError, match="checkpoint"):
        _set(session, "setup.intensity", 0.5)


def test_pool_needs_a_way_to_launch_standbys():
    with pytest.raises(ResilientError, match="launch standby"):
        enable_resilient_mode(FakeSession(), adapter=FakeAdapter(), pool_size=2)


def test_pool_launcher_from_config_takes_precedence():
    launched = []

    def launcher():
        launched.append(FakeSession())
        return launched[-1]

    session = FakeSession()
    enable_resilient_mode(
        session,
        ResilientConfig(pool=PoolConfig(size=2, launcher=launcher)),
        adapter=FakeAdapter(),
    )
    assert session.resilient.pool.standbys == launched


def test_exiting_the_session_exits_the_standbys(tmp_path):
    session, _, adapter = _pool_session(tmp_path, size=3)
    session.exit()
    assert all(standby.exited for standby in adapter.launched)


def test_after_failover_exiting_the_original_session_exits_the_pool(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    session.crash()
    with pytest.warns(ResilientFailoverWarning), pytest.raises(ConnectionError):
        _set(session, "setup.intensity", 0.6)
    promoted = session.resilient.active_session
    # The dead original session is left for the user to exit.
    assert not session.exited
    session.exit()
    assert promoted.exited


def test_disable_exits_the_standbys(tmp_path):
    session, _, adapter = _pool_session(tmp_path)
    session.resilient.disable()
    assert adapter.launched[0].exited
    assert not session.exited


def test_listener_errors_do_not_break_the_session():
    session, _ = _enable()

    def broken(event):
        raise ValueError("listener bug")

    session.resilient.on_event(broken)
    session.resilient.checkpoint("manual")
    assert session.resilient.checkpoints[-1].name == "manual"


def test_internal_leaf_without_activity_info():
    session, _ = _enable()
    session.settings.setup.plain = FakeLeaf(1)
    _set(session, "setup.plain", 2)
    assert session.settings.setup.plain.value == 2
