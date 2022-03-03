
import ansys.fluent as pyfluent
from ansys.fluent.core.async_execution import asynchronous
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solver
from ansys.fluent.core.async_execution import asynchronous

from functools import partial
import time


class WindLoad:
    @asynchronous
    def run(self):
        self.meshing_session = windload_mesh.run()
        self.solver_sessions = []
        inlet_velocity = 41.0
        for i in range(8):
            input_object = windload_solve.InputObject()
            input_object.inlet_velocity = inlet_velocity
            self.solver_sessions.append(windload_solve.run(
                read_mesh=partial(transfer_mesh_from_meshing_to_solver, self.meshing_session, len(self.solver_sessions)),
                input_object=input_object))
            inlet_velocity += 0.2
            time.sleep(3)