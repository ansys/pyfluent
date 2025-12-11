"""Provides a module for generating Fluent RST files."""

import importlib
import logging

from rstgen import _get_file_or_folder, generate

logger = logging.getLogger("pyfluent.tui")

if __name__ == "__main__":
    try:
        meshing_tui = importlib.import_module(
            f"ansys.fluent.core.generated.meshing.{_get_file_or_folder(mode='meshing', is_datamodel=False)}"
        )
        generate(main_menu=meshing_tui.main_menu, mode="meshing", is_datamodel=False)
    except ModuleNotFoundError as ex:
        logger.debug(ex)
    try:
        solver_tui = importlib.import_module(
            f"ansys.fluent.core.generated.solver.{_get_file_or_folder(mode='solver', is_datamodel=False)}"
        )
        generate(main_menu=solver_tui.main_menu, mode="solver", is_datamodel=False)
    except ModuleNotFoundError as ex:
        logger.debug(ex)
