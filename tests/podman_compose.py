"""Test Podman compose."""

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.utils.networking import get_free_port

port_1 = get_free_port()
port_2 = get_free_port()
container_dict = {"ports": {f"{port_1}": port_1, f"{port_2}": port_2}}

solver = pyfluent.launch_fluent(container_dict=container_dict)
assert len(solver._container.ports) == 2
case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
solver.file.read(file_name=case_file_name, file_type="case")
solver.exit()
