#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display import display
from .particle_tracks_child import particle_tracks_child


class particle_tracks(NamedObject[particle_tracks_child]):
    """'particle_tracks' child."""

    fluent_name = "particle-tracks"

    command_names = ["display"]

    display: display = display
    """
    display command of particle_tracks
    """
    child_object_type: particle_tracks_child = particle_tracks_child
    """
    child_object_type of particle_tracks.
    """
