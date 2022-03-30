"""Module providing post objects for Matplotlib."""
import inspect
import sys
from typing import Optional

from ansys.fluent.core.meta import PyLocalContainer
from ansys.fluent.post.matplotlib import matplot_windows_manager
from ansys.fluent.post.post_object_defns import XYPlotDefn


class Plots:
    """Plot objects provider."""

    _sessions_state = {}

    def __init__(self, session, local_surfaces_provider=None):
        """
        Instantiate Plots, container of plot objects.

        Parameters
        ----------
        session :
            Session object.
        local_surfaces_provider : object, optional
            Object providing local surfaces.
        """
        session_state = Plots._sessions_state.get(session.id if session else 1)
        if not session_state:
            session_state = self.__dict__
            Plots._sessions_state[session.id if session else 1] = session_state
            self.session = session
            self._init_module(self, sys.modules[__name__])
        else:
            self.__dict__ = session_state
        self._local_surfaces_provider = (
            lambda: local_surfaces_provider or getattr(self, "Surfaces", [])
        )

    def _init_module(self, obj, mod):
        for name, cls in mod.__dict__.items():

            if cls.__class__.__name__ in (
                "PyLocalNamedObjectMetaAbstract",
            ) and not inspect.isabstract(cls):
                setattr(
                    obj,
                    cls.PLURAL,
                    PyLocalContainer(self, cls),
                )


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
        self._pre_display()
        matplot_windows_manager.plot(self, window_id)
        self._post_display()
