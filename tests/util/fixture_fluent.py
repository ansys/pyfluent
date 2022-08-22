import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file


@pytest.fixture
def exhaust_system_geometry():
    global _exhaust_system_geometry_filename
    if not _exhaust_system_geometry_filename:
        _exhaust_system_geometry_filename = download_file(
            filename="exhaust_system.fmd", directory="pyfluent/exhaust_system"
        )
    return _exhaust_system_geometry_filename


_mixing_elbow_mesh_filename = None
_mixing_elbow_geom_filename = None


@pytest.fixture
def load_mixing_elbow_mesh(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="solver"
    )
    global _mixing_elbow_mesh_filename
    if not _mixing_elbow_mesh_filename:
        _mixing_elbow_mesh_filename = download_file(
            filename="mixing_elbow.msh.h5", directory="pyfluent/mixing_elbow"
        )
    solver_session.file.read(file_type="case", file_name=_mixing_elbow_mesh_filename)
    yield solver_session
    solver_session.exit()


_mixing_elbow_case_filename = None
_mixing_elbow_dat_filename = None


@pytest.fixture
def load_mixing_elbow_case_dat(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="solver"
    )
    global _mixing_elbow_case_filename
    if not _mixing_elbow_case_filename:
        _mixing_elbow_case_filename = download_file(
            filename="mixing_elbow.cas.h5", directory="pyfluent/mixing_elbow"
        )
    global _mixing_elbow_dat_filename
    if not _mixing_elbow_dat_filename:
        _mixing_elbow_dat_filename = download_file(
            filename="mixing_elbow.dat.h5", directory="pyfluent/mixing_elbow"
        )
    solver_session.file.read(
        file_type="case-data", file_name=_mixing_elbow_case_filename
    )
    yield solver_session
    solver_session.exit()


_mixing_elbow_param_case_filename = None
_mixing_elbow_param_dat_filename = None


@pytest.fixture
def load_mixing_elbow_param_case_dat(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="solver"
    )
    global _mixing_elbow_param_case_filename
    if not _mixing_elbow_param_case_filename:
        _mixing_elbow_param_case_filename = download_file(
            filename="elbow_param.cas.h5", directory="pyfluent/mixing_elbow"
        )
    global _mixing_elbow_param_dat_filename
    if not _mixing_elbow_param_dat_filename:
        _mixing_elbow_param_dat_filename = download_file(
            filename="elbow_param.dat.h5", directory="pyfluent/mixing_elbow"
        )
    solver_session.file.read(
        file_type="case-data", file_name=_mixing_elbow_param_case_filename
    )
    yield solver_session
    solver_session.exit()


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


_periodic_rot_case_filename = None


@pytest.fixture
def load_periodic_rot_cas(with_launching_container):
    solver_session = pyfluent.launch_fluent(
        precision="double", processor_count=2, mode="solver"
    )
    global _periodic_rot_case_filename
    if not _periodic_rot_case_filename:
        _periodic_rot_case_filename = download_file(
            filename="periodic_rot.cas.h5",
            directory="pyfluent/periodic_rot",
        )
    solver_session.file.read(file_type="case", file_name=_periodic_rot_case_filename)
    yield solver_session
    solver_session.exit()


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


_disk_mesh_filename = None


@pytest.fixture
def load_disk_mesh(with_launching_container):
    session = pyfluent.launch_fluent(
        precision="double", processor_count=2, version="2d"
    )
    global _disk_mesh_filename
    if not _disk_mesh_filename:
        _disk_mesh_filename = download_file(
            filename="disk.msh", directory="pyfluent/disk_tut"
        )
    session.solver.root.file.read(file_type="case", file_name=_disk_mesh_filename)
    yield session
    session.exit()
