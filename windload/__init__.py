
import ansys.fluent as pyfluent
from ansys.fluent.core.async_execution import asynchronous
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solver
from ansys.fluent.core.async_execution import asynchronous

from functools import partial
import time


class WindLoad:
    #@asynchronous
    def run(self):
        self.meshing_session = windload_mesh.run()
        self.solver_workflows = []
        inlet_velocity = 41.0
        for i in range(8):
            input_object = windload_solve.InputObject()
            input_object.inlet_velocity = inlet_velocity
            self.solver_workflows.append(windload_solve.create_workflow(
                read_mesh=partial(transfer_mesh_from_meshing_to_solver, self.meshing_session, len(self.solver_workflows)),
                input_object=input_object))
            inlet_velocity += 0.2
            time.sleep(3)