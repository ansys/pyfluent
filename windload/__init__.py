
import ansys.fluent as pyfluent
from .import windload_mesh, windload_solve
from ansys.fluent.addons.meshing import transfer_mesh_from_meshing_to_solver
from functools import partial

class WindLoad:

    def __init__(self) -> None:
        self.input_object = windload_solve.InputObject()

    def run(self):
        self.meshing_session = windload_mesh.run()
        self.solver_workflow = windload_solve.run(
            read_mesh=partial(transfer_mesh_from_meshing_to_solver, self.meshing_session),
            input_object=self.input_object)