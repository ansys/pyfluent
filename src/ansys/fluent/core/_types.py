# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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


"""Common type aliases for PyFluent.

This module centralizes reusable typing constructs
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypedDict

if TYPE_CHECKING:
    from ansys.fluent.core.launcher.launch_options import (
        Dimension,
        FluentLinuxGraphicsDriver,
        FluentWindowsGraphicsDriver,
        Precision,
        UIMode,
    )
    from ansys.fluent.core.utils.fluent_version import FluentVersion

PathType: TypeAlias = "os.PathLike[str] | str"
"""Type alias for file system paths."""


class LauncherArgsBase(TypedDict, total=False):
    """Common launcher arguments shared across launch modes."""

    ui_mode: "UIMode | str | None"
    """Defines the user interface mode for Fluent. Accepts either a ``UIMode`` value
    or a corresponding string such as ``"no_gui"``, ``"hidden_gui"``, or ``"gui"``.
    """
    graphics_driver: (
        "FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None"
    )
    """Graphics driver of Fluent. In Windows, options are either the values of the
    ``FluentWindowsGraphicsDriver`` enum or any of ``"null"``, ``"msw"``,
    ``"dx11"``, ``"opengl2"``, ``"opengl"`` or ``"auto"``. In Linux, options are
    either the values of the ``FluentLinuxGraphicsDriver`` enum or any of
    ``"null"``, ``"x11"``, ``"opengl2"``, ``"opengl"`` or ``"auto"``. The default is
    ``FluentWindowsGraphicsDriver.AUTO`` in Windows and
    ``FluentLinuxGraphicsDriver.AUTO`` in Linux.
    """
    product_version: "FluentVersion | str | float | int | None"
    """Version of Ansys Fluent to launch. To use Fluent version 2025 R1, pass
    any of  ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``or ``251``.
    The default is ``None``, in which case the newest installed version is used.
    PyFluent uses the ``AWP_ROOT<ver>`` environment variable to locate the Fluent
    installation, where ``<ver>`` is the Ansys release number such as ``251``.
    The ``AWP_ROOT<ver>`` environment variable is automatically configured on Windows
    system when Fluent is installed. On Linux systems, ``AWP_ROOT<ver>`` must be
    configured to point to the absolute path of an Ansys installation such as
    ``/apps/ansys_inc/v251``.
    """
    dimension: "Dimension | Literal[2, 3]"
    """Geometric dimensionality of the Fluent simulation. The default is ``Dimension.THREE``."""
    precision: "Precision | Literal['single', 'double']"
    """Floating point precision."""
    processor_count: int
    """Number of processors. The default is ``1``.  In job scheduler environments
    the total number of allocated cores is clamped to value of ``processor_count``.
    """
    start_timeout: int
    """Maximum allowable time in seconds for connecting to the Fluent
    server. The default is ``60`` if Fluent is launched outside a Slurm environment,
    no timeout if Fluent is launched within a Slurm environment.
    """
    additional_arguments: str
    """Additional arguments to send to Fluent as a string in the same
    format they are normally passed to Fluent on the command line.
    """
    cleanup_on_exit: bool
    """Whether to shut down the connected Fluent session when PyFluent is
    exited, or the ``exit()`` method is called on the session instance,
    or if the session instance becomes unreferenced. The default is ``True``.
    """
    start_transcript: bool
    """Whether to start streaming the Fluent transcript in the client. The
    default is ``True``. You can stop and start the streaming of the
    Fluent transcript subsequently via the method calls, ``transcript.start()``
    and ``transcript.stop()`` on the session object.
    """
    gpu: bool | list[int] | None
    """This option will start Fluent with the GPU Solver. A list of GPU IDs can be
    passed to use specific GPUs. If True is passed, the number of GPUs used will be
    clamped to the value of ``processor_count``. Please refer to
    *Starting the Fluent GPU Solver* section in *Fluent's User Guide* for more
    information like how to determine the GPU IDs.
    """
    start_watchdog: bool | None
    """When ``cleanup_on_exit`` is True, ``start_watchdog`` defaults to True,
    which means an independent watchdog process is run to ensure
    that any local GUI-less Fluent sessions started by PyFluent are properly closed (or killed if frozen)
    when the current Python process ends.
    """
    file_transfer_service: Any | None
    """File transfer service. Uploads/downloads files to/from the server."""
