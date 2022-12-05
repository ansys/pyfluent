"""Module providing visualization objects for PyVista."""

import inspect
import sys
from typing import Optional

from ansys.fluent.core.graphics_definitions.post_object_defns import (
    ContourDefn,
    MeshDefn,
    PathlinesDefn,
    SurfaceDefn,
    VectorDefn,
)
from ansys.fluent.core.graphics_definitions.pyvista.pyvista_windows_manager import (
    pyvista_windows_manager,
)
from ansys.fluent.core.meta import PyLocalContainer


class Graphics:
    """Provides the PyVista ``Graphics`` objects manager.

    This class provides access to ``Graphics`` object containers for a given
    session so that graphics objects can be created.

    Parameters
    ----------
    session : obj
        Session object.
    local_surfaces_provider : object, optional
        Object providing local surfaces so that you can access surfaces
        created in other modules, such as PyVista. The default is ``None``.

    Attributes
    ----------
    Meshes : dict
        Container for mesh objects.
    Surfaces : dict
        Container for surface objects.
    Contours : dict
        Container for contour objects.
    Vectors : dict
        Container for vector objects.
    """

    _sessions_state = {}

    def __init__(self, session, local_surfaces_provider=None):
        """Instantiate the ``Graphics`` object container.

        Parameters
        ----------
        session : obj
            Session object.
        local_surfaces_provider : object, optional
            Object providing local surfaces so that you can access surfaces
            created in other modules, such as PyVista. The default is ``None``.
        """
        session_state = Graphics._sessions_state.get(session.id if session else 1)
        if not session_state:
            session_state = self.__dict__
            Graphics._sessions_state[session.id if session else 1] = session_state
            self.session = session
            self._init_module(self, sys.modules[__name__])
        else:
            self.__dict__ = session_state
        self._local_surfaces_provider = lambda: local_surfaces_provider or getattr(
            self, "Surfaces", []
        )

    def _init_module(self, obj, mod):
        from ansys.fluent.visualization.post_helper import PostAPIHelper

        for name, cls in mod.__dict__.items():

            if cls.__class__.__name__ in (
                "PyLocalNamedObjectMetaAbstract",
            ) and not inspect.isabstract(cls):
                setattr(
                    obj,
                    cls.PLURAL,
                    PyLocalContainer(self, cls, PostAPIHelper),
                )

    def add_outline_mesh(self):
        """Add a mesh outline.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        meshes = getattr(self, "Meshes", None)
        if meshes is not None:
            outline_mesh_id = "Mesh-outline"
            outline_mesh = meshes[outline_mesh_id]
            outline_mesh.surfaces_list = [
                k
                for k, v in outline_mesh._api_helper.field_info()
                .get_surfaces_info()
                .items()
                if v["type"] == "zone-surf" and v["zone_type"] != "interior"
            ]
            return outline_mesh


class Mesh(MeshDefn):
    """Provides for displaying mesh graphics.

    Parameters
    ----------
    name :

    parent :

    api_helper :


    .. code-block:: python

        from ansys.fluent.visualization.pyvista import  Graphics

        graphics_session = Graphics(session)
        mesh1 = graphics_session.Meshes["mesh-1"]
        mesh1.show_edges = True
        mesh1.surfaces_list = ['wall']
        mesh1.display("window-0")
    """

    def display(self, window_id: Optional[str] = None):
        """Display mesh graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If an ID is not specified, a unique ID is used.
            The default is ``None``.
        """
        pyvista_windows_manager.plot(self, window_id)


class Pathlines(PathlinesDefn):
    """Pathlines definition for PyVista.

    .. code-block:: python

        from ansys.fluent.visualization.pyvista import  Graphics

        graphics_session = Graphics(session)
        pathlines1 = graphics_session.Pathlines["pathlines-1"]
        pathlines1.field = "velocity-magnitude"
        pathlines1.surfaces_list = ['inlet']
        pathlines1.display("window-0")
    """

    def display(self, window_id: Optional[str] = None):
        """Display mesh graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If an ID is not specified, a unique ID is used.
            The default is ``None``.
        """
        pyvista_windows_manager.plot(self, window_id)


class Surface(SurfaceDefn):
    """Provides for displaying surface graphics.

    Parameters
    ----------
    name :

    parent :

    api_helper :


    .. code-block:: python

        from ansys.fluent.visualization.pyvista import Graphics

        graphics_session = Graphics(session)
        surface1 = graphics_session.Surfaces["surface-1"]
        surface1.definition.type = "iso-surface"
        surface1.definition.iso_surface.field= "velocity-magnitude"
        surface1.definition.iso_surface.rendering= "contour"
        surface1.definition.iso_surface.iso_value = 0.0
        surface1.display("window-0")
    """

    def display(self, window_id: Optional[str] = None):
        """Display surface graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If an ID is not specified, a unique ID is used.
            The default is ``None``.
        """
        pyvista_windows_manager.plot(self, window_id)


class Contour(ContourDefn):
    """Provides for displaying contour graphics.

    Parameters
    ----------
    name :

    parent :

    api_helper :


    .. code-block:: python

        from ansys.fluent.visualization.pyvista import  Graphics

        graphics_session = Graphics(session)
        contour1 = graphics_session.Contours["contour-1"]
        contour1.field = "velocity-magnitude"
        contour1.surfaces_list = ['wall']
        contour1.display("window-0")
    """

    def display(self, window_id: Optional[str] = None):
        """Display contour graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If an ID is not specified, a unique ID is used.
            The default is ``None``.
        """
        pyvista_windows_manager.plot(self, window_id)


class Vector(VectorDefn):
    """Provides for displaying vector graphics.

    Parameters
    ----------
    name :

    parent :

    api_helper :


    .. code-block:: python

        from ansys.fluent.visualization.pyvista import  Graphics

        graphics_session = Graphics(session)
        vector1 = graphics_session.Vectors["vector-1"]
        vector1.surfaces_list  = ['symmetry']
        vector1.scale = 4.0
        vector1.skip = 4
        vector1.display("window-0")
    """

    def display(self, window_id: Optional[str] = None):
        """Display vector graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If an ID is not specified, a unique ID is used.
            The default is ``None``.
        """
        pyvista_windows_manager.plot(self, window_id)
