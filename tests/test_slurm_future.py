# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

from concurrent.futures import Future

import pytest

from ansys.fluent.core.launcher.slurm_launcher import SlurmFuture


class SlurmEnvironment:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state


class SlurmFutureResult:
    pass


class SlurmFutureException:
    pass


@pytest.fixture
def slurm_future(monkeypatch: pytest.MonkeyPatch) -> SlurmFuture:
    env = SlurmEnvironment()
    future = Future()
    future.set_running_or_notify_cancel()
    slurm_future = SlurmFuture(future, 0)
    monkeypatch.setattr(slurm_future, "_get_state", lambda: env.state)
    monkeypatch.setattr(slurm_future, "_cancel", lambda: env.set_state(""))
    env.set_state("RUNNING")
    slurm_future.env = env
    return slurm_future


def test_cancel_slurm_future(slurm_future: SlurmFuture):
    assert slurm_future.cancel()


def test_slurm_future_lifecycle(slurm_future: SlurmFuture):
    assert slurm_future.pending()
    assert not slurm_future.running()
    assert not slurm_future.done()
    slurm_future._future.set_result(SlurmFutureResult())
    assert not slurm_future.pending()
    assert slurm_future.running()
    assert not slurm_future.done()
    assert isinstance(slurm_future.result(), SlurmFutureResult)
    slurm_future.env.set_state("")
    assert not slurm_future.pending()
    assert not slurm_future.running()
    assert slurm_future.done()


def test_slurm_future_exception(slurm_future: SlurmFuture):
    slurm_future._future.set_exception(SlurmFutureException())
    assert isinstance(slurm_future.exception(), SlurmFutureException)


def test_slurm_future_done_callback(slurm_future: SlurmFuture):
    called = []
    slurm_future.add_done_callback(lambda session: called.append(True))
    assert not called
    slurm_future._future.set_result(SlurmFutureResult())
    assert called
    assert called[0]
