"""Provides a module for generating Fluent datamodel RST files."""

import importlib

from rstgen import _get_file_or_folder, _write_datamodel_index_doc, generate


def generate_meshing_datamodels():
    """Generate meshing datamodel RST files."""
    meshing_datamodel_roots = []
    available_datamodels = []
    meshing_datamodels = [
        "meshing",
        "MeshingUtilities",
        "PartManagement",
        "PMFileManagement",
        "preferences",
        "workflow",
    ]
    for meshing_datamodel in meshing_datamodels:
        try:
            datamodel = importlib.import_module(
                f"ansys.fluent.core.generated.{_get_file_or_folder(mode='meshing', is_datamodel=True)}.{meshing_datamodel}"
            )
            if datamodel:
                meshing_datamodel_roots.append(datamodel.Root)
                available_datamodels.append(meshing_datamodel)
        except ModuleNotFoundError:
            pass
    _write_datamodel_index_doc(available_datamodels, "meshing")
    for root in meshing_datamodel_roots:
        generate(main_menu=root, mode="meshing", is_datamodel=True)


def generate_solver_datamodels():
    """Generate solver datamodel RST files."""
    solver_datamodel_roots = []
    available_datamodels = []
    solver_datamodels = ["flicing", "preferences", "solverworkflow", "workflow"]
    for solver_datamodel in solver_datamodels:
        try:
            datamodel = importlib.import_module(
                f"ansys.fluent.core.generated.{_get_file_or_folder(mode='solver', is_datamodel=True)}.{solver_datamodel}"
            )
            if datamodel:
                solver_datamodel_roots.append(datamodel.Root)
                available_datamodels.append(solver_datamodel)
        except ModuleNotFoundError:
            pass
    _write_datamodel_index_doc(available_datamodels, "solver")
    for root in solver_datamodel_roots:
        generate(main_menu=root, mode="solver", is_datamodel=True)


if __name__ == "__main__":
    generate_meshing_datamodels()
    generate_solver_datamodels()
