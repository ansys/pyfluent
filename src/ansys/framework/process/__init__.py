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

"""Backend-neutral process-controller contract for the platform layer.

A :class:`ProcessLauncher` starts a solver server (local subprocess, container,
remote instance, scheduler job, ...) and returns a :class:`ProcessHandle`. The
handle exposes what is needed to reach the server (:class:`Endpoint`) and to
monitor and stop it, without opening a connection. A :class:`ReadinessProbe`
decides when the server is ready to accept connections; probes are supplied by
the caller (for example by a transport), so this module needs only the standard
library. It also holds generic helpers shared by launchers: a file-based
readiness probe, process liveness, background and detached spawning, child
environments and cleanup scripts. Backend-specific runtimes live in the
:mod:`.slurm` and :mod:`.container` submodules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Endpoint:
    """Where and how to reach a launched server.

    Attributes
    ----------
    host : str, optional
        Host name or IP address.
    port : int, optional
        Port number.
    address : str, optional
        Full address, either ``host:port`` or a Unix domain socket path. Takes
        precedence over ``host`` and ``port`` when set.
    password : str, optional
        Authentication secret required by the server.
    """

    host: str | None = None
    port: int | None = None
    address: str | None = None
    password: str | None = None

    def __repr__(self) -> str:
        """Represent the endpoint without revealing the password."""
        password = "***" if self.password else None
        return (
            f"Endpoint(host={self.host!r}, port={self.port!r}, "
            f"address={self.address!r}, password={password!r})"
        )


class ProcessExitedError(RuntimeError):
    """Raised when a launched process exits before it becomes ready."""


@runtime_checkable
class ProcessHandle(Protocol):
    """A launched solver server process.

    Identifiers that do not apply to a backend (for example ``pid`` for a remote
    instance) are ``None``.
    """

    @property
    def pid(self) -> int | None:
        """Process ID of the server, if it runs as a local process."""
        ...

    @property
    def container_id(self) -> str | None:
        """Container ID of the server, if it runs in a container."""
        ...

    @property
    def endpoint(self) -> Endpoint | None:
        """Connection endpoint, or ``None`` until the server has published it."""
        ...

    def is_alive(self) -> bool:
        """Whether the server process is still running."""
        ...

    def wait(self, timeout: float | None = None) -> bool:
        """Wait for the process to finish; return whether it finished in time."""
        ...

    def terminate(self) -> None:
        """Stop the process immediately, without a graceful shutdown."""
        ...

    def cleanup(self) -> None:
        """Release launch resources (temporary files, containers, jobs)."""
        ...


@runtime_checkable
class ReadinessProbe(Protocol):
    """Decides whether a launched server is ready to accept connections."""

    def __call__(self, handle: ProcessHandle) -> bool:
        """Return ``True`` once the server is ready."""
        ...


@runtime_checkable
class ProcessLauncher(Protocol):
    """Starts a solver server process."""

    def launch(self) -> ProcessHandle:
        """Start the server and return a handle to it without waiting for readiness."""
        ...


class LocalProcess:
    """:class:`ProcessHandle` for a server running as a local subprocess.

    Parameters
    ----------
    process : subprocess.Popen
        The server process.
    endpoint : Endpoint, optional
        Connection endpoint, if known at launch.
    cleanup_paths : iterable of str or os.PathLike, optional
        Files removed by :meth:`cleanup`.
    """

    container_id: str | None = None

    def __init__(
        self,
        process: subprocess.Popen,
        endpoint: Endpoint | None = None,
        cleanup_paths: Iterable[str | os.PathLike] = (),
    ) -> None:
        """Initialize the handle."""
        self.process = process
        self._endpoint = endpoint
        self._cleanup_paths = [Path(path) for path in cleanup_paths]

    @property
    def pid(self) -> int:
        """Process ID."""
        return self.process.pid

    @property
    def endpoint(self) -> Endpoint | None:
        """Connection endpoint, or ``None`` if not known."""
        return self._endpoint

    def is_alive(self) -> bool:
        """Whether the process is still running."""
        return self.process.poll() is None

    def wait(self, timeout: float | None = None) -> bool:
        """Wait for the process to finish; return whether it finished in time."""
        try:
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return False
        return True

    def terminate(self, grace_period: float = 5) -> None:
        """Stop the process, killing it if it is still running after ``grace_period`` seconds."""
        if not self.is_alive():
            return
        self.process.terminate()
        if not self.wait(grace_period):
            self.process.kill()
            self.process.wait()

    def cleanup(self) -> None:
        """Remove the cleanup files."""
        for path in self._cleanup_paths:
            path.unlink(missing_ok=True)


class SubprocessLauncher:
    """:class:`ProcessLauncher` that runs a command as a local subprocess.

    Parameters
    ----------
    args : str or sequence of str
        Command to run.
    endpoint : Endpoint, optional
        Connection endpoint of the server, if known in advance.
    cleanup_paths : iterable of str or os.PathLike, optional
        Files removed by the handle's ``cleanup()``.
    **popen_kwargs
        Keyword arguments for ``subprocess.Popen``.
    """

    def __init__(
        self,
        args: str | Sequence[str],
        endpoint: Endpoint | None = None,
        cleanup_paths: Iterable[str | os.PathLike] = (),
        **popen_kwargs: Any,
    ) -> None:
        """Initialize the launcher."""
        self.args = args
        self.endpoint = endpoint
        self.cleanup_paths = list(cleanup_paths)
        self.popen_kwargs = popen_kwargs

    def launch(self) -> LocalProcess:
        """Start the command and return a handle to it."""
        return LocalProcess(
            subprocess.Popen(self.args, **self.popen_kwargs),
            endpoint=self.endpoint,
            cleanup_paths=self.cleanup_paths,
        )


class BaseLauncher(ABC):
    """Base class for solver launchers.

    A launcher resolves its launch arguments into :attr:`argvals` when it is
    created and starts the server when it is called.

    Attributes
    ----------
    argvals : dict
        Resolved launch arguments.
    """

    argvals: dict[str, Any]

    def _set_default_argvals(self, **defaults: Any) -> None:
        """Fill launch arguments that are missing or ``None`` with defaults."""
        for name, value in defaults.items():
            if self.argvals.get(name) is None:
                self.argvals[name] = value

    @abstractmethod
    def __call__(self) -> Any:
        """Launch the server.

        Returns the connected session, or the launch details for a dry run.
        """


def wait_until_ready(
    handle: ProcessHandle,
    probe: ReadinessProbe,
    timeout: float,
    interval: float = 1.0,
) -> None:
    """Poll ``probe`` until the server is ready.

    Parameters
    ----------
    handle : ProcessHandle
        The launched process.
    probe : ReadinessProbe
        Readiness check, called with ``handle``.
    timeout : float
        Maximum time to wait, in seconds.
    interval : float, optional
        Delay between checks, in seconds. The default is ``1.0``.

    Raises
    ------
    ProcessExitedError
        If the process exits before it becomes ready.
    TimeoutError
        If the server is not ready within ``timeout`` seconds.
    """
    deadline = time.monotonic() + timeout
    while True:
        if probe(handle):
            return
        if not handle.is_alive():
            raise ProcessExitedError("The process exited before it became ready.")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"The process was not ready within {timeout} seconds.")
        time.sleep(interval)


class FileUpdatedProbe:
    """Readiness probe that passes once a file is modified after a reference time.

    Servers that publish their endpoint by rewriting a file (for example a
    server-info file) are ready once that file's modification time advances.

    Parameters
    ----------
    path : str or os.PathLike
        File the server writes when it is ready.
    last_mtime : float
        Modification time of the file before launch.
    """

    def __init__(self, path: str | os.PathLike, last_mtime: float) -> None:
        """Initialize the probe."""
        self.path = Path(path)
        self.last_mtime = last_mtime

    def __call__(self, handle: ProcessHandle | None = None) -> bool:
        """Return whether the file has been modified since ``last_mtime``."""
        return self.path.stat().st_mtime > self.last_mtime


def pid_exists(pid: int) -> bool:
    """Return whether a local process with the given ID is running.

    Only Linux and Windows are supported; other platforms return ``False``.
    """
    system = platform.system()
    if system == "Linux":
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True
    if system == "Windows":
        import ctypes

        process_query_limited_information = 0x1000
        process_handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information, 0, pid
        )
        if process_handle == 0:
            return False
        ctypes.windll.kernel32.CloseHandle(process_handle)
        return True
    return False


def background_process_kwargs() -> dict[str, Any]:
    """Return ``subprocess.Popen`` options that run a shell command in the background.

    The child gets its own process group (Windows) or session (POSIX), so it is
    not interrupted by signals sent to this process, and no console window.
    """
    if platform.system() == "Windows":
        return {
            "shell": True,
            "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW,
        }
    return {"shell": True, "start_new_session": True}


def child_environment(env: dict[str, Any] | None = None) -> dict[str, str]:
    """Return a copy of the current environment updated with ``env``.

    Values in ``env`` are converted to strings.
    """
    child_env = os.environ.copy()
    if env:
        child_env.update({k: str(v) for k, v in env.items()})
    return child_env


def detached_process_kwargs() -> dict[str, Any]:
    """Return ``subprocess.Popen`` options that detach a child from this process.

    The child survives the parent and gets no console window or terminal
    signals from it.
    """
    if os.name == "nt":
        flags = (
            subprocess.CREATE_NO_WINDOW
            | subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS
            | subprocess.CREATE_BREAKAWAY_FROM_JOB
            | subprocess.SW_HIDE
        )
        return {"shell": True, "creationflags": flags}
    return {"start_new_session": True}


def run_cleanup_script(script: str | os.PathLike, timeout: float = 120) -> None:
    """Run a server-written cleanup script that kills its processes.

    ``.sh`` scripts run through ``bash``; other scripts run directly.

    Raises
    ------
    subprocess.CalledProcessError
        If the script exits with a non-zero status.
    subprocess.TimeoutExpired
        If the script does not finish within ``timeout`` seconds.
    """
    script = Path(script)
    cmd = ["bash", script] if script.suffix == ".sh" else [script]
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=timeout,
        check=True,
    )


def app_data_root() -> Path:
    """Return the per-user application data directory for this platform."""
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    if sys.platform.startswith(("linux", "freebsd", "openbsd")):
        return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return Path.home() / ".config"
