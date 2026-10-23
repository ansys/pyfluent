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

"""End-to-end facade tests using fakes (no live Fluent)."""

import pytest

from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.pool import PoolConfig, WarmSessionPool
from ansys.fluent.core.resilient.solver import ResilientConfig, ResilientSolver
from ansys.fluent.core.resilient.types import CheckpointKind
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def _elbow_session():
    def reject_high_ti(value):
        if isinstance(value, (int, float)) and value > 1.0:
            raise RuntimeError("value is above maximum 1.0")

    settings = FakeSettings(
        file_group=FakeFileGroup(),
        setup=FakeGroup(
            models=FakeGroup(energy=FakeGroup(enabled=FakeLeaf(False))),
            turbulence=FakeGroup(
                intensity=FakeLeaf(
                    0.05, minimum=0.0, maximum=1.0, set_raises=reject_high_ti
                )
            ),
        ),
        solution=FakeGroup(
            run_calculation=FakeGroup(
                iterate=_IterateCommand(),
            ),
        ),
    )
    return FakeSession(settings=settings)


class _IterateCommand:
    def __init__(self):
        self.iterations = 0

    def __call__(self, iter_count=0, **kwargs):
        self.iterations += iter_count
        return {"iterated": iter_count}


def _rsolver(session, tmp_path, pool_size=1, launcher=None):
    config = ResilientConfig(
        pool=PoolConfig(size=pool_size),
        file_checkpoint=FileCheckpointConfig(directory=str(tmp_path)),
    )
    pool = WarmSessionPool(
        config.pool,
        seed_session=session,
        launcher=launcher or (lambda _k: _elbow_session()),
    )
    return ResilientSolver(config=config, _pool=pool)


def test_set_and_auto_recover(tmp_path):
    session = _elbow_session()
    with _rsolver(session, tmp_path) as rsolver:
        rsolver.set("setup.models.energy.enabled", True)
        assert session.settings.setup.models.energy.enabled.get_state() is True
        # Out-of-range turbulence intensity is auto-clamped.
        out = rsolver.set("setup.turbulence.intensity", 5.0)
        assert out.ok and out.fixes_applied
        assert session.settings.setup.turbulence.intensity.get_state() == 1.0


def test_auto_file_checkpoint_before_iterate(tmp_path):
    session = _elbow_session()
    with _rsolver(session, tmp_path) as rsolver:
        rsolver.command("solution.run_calculation.iterate", iter_count=10)
        # An automatic file checkpoint was written before the irreversible op.
        assert any(c[0] == "write_case_data" for c in session.settings.file.calls)
        assert session.settings.solution.run_calculation.iterate.iterations == 10


def test_explicit_checkpoint_and_undo(tmp_path):
    session = _elbow_session()
    with _rsolver(session, tmp_path) as rsolver:
        rsolver.checkpoint(
            "pre", kind=CheckpointKind.SETTINGS, paths=["setup.models.energy.enabled"]
        )
        rsolver.set("setup.models.energy.enabled", True)
        assert session.settings.setup.models.energy.enabled.get_state() is True
        rsolver.undo()
        assert session.settings.setup.models.energy.enabled.get_state() is False


def test_failover_on_catastrophic_set(tmp_path):
    standby = _elbow_session()

    def launcher(_kwargs):
        return standby

    session = _elbow_session()
    with _rsolver(session, tmp_path, pool_size=2, launcher=launcher) as rsolver:
        rsolver.checkpoint("base")  # file checkpoint = replay base
        # Rig the active session's leaf to go fatal on set.
        leaf = session.settings.setup.models.energy.enabled

        def die(value):
            session.go_fatal("crash during set")
            raise RuntimeError("fatal: solver crashed")

        leaf._set_raises = die
        out = rsolver.set("setup.models.energy.enabled", True)
        assert out.failed_over
        # Active is now the standby, which applied the value successfully.
        assert rsolver.session is standby
