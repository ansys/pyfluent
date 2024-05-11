"""Helper module to generate Fluent API classes."""

from time import time

from ansys.fluent.core import FluentMode, FluentVersion, launch_fluent
from ansys.fluent.core.codegen import StaticInfoType, allapigen, print_fluent_version
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name

if __name__ == "__main__":
    t0 = time()
    solver = launch_fluent()
    meshing = launch_fluent(mode=FluentMode.MESHING_MODE)
    version = get_version_for_file_name(session=solver)
    static_infos = {
        StaticInfoType.TUI_SOLVER: solver._datamodel_service_tui.get_static_info(""),
        StaticInfoType.TUI_MESHING: meshing._datamodel_service_tui.get_static_info(""),
        StaticInfoType.DATAMODEL_WORKFLOW: meshing._datamodel_service_se.get_static_info(
            "workflow"
        ),
        StaticInfoType.DATAMODEL_MESHING: meshing._datamodel_service_se.get_static_info(
            "meshing"
        ),
        StaticInfoType.DATAMODEL_PART_MANAGEMENT: meshing._datamodel_service_se.get_static_info(
            "PartManagement"
        ),
        StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT: meshing._datamodel_service_se.get_static_info(
            "PMFileManagement"
        ),
        StaticInfoType.DATAMODEL_PREFERENCES: solver._datamodel_service_se.get_static_info(
            "preferences"
        ),
        StaticInfoType.SETTINGS: solver._settings_service.get_static_info(),
    }
    if FluentVersion(version) >= FluentVersion.v231:
        flicing = launch_fluent(mode=FluentMode.SOLVER_ICING)
        static_infos[StaticInfoType.DATAMODEL_FLICING] = (
            flicing._datamodel_service_se.get_static_info("flserver")
        )
        static_infos[StaticInfoType.DATAMODEL_SOLVER_WORKFLOW] = (
            solver._datamodel_service_se.get_static_info("solverworkflow")
        )
    if FluentVersion(version) >= FluentVersion.v242:
        static_infos[StaticInfoType.DATAMODEL_MESHING_UTILITIES] = (
            meshing._datamodel_service_se.get_static_info("MeshingUtilities")
        )
    t1 = time()
    print(f"Time to fetch static info: {t1 - t0:.2f} seconds")
    print_fluent_version.generate(version, solver.scheme_eval.scheme_eval)
    allapigen.generate(version, static_infos)
    t2 = time()
    print(f"Time to generate APIs: {t2 - t1:.2f} seconds")
