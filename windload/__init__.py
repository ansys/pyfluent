
import ansys.fluent as pyfluent
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solver
from functools import partial

class WindLoad:
    
    def run(self):
        self.meshing_session = windload_mesh.run()
        inlet_velocities = [41.0, 41.4, 41.7, 50.0]
        id = 0
        for inlet_velocity in inlet_velocities:
            input_object = windload_solve.InputObject()
            input_object.inlet_velocity = inlet_velocity
            windload_solve.run(
                read_mesh=partial(transfer_mesh_from_meshing_to_solver, self.meshing_session, id),
                input_object=input_object)
            id += 1