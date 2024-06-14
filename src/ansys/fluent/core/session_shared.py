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

        module = pyfluent.utils.load_module(
            f"{module_name}_{session._version}",
            CODEGEN_OUTDIR / f"datamodel_{session._version}" / f"{module_name}.py",
        )
        return module.Root(session._se_service, module_name, [])
    except (ImportError, FileNotFoundError):
        datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)
        return PyMenuGeneric(session._se_service, module_name)
