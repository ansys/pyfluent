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

"""Unit tests for the ansys.framework platform contracts (no Fluent needed)."""

import os
import subprocess
import sys

import pytest

from ansys.framework.process import (
    BaseLauncher,
    Endpoint,
    FileUpdatedProbe,
    ProcessExitedError,
    ProcessHandle,
    ProcessLauncher,
    ReadinessProbe,
    background_process_kwargs,
    child_environment,
    detached_process_kwargs,
    pid_exists,
    run_cleanup_script,
    slurm,
    wait_until_ready,
)
from ansys.framework.process.container import run_docker_container
from ansys.framework.process.slurm import SlurmScheduler, read_job_id
from ansys.framework.services import NotSupported, ServiceRegistry
from ansys.framework.transport import ErrorState, Transport


def test_service_registry_lazy_resolution_and_caching():
    calls = []

    def build_settings():
        calls.append("settings")
        return object()

    registry = ServiceRegistry()
    registry.register("settings", build_settings)

    assert registry.has("settings")
    assert not registry.has("field_data")
    assert calls == []  # not built until requested

    first = registry.get("settings")
    second = registry.get("settings")
    assert first is second  # cached
    assert calls == ["settings"]  # factory called exactly once


def test_service_registry_missing_capability_raises_not_supported():
    registry = ServiceRegistry()
    with pytest.raises(NotSupported) as exc_info:
        registry.get("field_data")
    assert exc_info.value.capability == "field_data"


def test_service_registry_capabilities_set():
    registry = ServiceRegistry()
    registry.register("settings", lambda: 1)
    registry.register("field_data", lambda: 2)
    assert registry.capabilities() == frozenset({"settings", "field_data"})


def test_transport_protocol_is_runtime_checkable():
    class _ErrorState:
        name = ""
        details = ""

        def set(self, name, details):
            pass

        def clear(self):
            pass

    class _Transport:
        metadata = [("password", "secret")]
        error_state = _ErrorState()
        is_serving = True

        def connect(self):
            pass

        def close(self):
            pass

    transport = _Transport()
    assert isinstance(transport.error_state, ErrorState)
    assert isinstance(transport, Transport)
    assert not isinstance(object(), Transport)


class _FakeHandle:
    pid = 1234
    container_id = None
    endpoint = Endpoint(host="localhost", port=50051, password="secret")

    def __init__(self, alive=True):
        self.alive = alive
        self.terminated = False

    def is_alive(self):
        return self.alive

    def wait(self, timeout=None):
        return not self.alive

    def terminate(self):
        self.terminated = True
        self.alive = False

    def cleanup(self):
        pass


def test_process_protocols_are_runtime_checkable():
    class _Launcher:
        def launch(self):
            return _FakeHandle()

    handle = _Launcher().launch()
    assert isinstance(_Launcher(), ProcessLauncher)
    assert isinstance(handle, ProcessHandle)
    assert isinstance(lambda h: True, ReadinessProbe)
    assert not isinstance(object(), ProcessHandle)


def test_base_launcher_requires_call_and_fills_defaults():
    with pytest.raises(TypeError):
        BaseLauncher()

    class _Launcher(BaseLauncher):
        def __init__(self, **argvals):
            self.argvals = argvals

        def __call__(self):
            return self.argvals

    launcher = _Launcher(start_timeout=None, cleanup_on_exit=False)
    launcher._set_default_argvals(
        start_timeout=100, cleanup_on_exit=True, start_transcript=True
    )
    assert launcher() == {
        "start_timeout": 100,
        "cleanup_on_exit": False,
        "start_transcript": True,
    }


def test_endpoint_repr_hides_password():
    endpoint = Endpoint(host="localhost", port=50051, password="secret")
    assert "secret" not in repr(endpoint)
    assert endpoint.password == "secret"


def test_wait_until_ready_returns_once_probe_passes():
    checks = iter([False, False, True])
    wait_until_ready(_FakeHandle(), lambda h: next(checks), timeout=5, interval=0)


def test_wait_until_ready_times_out():
    with pytest.raises(TimeoutError):
        wait_until_ready(_FakeHandle(), lambda h: False, timeout=0.05, interval=0.01)


def test_wait_until_ready_fails_fast_when_process_exits():
    with pytest.raises(ProcessExitedError):
        wait_until_ready(
            _FakeHandle(alive=False), lambda h: False, timeout=5, interval=0
        )


