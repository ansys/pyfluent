"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS MESHING WITHOUT THE SWITCH TO SOLVER***********
"""


from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session import _BaseSession
from ansys.fluent.core.session_base_meshing import _BaseMeshing
from ansys.fluent.core.utils.data_transfer import transfer_case


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
        file_type: str = "case",
        file_name_stem: str = None,
        num_files_to_try: int = 1,
        clean_up_mesh_file: bool = True,
        overwrite_previous: bool = True,
    ):
        """Transfer mesh to Fluent solver instances.

        Parameters
        ----------
        solvers : iterable
            Sequence of solver instances
        file_type : str, default "case"
            "case" or "mesh"
        file_name_stem : str
            Optional file name stem
        num_files_to_try : int, default 1
            Optional number of files to try to write,
            each with a different generated name.
            Defaults to 1
        clean_up_mesh_file: bool, default True
            Whether to remove the file at the end
        overwrite_previous: bool, default True
            Whether to overwrite the file if it already exists
        Returns
        -------
        None
        """
        transfer_case(
            self,
            solvers,
            file_type,
            file_name_stem,
            num_files_to_try,
            clean_up_mesh_file,
            overwrite_previous,
        )
