
import os

def transfer_mesh_from_meshing_to_solver(meshing_session, id, solver_session):
    mesh_dir = os.getenv("TEMP") or os.getenv("TMP")
    if not isinstance(mesh_dir, str):
        mesh_dir = "."
    file_stem = "fluent_mesh_"
    file_ext = ".msh.cas.h5"
    for idx in range(100):
        file_name = file_stem + str(id) + "_" + str(idx) + file_ext
        path = os.path.join(mesh_dir, file_name)
        if not os.path.isfile(path):
            meshing_session.tui.meshing.file.write_case(path).result()
            solver_session.tui.solver.file.read_case(path).result()
            os.remove(path)
            return
    raise RuntimeError("Could not write mesh to transfer")
