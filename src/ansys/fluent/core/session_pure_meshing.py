"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS MESHING WITHOUT THE SWITCH TO SOLVER***********
"""

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing


class PureMeshing(BaseSession):
    """Encapsulates a Fluent - Pure Meshing session connection.
    PureMeshing(BaseSession) holds the top-level objects
    for meshing TUI and various meshing datamodel API calls."""

    def __init__(self, fluent_connection: _FluentConnection):
        super(PureMeshing, self).__init__(fluent_connection=fluent_connection)

        self._base_meshing = BaseMeshing(fluent_connection)

    def __getattr__(self, attr):
        return getattr(self._base_meshing, attr)
