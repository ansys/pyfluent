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

"""Docker container runtime for servers launched in a container.

The ``docker`` package is imported only when a container is started.
"""

from __future__ import annotations

from collections.abc import Callable
import time
from typing import Any


def run_docker_container(
    image: str,
    run_kwargs: dict[str, Any],
    is_ready: Callable[[], bool],
    timeout: float,
    description: str = "Container",
    interval: float = 0.2,
) -> Any:
    """Start a detached Docker container and wait until it is ready.

    Parameters
    ----------
    image : str
        Image reference.
    run_kwargs : dict
        Keyword arguments for ``docker.containers.run``.
    is_ready : Callable[[], bool]
        Readiness check, polled until it returns ``True``.
    timeout : float
        Maximum time to wait, in seconds.
    description : str, optional
        Name used in timeout messages. The default is ``"Container"``.
    interval : float, optional
        Delay between readiness checks, in seconds. The default is ``0.2``.

    Returns
    -------
    docker.models.containers.Container
        The running container.

    Raises
    ------
    TimeoutError
        If the container is not ready in time. The container is stopped first.
    """
    import docker

    container = docker.from_env().containers.run(image, **run_kwargs)

    deadline = time.monotonic() + timeout
    while not is_ready():
        if time.monotonic() >= deadline:
            break
        time.sleep(interval)
    else:
        return container

    try:
        container.stop()
    except Exception as stop_ex:
        raise TimeoutError(
            f"{description} launch has timed out after {timeout} seconds. "
            f"Additionally, stopping the container failed: {stop_ex}"
        ) from stop_ex
    raise TimeoutError(
        f"{description} launch has timed out after {timeout} seconds."
        " The container was stopped."
    )
