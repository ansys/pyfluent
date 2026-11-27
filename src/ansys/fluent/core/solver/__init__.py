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

"""Solver settings and session classes.

Use the hierarchical Python settings API to configure and run the Fluent
solver. Start at the :ref:`settings root <ref_root>` to navigate the full
hierarchy.

Solver sessions are created and managed through session objects
( See :ref:`session <ref_ansys_fluent_core_solver_session>` ).

Import commonly used settings classes such as ``Viscous`` and
``VelocityInlet`` directly from this package, rather than navigating
the hierarchy to find them.

"""

from importlib import import_module
import logging

from ansys.fluent.core.execution import using

logger = logging.getLogger("pyfluent.general")

try:
    from ansys.fluent.core.generated.solver.settings_builtin import *  # noqa: F401, F403
    from ansys.fluent.core.generated.solver.settings_builtin import (
        __all__ as _settings_all,
    )
except (ImportError, AttributeError, SyntaxError, ValueError) as ex:
    _settings_all = []
    logger.debug(ex)

_SESSION_MODULES = {
    "Solver": "solver",
    "SolverAero": "solver_aero",
    "SolverIcing": "solver_icing",
    "SolverLite": "solver_lite",
    "PrePost": "solver_pre_post",
}

__all__ = ["using", *_settings_all, *_SESSION_MODULES]


def __getattr__(name: str):
    module_name = _SESSION_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f".session.{module_name}", __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value
