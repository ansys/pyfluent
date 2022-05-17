#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .mesh_1 import mesh
from .contour import contour
from .vector import vector
from .pathlines import pathlines
from .particle_tracks import particle_tracks
from .lic import lic
from .views import views
class graphics(Group):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['mesh', 'contour', 'vector', 'pathlines', 'particle_tracks', 'lic',
         'views']

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
