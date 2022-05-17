#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .theory import theory
from .wave_ht import wave_ht
from .wave_len import wave_len
from .phase_diff import phase_diff
from .heading_angle import heading_angle
class wave_list_child(Group):
    """
    'child_object_type' of wave_list
    """

    fluent_name = "child-object-type"

    child_names = \
        ['theory', 'wave_ht', 'wave_len', 'phase_diff', 'heading_angle']

    theory: theory = theory
    """
    theory child of wave_list_child
    """
    wave_ht: wave_ht = wave_ht
    """
    wave_ht child of wave_list_child
    """
    wave_len: wave_len = wave_len
    """
    wave_len child of wave_list_child
    """
    phase_diff: phase_diff = phase_diff
    """
    phase_diff child of wave_list_child
    """
    heading_angle: heading_angle = heading_angle
    """
    heading_angle child of wave_list_child
    """
