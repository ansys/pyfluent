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
