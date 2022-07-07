import pytest
import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file

@pytest.fixture
def load_mixing_elbow_mesh():
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    mixing_elbow_mesh_filename = download_file(
        filename="mixing_elbow.msh.h5", directory="pyfluent/mixing_elbow")
    session.solver.root.file.read(file_type="case", file_name=mixing_elbow_mesh_filename)
    return session