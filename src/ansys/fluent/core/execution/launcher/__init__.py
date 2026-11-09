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

"""Launch and connect to Ansys Fluent.

This package provides launch configuration for local Fluent processes, Fluent
containers, and remote Fluent instances. It also includes launch-mode options,
container setup helpers, remote launch support, executable discovery, and the
Fluent version information used by launchers.

Each launcher runs the same stages, which belong to different layers:

* **Process**: spawn Fluent (subprocess, container, PIM instance or Slurm job),
  wait for the server-info file, start the watchdog and clean up on exit.
  Generic parts live in ``launcher_utils``, ``fluent_container``, ``watchdog``
  and the Slurm wrappers; Fluent-specific parts are the command line
  (``process_launch_string``), environment and image selection.
* **Transport**: resolve the endpoint and credentials (``server_info``,
  ``get_remote_grpc_options``) and open a ``FluentConnection``.
* **Session**: pick the session class for the launch mode (``FluentMode``) and
  build it (``launch_fluent``, ``connect_to_fluent``).
"""

from ...utils.fluent_version import FluentVersion  # noqa: F401
from .fluent_container import (  # noqa: F401
    configure_container_dict,
    start_fluent_container,
)
from .launch_options import LaunchMode  # noqa: F401
from .launcher import create_launcher  # noqa: F401
from .pim_launcher import launch_remote_fluent  # noqa: F401
from .process_launch_string import get_fluent_exe_path  # noqa: F401

__all__ = [
    "FluentVersion",
    "configure_container_dict",
    "start_fluent_container",
    "LaunchMode",
    "create_launcher",
    "launch_remote_fluent",
    "get_fluent_exe_path",
]
