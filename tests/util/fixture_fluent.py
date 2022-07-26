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


@pytest.fixture
def load_mixing_elbow_mesh(with_launching_container):
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    global _mixing_elbow_mesh_filename
    if not _mixing_elbow_mesh_filename:
        _mixing_elbow_mesh_filename = download_file(
            filename="mixing_elbow.msh.h5", directory="pyfluent/mixing_elbow"
        )
    session.solver.root.file.read(
        file_type="case", file_name=_mixing_elbow_mesh_filename
    )
    yield session
    session.exit()


_mixing_elbow_case_filename = None
_mixing_elbow_dat_filename = None


@pytest.fixture
def load_mixing_elbow_case_dat(with_launching_container):
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
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
    session.solver.root.file.read(
        file_type="case-data", file_name=_mixing_elbow_case_filename
    )
    yield session
    session.exit()


_mixing_elbow_param_case_filename = None
_mixing_elbow_param_dat_filename = None


@pytest.fixture
def load_mixing_elbow_param_case_dat(with_launching_container):
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
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
    session.solver.root.file.read(
        file_type="case-data", file_name=_mixing_elbow_param_case_filename
    )
    yield session
    session.exit()
