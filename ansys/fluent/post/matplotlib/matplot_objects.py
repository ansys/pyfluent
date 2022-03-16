"""Module providing post objects for Matplotlib."""

from typing import Optional

from ansys.fluent.core.meta import PyLocalContainer
from ansys.fluent.post.matplotlib import matplot_windows_manager
from ansys.fluent.post.post_object_defns import XYPlotDefn


class XYPlots(PyLocalContainer):
    """XYPlot objects provider."""

    _sessions_state = {}

    def __init__(self, session):
        """Instantiate XYPlots, containter of XYPlot."""
        session_state = XYPlots._sessions_state.get(session.id)
        if not session_state:
            session_state = self.__dict__
            XYPlots._sessions_state[session.id] = session_state
            self.session = session
            super().__init__(None, XYPlot)
        else:
            self.__dict__ = session_state


class XYPlot(XYPlotDefn):
    """XY Plot."""

    def plot(self, window_id: Optional[str] = None):
        """
        Draw XYPlot.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.

        """
        matplot_windows_manager.plot(self, window_id)
