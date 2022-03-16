"""Module providing post objects for PyVista."""

import inspect
import sys
from typing import Optional

from ansys.fluent.core.meta import PyLocalContainer
from ansys.fluent.post.post_object_defns import (
    ContourDefn,
    MeshDefn,
    SurfaceDefn,
    VectorDefn,
)
from ansys.fluent.post.pyvista.pyvista_windows_manager import (
    pyvista_windows_manager,
)


class Graphics:
    """Graphics objects provider."""

    _sessions_state = {}

    def __init__(self, session):
        """Instantiate Graphics, containter of graphics objects."""
        session_state = Graphics._sessions_state.get(
            session.id if session else 1
        )
        if not session_state:
            session_state = self.__dict__
            Graphics._sessions_state[
                session.id if session else 1
            ] = session_state
            self.session = session
            self._init_module(self, sys.modules[__name__])
        else:
            self.__dict__ = session_state

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


class Mesh(MeshDefn):
    """Mesh graphics."""

    def display(self, window_id: Optional[str] = None):
        """
        Display mesh graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pyvista_windows_manager.plot(self, window_id)


class Surface(SurfaceDefn):
    """Surface graphics."""

    def display(self, window_id: Optional[str] = None):
        """
        Display surface graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pyvista_windows_manager.plot(self, window_id)


class Contour(ContourDefn):
    """Contour graphics."""

    def display(self, window_id: Optional[str] = None):
        """
        Display contour graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pyvista_windows_manager.plot(self, window_id)


class Vector(VectorDefn):
    """Vector graphics."""

    def display(self, window_id: Optional[str] = None):
        """
        Display vector graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pyvista_windows_manager.plot(self, window_id)
