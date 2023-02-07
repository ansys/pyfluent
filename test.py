import functools
import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.async_execution import asynchronous
import asyncio

solver_light = pyfluent.launch_fluent(show_gui=True)
solver_light.file.read(file_type="case", file_name="elbow.cas.h5", lightweight_setup=True)
# solver_light.setup.models.energy.enabled = False
# print(solver_light.setup.models.energy())


def sync(solver_light, fut):
    state = solver_light._root.get_state()
    solver_light.build_from_fluent_connection(fut.result().fluent_connection)
    solver_light._root.set_state(state)

fut: asyncio.Future = asynchronous(pyfluent.launch_fluent)(show_gui=True, case_filepath="elbow.cas.h5")
fut.add_done_callback(functools.partial(sync, solver_light))
#solver = pyfluent.launch_fluent(show_gui=True, case_filepath="elbow.cas.h5")
#solver_light.build_from_fluent_connection(solver.fluent_connection)
#solver_light._root.set_state(state)
#print(solver_light.setup.models.energy())

# solver._root.set_state(solver._root.get_state())

# solver._root.setup.materials.solid['aluminum'].chemical_formula.set_state(solver._root.setup.materials.solid['aluminum'].chemical_formula())  # fails
# solver._root.results.graphics.mesh.set_state(solver._root.results.graphics.mesh())  # fails
