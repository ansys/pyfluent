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

"""Solver settings and context-management APIs for PyFluent.

This package exposes generated solver settings objects and the :func:`using`
context manager. Solver session classes are defined in modules under
:mod:`ansys.fluent.core.solver.session`: ``Solver`` directly inherits from
:class:`~ansys.fluent.core.execution.session.session.BaseSession`, and the
``SolverAero``, ``SolverIcing``, ``SolverLite``, and ``PrePost`` variants
inherit from ``Solver``. The session classes are re-exported through
:mod:`ansys.fluent.core.execution.session` and the top-level
``ansys.fluent.core`` API.
"""

from importlib import import_module
import logging

from ansys.fluent.core import using  # noqa: F401

logger = logging.getLogger("pyfluent.general")

try:
    from ansys.fluent.core.generated.solver.settings_builtin import (
        __all__ as _settings_all,
    )
    from ansys.fluent.core.generated.solver.settings_builtin import *  # noqa: F401, F403
except (ImportError, AttributeError, SyntaxError) as ex:
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
