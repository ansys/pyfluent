"""Provides a module for generating Fluent result files."""

import importlib

from rstgen import _get_file_or_folder, generate

if __name__ == "__main__":
    meshing_tui = importlib.import_module(
        f"ansys.fluent.core.meshing.{_get_file_or_folder(mode='meshing', is_datamodel=False)}"
    )
    generate(main_menu=meshing_tui.main_menu, mode="meshing", is_datamodel=False)
    solver_tui = importlib.import_module(
        f"ansys.fluent.core.solver.{_get_file_or_folder(mode='solver', is_datamodel=False)}"
    )
    generate(main_menu=solver_tui.main_menu, mode="solver", is_datamodel=False)
