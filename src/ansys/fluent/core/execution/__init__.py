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

"""Launch Fluent processes and manage their execution environment.

This package groups the lower-level components used to start Fluent, connect
to running instances, create PyFluent sessions, and configure parallel or
container-based execution:

* :mod:`launcher` handles local, remote, and scheduler-based launch workflows.
* :mod:`session` provides :class:`BaseSession` and :class:`FileSession`; solver
    and meshing session classes are defined in their respective packages.
* :mod:`docker` provides Docker and Podman Compose support.
* :mod:`scheduler` builds parallel execution options from allocated resources.

Most applications can use the public launch API from
``ansys.fluent.core``. The subpackages here are available for lower-level
workflows and are loaded on demand.
"""

from importlib import import_module

__all__ = ("docker", "launcher", "scheduler", "session")


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f".{name}", __name__)
    globals()[name] = module
    return module
