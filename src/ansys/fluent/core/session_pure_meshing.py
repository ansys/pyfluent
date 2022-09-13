"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS MESHING WITHOUT THE SWITCH TO SOLVER***********
"""

import os
import time

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session import _BaseSession
from ansys.fluent.core.session_base_meshing import _BaseMeshing
from ansys.fluent.core.utils.async_execution import asynchronous


class PureMeshing(_BaseSession):
    """Encapsulates a Fluent - Pure Meshing session connection.
    PureMeshing(_BaseSession) holds the top-level objects
    for meshing TUI and various meshing datamodel API calls.
    In pure-meshing mode, switch to solver is not available.
    Public attributes of this class or extracted from the _BaseMeshing
    class"""

    def __init__(self, fluent_connection: _FluentConnection):
        super(PureMeshing, self).__init__(fluent_connection=fluent_connection)
        self._base_meshing = _BaseMeshing(self.execute_tui, fluent_connection)

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        return self._base_meshing.tui

    @property
    def meshing(self):
        """meshing datamodel root."""
        return self._base_meshing.meshing

    @property
    def workflow(self):
        """workflow datamodel root."""
        return self._base_meshing.workflow

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        return self._base_meshing.PartManagement

    @property
    def PMFileManagement(self):
        """PMFileManagement datamodel root."""
        return self._base_meshing.PMFileManagement

    @property
    def preferences(self):
        """preferences datamodel root."""
        return self._base_meshing.preferences

    def transfer_mesh_to_solvers(
        self,
        solvers,
        file_name_stem=None,
        num_files_to_try=1,
        clean_up_mesh_file=True,
        sleep_time=0,
    ):
        _transfer_mesh_from_meshing_to_solvers(
            self,
            solvers,
            file_name_stem,
            num_files_to_try,
            clean_up_mesh_file,
            sleep_time,
        )


@asynchronous
def _read_mesh_into_solver(file_name, solver, sleep_time):
    print("read in solver")
    solver.upload(file_name)
    time.sleep(sleep_time)
    solver.tui.file.read_case(file_name)  # make this asynchronous
    print("have read in solver")


def _read_mesh_into_solvers(file_name, solvers, sleep_time):
    reads = []
    for solver in solvers:
        reads.append(_read_mesh_into_solver(file_name, solver, sleep_time))
    for r in reads:
        r.result()


def _transfer_mesh_from_meshing_to_solvers(
    meshing, solvers, file_name_stem, num_files_to_try, clean_up_mesh_file, sleep_time
):
    file_ext = ".msh.cas.h5"
    for idx in range(num_files_to_try):
        file_name = (file_name_stem or "fluent_mesh_") + "_" + str(idx) + file_ext
        folder = os.getenv("TMP", os.getenv("TMPDIR", "."))
        file_name = os.path.join(folder, file_name)
        print(file_name)
        if not os.path.isfile(file_name):
            print("save mesh from meshing")
            meshing.tui.file.write_case(file_name)
            time.sleep(sleep_time)
            meshing.download(file_name, ".")
            time.sleep(sleep_time)
            print("saved mesh from meshing")
            _read_mesh_into_solvers(file_name, solvers, sleep_time)
            if clean_up_mesh_file:
                os.remove(file_name)
            return
    raise RuntimeError("Could not write mesh to transfer")
