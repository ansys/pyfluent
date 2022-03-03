
import ansys.fluent as pyfluent
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solver
from functools import partial
import time


class WindLoad:
    
    def run(self):
        self.meshing_session = windload_mesh.run()
        self.solver_sessions = []
        inlet_velocities = [41.6, 41.7, 41.8]
        for inlet_velocity in inlet_velocities:
            input_object = windload_solve.InputObject()
            input_object.inlet_velocity = inlet_velocity
            self.solver_sessions.append(windload_solve.run(
                read_mesh=partial(transfer_mesh_from_meshing_to_solver, self.meshing_session, len(self.solver_sessions)),
                input_object=input_object))
            time.sleep(3)