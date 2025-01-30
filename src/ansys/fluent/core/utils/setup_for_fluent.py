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

"""Provides a module to get global PyConsole objects."""

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.session_solver import Solver


def setup_for_fluent(*args, **kwargs):
    """Returns global PyConsole objects."""
    session = launch_fluent(*args, **kwargs)
    globals = {}
    if kwargs.get("mode", "solver") == "meshing":
        globals["meshing"] = session
        globals["PartManagement"] = session.PartManagement
        globals["PMFileManagement"] = session.PMFileManagement
        globals["solver"] = Solver(
            fluent_connection=session._fluent_connection,
            scheme_eval=session._fluent_connection._connection_interface.scheme_eval,
        )
    else:
        globals["solver"] = session

    globals["preferences"] = session.preferences
    globals["workflow"] = session.workflow

    return globals
