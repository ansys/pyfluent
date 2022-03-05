
import ansys.fluent as pyfluent
from ansys.fluent.core.async_execution import asynchronous
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solvers
from ansys.fluent.core.async_execution import asynchronous

from functools import partial
import time


class WindLoad:
    #@asynchronous
    def run(self):
        self.meshing_session = windload_mesh.run()
        num_solves = 4
        self.solver_workflows = []
        for i in range(num_solves):
            input_object = windload_solve.InputObject()
            input_object.inlet_velocity = 41.0 + 0.2 * i
            solver_workflow = windload_solve.create_workflow(
                launcher = pyfluent.launch_fluent, 
                input_object=input_object)
            self.solver_workflows.append(solver_workflow)
        transfer_mesh_from_meshing_to_solvers(
            self.meshing_session.result(), 
            (solver_workflow.result().session for solver_workflow in self.solver_workflows)
            )
        for solver_workflow in self.solver_workflows:
            solver_workflow.result().run()


             