from pathlib import Path

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file


def get_file_type(full_file_name):
    if ".msh" in full_file_name:
        return "mesh"
    if ".cas" in full_file_name:
        return "case"
    if ".dat" in full_file_name:
        return "data"
    if Path(full_file_name).suffix in (".fmd", ".scdoc", ".pmdb", ".agdb"):
        return "geometry"


def download_input_file(directory_name, full_file_name, data_file_name=None):
    file_type = get_file_type(full_file_name)
    file_name = "_%s_%s_filename" % (full_file_name.split(".")[0], file_type)
    globals()[file_name] = None
    if not globals()[file_name]:
        globals()[file_name] = download_file(
            filename=full_file_name,
            directory=directory_name,
        )
    file_name = globals()[file_name]
    if data_file_name:
        dat_file_type = get_file_type(data_file_name)
        dat_name = "_%s_%s_filename" % (data_file_name.split(".")[0], dat_file_type)
        globals()[dat_name] = None
        if not globals()[dat_name]:
            globals()[dat_name] = download_file(
                filename=data_file_name,
                directory=directory_name,
            )
        file_type = "case-data"
    return file_type, file_name


def get_name_info(allnamesdict, namescheck):
    name_selected = {}
    for names, details in allnamesdict.items():
        if isinstance(details, dict):
            for name in namescheck:
                if name in details.values() or name in details or name in names:
                    name_selected[name] = details
    return name_selected


@pytest.fixture
def sample_solver_session(with_launching_container):
    solver_session = pyfluent.launch_fluent(mode="solver")
    yield solver_session
    solver_session.exit()


@pytest.fixture
def launch_fluent_pure_meshing(with_launching_container):
    pure_meshing_session = pyfluent.launch_fluent(mode="pure-meshing")
    yield pure_meshing_session
    pure_meshing_session.exit()


@pytest.fixture
def launch_fluent_solver_3ddp_t2(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="solver"
    )
    yield solver_session
    solver_session.exit()


@pytest.fixture
def launch_fluent_solver_2ddp_t2(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        version="2d", precision="double", processor_count=2, mode="solver"
    )
    yield solver_session
    solver_session.exit()


_exhaust_system_geometry_filename = None


@pytest.fixture
def exhaust_system_geometry():
    global _exhaust_system_geometry_filename
    if not _exhaust_system_geometry_filename:
        _exhaust_system_geometry_filename = download_file(
            filename="exhaust_system.fmd", directory="pyfluent/exhaust_system"
        )
    return _exhaust_system_geometry_filename


@pytest.fixture
def load_mixing_elbow_mesh(launch_fluent_solver_3ddp_t2):
    solver_session = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/mixing_elbow", "mixing_elbow.msh.h5"
    )
    solver_session.file.read(file_type=input_type, file_name=input_name)
    yield solver_session
    solver_session.exit()


@pytest.fixture
def load_mixing_elbow_case_dat(launch_fluent_solver_3ddp_t2):
    solver_session = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/mixing_elbow", "mixing_elbow.cas.h5", "mixing_elbow.dat.h5"
    )
    solver_session.file.read(file_type=input_type, file_name=input_name)
    yield solver_session
    solver_session.exit()


@pytest.fixture
def load_static_mixer_case(sample_solver_session):
    solver = sample_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(file_type="case", file_name=case_path)
    yield solver
    solver.exit()


@pytest.fixture
def load_mixing_elbow_param_case_dat(launch_fluent_solver_3ddp_t2):
    solver_session = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/mixing_elbow", "elbow_param.cas.h5", "elbow_param.dat.h5"
    )
    solver_session.file.read(file_type=input_type, file_name=input_name)
    yield solver_session
    solver_session.exit()


_mixing_elbow_geom_filename = None


@pytest.fixture
def load_mixing_elbow_pure_meshing(with_launching_container):
    pure_meshing_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="pure-meshing"
    )
    global _mixing_elbow_geom_filename
    if not _mixing_elbow_geom_filename:
        _mixing_elbow_geom_filename = download_file(
            filename="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
        )

    pure_meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    pure_meshing_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=_mixing_elbow_geom_filename, LengthUnit="in"
    )

    yield pure_meshing_session
    pure_meshing_session.exit()


@pytest.fixture
def load_mixing_elbow_meshing(with_launching_container):
    meshing_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="meshing"
    )
    global _mixing_elbow_geom_filename
    if not _mixing_elbow_geom_filename:
        _mixing_elbow_geom_filename = download_file(
            filename="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
        )

    meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    meshing_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=_mixing_elbow_geom_filename, LengthUnit="in"
    )

    yield meshing_session
    meshing_session.exit()


@pytest.fixture
def load_periodic_rot_cas(launch_fluent_solver_3ddp_t2):
    solver_session = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/periodic_rot", "periodic_rot.cas.h5"
    )
    solver_session.file.read(file_type=input_type, file_name=input_name)
    yield solver_session
    solver_session.exit()


@pytest.fixture
def load_disk_mesh(launch_fluent_solver_2ddp_t2):
    solver_session = launch_fluent_solver_2ddp_t2
    input_type, input_name = download_input_file("pyfluent/rotating_disk", "disk.msh")
    solver_session.file.read(file_type=input_type, file_name=input_name)
    yield solver_session
    solver_session.exit()
