"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS MESHING WITHOUT THE SWITCH TO SOLVER***********
"""

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session import _BaseSession
from ansys.fluent.core.session_base_meshing import _BaseMeshing


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

        for attr in _BaseMeshing.meshing_attrs:
            setattr(self, attr, getattr(self._base_meshing, attr))