def test_process_layer_imports_without_grpc():
    code = (
        "import sys; sys.modules['grpc'] = None; sys.modules['ansys.api'] = None; "
        "import ansys.framework.process, ansys.framework.process.slurm, "
        "ansys.framework.process.container; "
        "assert 'ansys.fluent.core' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_file_updated_probe(tmp_path):
    server_info = tmp_path / "server_info.txt"
    server_info.write_text("")
    last_mtime = server_info.stat().st_mtime
    probe = FileUpdatedProbe(server_info, last_mtime)
    assert isinstance(probe, ReadinessProbe)
    assert not probe()
    os.utime(server_info, (last_mtime + 10, last_mtime + 10))
    assert probe()


@pytest.mark.skipif(
    sys.platform not in ("win32", "linux"), reason="pid_exists supports Linux/Windows"
)
def test_pid_exists():
    assert pid_exists(os.getpid())
    if sys.platform == "linux":
        process = subprocess.Popen([sys.executable, "-c", "pass"])
        process.wait()
        assert not pid_exists(process.pid)


def test_detached_process_kwargs():
    kwargs = detached_process_kwargs()
    if os.name == "nt":
        assert kwargs["creationflags"] & subprocess.DETACHED_PROCESS
    else:
        assert kwargs == {"start_new_session": True}


def test_run_cleanup_script(tmp_path):
    marker = tmp_path / "cleaned"
    if os.name == "nt":
        script = tmp_path / "cleanup.bat"
        script.write_text(f'@echo off\ntype nul > "{marker}"\n')
        failing = tmp_path / "failing.bat"
        failing.write_text("@echo off\nexit /b 3\n")
    else:
        script = tmp_path / "cleanup.sh"
        script.write_text(f'touch "{marker}"\n')
        failing = tmp_path / "failing.sh"
        failing.write_text("exit 3\n")
    run_cleanup_script(script)
    assert marker.is_file()
    with pytest.raises(subprocess.CalledProcessError):
        run_cleanup_script(failing)


def test_background_process_kwargs():
    kwargs = background_process_kwargs()
    assert kwargs["shell"] is True
    if sys.platform == "win32":
        assert kwargs["creationflags"] & subprocess.CREATE_NO_WINDOW
    else:
        assert kwargs["start_new_session"] is True


def test_child_environment(monkeypatch):
    monkeypatch.setenv("FRAMEWORK_TEST_VAR", "inherited")
    env = child_environment({"FRAMEWORK_TEST_NUM": 4})
    assert env["FRAMEWORK_TEST_VAR"] == "inherited"
    assert env["FRAMEWORK_TEST_NUM"] == "4"
    assert "FRAMEWORK_TEST_NUM" not in os.environ


def test_slurm_read_job_id():
    assert read_job_id([b"queued\n", b"Submitted batch job 4321\n", b"x\n"]) == 4321
    assert read_job_id([b"error\n"]) is None


def test_slurm_scheduler_commands(monkeypatch):
    calls = []

    def check_output(cmd):
        calls.append(cmd)
        return b"debug* long\n" if cmd[0] == "sinfo" else b'"RUNNING"\n'

    monkeypatch.setattr(slurm.subprocess, "check_output", check_output)
    monkeypatch.setattr(slurm.subprocess, "run", lambda cmd: calls.append(cmd))
    monkeypatch.setattr(slurm.shutil, "which", lambda name: "/usr/bin/sinfo")

    assert SlurmScheduler.list_queues() == ["debug", "long"]
    assert SlurmScheduler.is_available()
    assert SlurmScheduler.get_state(7) == "RUNNING"
    SlurmScheduler.cancel(7)
    assert calls[-1] == ["scancel", "7"]


class _FakeContainer:
    def __init__(self, stop_error=None):
        self.stopped = False
        self.stop_error = stop_error

    def stop(self):
        if self.stop_error:
            raise self.stop_error
        self.stopped = True


@pytest.fixture
def fake_docker(monkeypatch):
    runs = []
    state = {"container": _FakeContainer()}

    class _Containers:
        def run(self, image, **kwargs):
            runs.append((image, kwargs))
            return state["container"]

    class _Client:
        containers = _Containers()

    module = type(sys)("docker")
    module.from_env = lambda: _Client()
    monkeypatch.setitem(sys.modules, "docker", module)
    return runs, state


def test_run_docker_container_returns_ready_container(fake_docker):
    runs, state = fake_docker
    checks = iter([False, True])
    container = run_docker_container(
        "image:tag", {"detach": True}, lambda: next(checks), timeout=5, interval=0
    )
    assert container is state["container"]
    assert runs == [("image:tag", {"detach": True})]


def test_run_docker_container_stops_container_on_timeout(fake_docker):
    _, state = fake_docker
    with pytest.raises(TimeoutError, match="Solver container launch has timed out"):
        run_docker_container(
            "image", {}, lambda: False, timeout=0.05, description="Solver container"
        )
    assert state["container"].stopped

    state["container"] = _FakeContainer(stop_error=RuntimeError("gone"))
    with pytest.raises(TimeoutError, match="stopping the container failed: gone"):
        run_docker_container("image", {}, lambda: False, timeout=0.05, interval=0.01)
