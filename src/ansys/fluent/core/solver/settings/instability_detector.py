#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable_instability_detector import enable_instability_detector
from .set_cfl_limit import set_cfl_limit
from .set_cfl_type import set_cfl_type
from .set_velocity_limit import set_velocity_limit
from .unstable_event_outer_iterations import unstable_event_outer_iterations
class instability_detector(Group):
    """
    'instability_detector' child.
    """

    fluent_name = "instability-detector"

    child_names = \
        ['enable_instability_detector', 'set_cfl_limit', 'set_cfl_type',
         'set_velocity_limit', 'unstable_event_outer_iterations']

    enable_instability_detector: enable_instability_detector = enable_instability_detector
    """
    enable_instability_detector child of instability_detector
    """
    set_cfl_limit: set_cfl_limit = set_cfl_limit
    """
    set_cfl_limit child of instability_detector
    """
    set_cfl_type: set_cfl_type = set_cfl_type
    """
    set_cfl_type child of instability_detector
    """
    set_velocity_limit: set_velocity_limit = set_velocity_limit
    """
    set_velocity_limit child of instability_detector
    """
    unstable_event_outer_iterations: unstable_event_outer_iterations = unstable_event_outer_iterations
    """
    unstable_event_outer_iterations child of instability_detector
    """
