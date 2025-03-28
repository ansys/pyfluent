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

"""Provides a module for codegen messages."""

import logging

import ansys.fluent.core as pyfluent
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import TUIMenu

_CODEGEN_MSG_DATAMODEL = (
    "Currently calling the datamodel API in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local datamodel API classes."
)

_CODEGEN_MSG_TUI = (
    "Currently calling the TUI commands in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local TUI commands classes."
)

datamodel_logger = logging.getLogger("pyfluent.datamodel")
tui_logger = logging.getLogger("pyfluent.tui")


def _make_tui_module(session, module_name):
    try:
        from ansys.fluent.core import CODEGEN_OUTDIR

        tui_module = pyfluent.utils.load_module(
            f"{module_name}_tui_{session._version}",
            CODEGEN_OUTDIR / module_name / f"tui_{session._version}.py",
        )
        return tui_module.main_menu(
            session._tui_service, session._version, module_name, []
        )
    except (ImportError, FileNotFoundError):
        tui_logger.warning(_CODEGEN_MSG_TUI)
        return TUIMenu(session._tui_service, session._version, module_name, [])


def _make_datamodel_module(session, module_name):
    try:
        from ansys.fluent.core import CODEGEN_OUTDIR
        from ansys.fluent.core.codegen.datamodelgen import meshing_rule_file_names

        file_name = meshing_rule_file_names[module_name]
        module = pyfluent.utils.load_module(
            f"{module_name}_{session._version}",
            CODEGEN_OUTDIR / f"datamodel_{session._version}" / f"{file_name}.py",
        )
        return module.Root(session._se_service, module_name, [])
    except (ImportError, FileNotFoundError):
        datamodel_logger.warning("Generated API not found for %s.", module_name)
        datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
        return PyMenuGeneric(session._se_service, module_name)
