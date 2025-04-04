"""Helper module to generate Fluent API classes."""

import argparse
from pdb import pm
from time import time

from ansys.fluent.core import CODEGEN_OUTDIR, FluentMode, FluentVersion, launch_fluent
from ansys.fluent.core.codegen import StaticInfoType, allapigen
from ansys.fluent.core.codegen.print_fluent_version import print_fluent_version
from ansys.fluent.core.search import _generate_api_data
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name

if __name__ == "__main__":
    t0 = time()
    meshing = launch_fluent(mode=FluentMode.MESHING)
    version = get_version_for_file_name(session=meshing)
    gt_222 = FluentVersion(version) > FluentVersion.v222
    ge_231 = FluentVersion(version) >= FluentVersion.v231
    ge_242 = FluentVersion(version) >= FluentVersion.v242
    ge_252 = FluentVersion(version) >= FluentVersion.v252

    print("w")

    w = True or meshing._datamodel_service_se.get_static_info("workflow")
    print("m")

    m = True or meshing._datamodel_service_se.get_static_info("meshing")
    print("pm")

    pm = True or meshing._datamodel_service_se.get_static_info("PartManagement")
    print("pmf")
    pmf = True or meshing._datamodel_service_se.get_static_info("PMFileManagement")

    static_infos = {
        StaticInfoType.DATAMODEL_WORKFLOW: w,
        StaticInfoType.DATAMODEL_MESHING: m,
        StaticInfoType.DATAMODEL_PART_MANAGEMENT: pm,
        StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT: pmf,
    }
    print("tm")
    if False and gt_222:
        static_infos[StaticInfoType.TUI_MESHING] = (
            meshing._datamodel_service_tui.get_static_info("")
        )
    print("mu")
    if False and ge_242:
        static_infos[StaticInfoType.DATAMODEL_MESHING_UTILITIES] = (
            meshing._datamodel_service_se.get_static_info("MeshingUtilities")
        )
    print("mw")
    input()
    if ge_252:
        static_infos[StaticInfoType.DATAMODEL_MESHING_WORKFLOW] = (
            meshing._datamodel_service_se.get_static_info("meshing_workflow")
        )
    print("meshing.exit()")
    meshing.exit()

    print("launch_fluent()")
    solver = launch_fluent(
        mode=FluentMode.SOLVER
        # mode=FluentMode.SOLVER_ICING if ge_231 else FluentMode.SOLVER
    )
    print("p")
    static_infos[StaticInfoType.DATAMODEL_PREFERENCES] = (
        solver._datamodel_service_se.get_static_info("preferences")
    )
    print("s")
    static_infos[StaticInfoType.SETTINGS] = solver._settings_service.get_static_info()
    print("st")
    if gt_222:
        static_infos[StaticInfoType.TUI_SOLVER] = (
            solver._datamodel_service_tui.get_static_info("")
        )
    print("i")
    if False and ge_231:
        static_infos[StaticInfoType.DATAMODEL_FLICING] = (
            solver._datamodel_service_se.get_static_info("flserver")
        )
        print("sw")
        static_infos[StaticInfoType.DATAMODEL_SOLVER_WORKFLOW] = (
            solver._datamodel_service_se.get_static_info("solverworkflow")
        )
    t1 = time()
    print(f"\nTime to fetch static info: {t1 - t0:.2f} seconds")
    CODEGEN_OUTDIR.mkdir(parents=True, exist_ok=True)
    print_fluent_version(solver._app_utilities)
    solver.exit()
    parser = argparse.ArgumentParser(
        description="A script to write Fluent API files with an optional verbose output."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show paths of written Fluent API files.",
    )
    args = parser.parse_args()
    allapigen.generate(version, static_infos, args.verbose)
    t2 = time()
    print(f"Time to generate APIs: {t2 - t1:.2f} seconds")
    _generate_api_data(version=version)
