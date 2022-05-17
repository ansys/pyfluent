#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_2 import enabled
from .stream_id import stream_id
class track_single_particle_stream(Group):
    """
    'track_single_particle_stream' child.
    """

    fluent_name = "track-single-particle-stream"

    child_names = \
        ['enabled', 'stream_id']

    enabled: enabled = enabled
    """
    enabled child of track_single_particle_stream
    """
    stream_id: stream_id = stream_id
    """
    stream_id child of track_single_particle_stream
    """
