import inspect
import sys
from typing import Optional
from ansys.fluent.post.object_defns import (
    ContourDefn,
    MeshDefn,
    SurfaceDefn,
    VectorDefn,
)
from ansys.fluent.post.pyvista.plotter import plotter
from ansys.fluent.core.meta import PyLocalContainer


class Graphics:
    """Graphics objects provider."""

    def __init__(self, session):
        self.session = session
        self._init_module(self, sys.modules[__name__])

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

    def display(self, plotter_id: Optional[str] = None):
        """Display mesh graphics."""
        plotter.plot(self, plotter_id)


class Surface(SurfaceDefn):
    """Surface graphics."""

    def display(self, plotter_id: Optional[str] = None):
        """Display surface graphics."""
        plotter.plot(self, plotter_id)


class Contour(ContourDefn):
    """Contour graphics."""

    def display(self, plotter_id: Optional[str] = None):
        """Display contour graphics."""
        plotter.plot(self, plotter_id)


class Vector(VectorDefn):
    """Vector graphics."""

    def display(self, plotter_id: Optional[str] = None):
        """Display vector graphics."""
        plotter.plot(self, plotter_id)
