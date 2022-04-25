#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .contour import contour
from .lic import lic
from .mesh_1 import mesh
from .particle_tracks import particle_tracks
from .pathlines import pathlines
from .vector import vector
from .views import views


class graphics(Group):
    """'graphics' child."""

    fluent_name = "graphics"

    child_names = [
        "mesh",
        "contour",
        "vector",
        "pathlines",
        "particle_tracks",
        "lic",
        "views",
    ]

    mesh: mesh = mesh
    """
    mesh child of graphics
    """
    contour: contour = contour
    """
    contour child of graphics
    """
    vector: vector = vector
    """
    vector child of graphics
    """
    pathlines: pathlines = pathlines
    """
    pathlines child of graphics
    """
    particle_tracks: particle_tracks = particle_tracks
    """
    particle_tracks child of graphics
    """
    lic: lic = lic
    """
    lic child of graphics
    """
    views: views = views
    """
    views child of graphics
    """
