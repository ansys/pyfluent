from typing import Callable

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.examples import download_file


def fluent_launcher_args(args: str):
    def fluent_launcher_args_inner(f: Callable):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        wrapper.fluent_launcher_args = args
        return wrapper

    return fluent_launcher_args_inner


def mixing_elbow_geometry_filename(globals):
    return download_file(
        file_name="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )


def exhaust_system_geometry_filename(globals):
    return download_file(
        file_name="exhaust_system.fmd", directory="pyfluent/exhaust_system"
    )


@fluent_launcher_args("3ddp -meshing")
def new_meshing_session(globals):
    meshing = globals["meshing"]
    return meshing


@fluent_launcher_args("3ddp -meshing")
def new_pure_meshing_session(globals):
    return new_meshing_session(globals)


@fluent_launcher_args("3ddp -meshing")
def watertight_workflow_session(globals):
    meshing = new_meshing_session(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def fault_tolerant_workflow_session(globals):
    meshing = new_meshing_session(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    return meshing


@fluent_launcher_args("3ddp -meshing")
def mixing_elbow_watertight_pure_meshing_session(globals):
    meshing = new_pure_meshing_session(globals)
    geometry_filename = mixing_elbow_geometry_filename(globals)
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    meshing.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=geometry_filename, LengthUnit="in"
    )
    return meshing


@fluent_launcher_args("3ddp")
def new_solver_session(globals):
    solver = globals["solver"]
    return solver


@fluent_launcher_args("3d")
def new_solver_session_sp(globals):
    return new_solver_session(globals)


@fluent_launcher_args("2ddp")
def new_solver_session_2d(globals):
    return new_solver_session(globals)


@fluent_launcher_args("3ddp")
def static_mixer_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("3ddp")
def static_mixer_case_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_case_data_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case-data", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def mixing_elbow_param_case_data_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file("elbow_param.cas.h5", "pyfluent/mixing_elbow")
    download_file("elbow_param.dat.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read(file_type="case-data", file_name=case_name)
    return solver


@fluent_launcher_args("2ddp")
def disk_settings_session(globals):
    solver = new_solver_session_2d(globals)
    case_name = download_file("disk.cas.h5", "pyfluent/rotating_disk")
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


@fluent_launcher_args("2ddp")
def disk_case_session(globals):
    solver = new_solver_session_2d(globals)
    case_name = download_file("disk.cas.h5", "pyfluent/rotating_disk")
    solver.file.read(file_type="case", file_name=case_name)
    return solver


@fluent_launcher_args("3ddp")
def periodic_rot_settings_session(globals):
    solver = new_solver_session(globals)
    case_name = download_file(
        "periodic_rot.cas.h5",
        "pyfluent/periodic_rot",
    )
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    return solver


monkeypatch = pytest.MonkeyPatch()


def disable_datamodel_cache(globals):
    monkeypatch.setattr(pyfluent, "DATAMODEL_USE_STATE_CACHE", False)


def display_names_as_keys_in_cache(globals):
    DataModelCache.use_display_name = True


def new_meshing_session2(globals):
    session = pyfluent.launch_fluent(mode=pyfluent.LaunchMode.MESHING)
    return session


def new_solver_session2(globals):
    session = pyfluent.launch_fluent()
    return session


def static_mixer_case_session2(globals):
    session = new_solver_session2(globals)
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.file.read(file_type="case", file_name=case_name)
    return session
